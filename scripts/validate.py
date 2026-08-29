#!/usr/bin/env python3
"""Repository validation for CI.

Checks:
1. Every skill has a SKILL.md with valid frontmatter (name matches the
   directory, description present and within length limits).
2. Every markdown file in a skill carries a `last_verified: YYYY-MM-DD`
   frontmatter field that is a real date and is not in the future.
3. Every ```json code block in skill markdown files parses as JSON.
4. marketplace manifests are valid JSON.
5. Every declared version is present and agrees: both marketplace manifests
   and every SKILL.md frontmatter, and CHANGELOG.md has a matching section.
6. The EN and JP skills stay structurally in sync (same file list, same
   heading counts per level, same number of JSON code blocks per file,
   same `last_verified` date per file).

Stdlib only — no dependencies.
"""

import datetime
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / ".claude" / "skills"
MANIFESTS = [REPO / "marketplace.json", REPO / ".claude-plugin" / "marketplace.json"]
CHANGELOG = REPO / "CHANGELOG.md"
SYNC_PAIRS = [("seo-mastery", "seo-mastery-jp")]
MAX_DESCRIPTION_LENGTH = 1024
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FIELD_PATTERN = re.compile(r"^(\w[\w-]*):\s*(.*)$")

# A YAML plain (unquoted) scalar may not contain ": " or " #", may not end in
# ":", and may not start with an indicator character. The frontmatter is read
# by a real YAML parser when the skill loads, so a value this script accepts
# but YAML rejects means the skill silently fails to load with CI still green
# — which is how a JP SKILL.md whose description contained "使い分け: " passed
# review. The trailing ":" is the same failure one character further along:
# "description: 使い分け:" is a scanner error too.
PLAIN_FORBIDDEN = re.compile(r": |\s#|:$")
YAML_INDICATORS = ",[]{}#&*!|>%@`"
# "-", "?" and ":" are indicators only when a space or the end of the value
# follows, so "-alpha" is a perfectly good plain scalar while "- alpha" is a
# sequence entry. Rejecting them unconditionally failed valid frontmatter.
SPACED_INDICATORS = "-?:"
DOUBLE_QUOTE_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "0": "\0"}
# \x, \u and \U consume a fixed run of hex digits. Expanding them is what keeps
# a description's measured length equal to the length YAML produces.
HEX_ESCAPES = {"x": 2, "u": 4, "U": 8}
HEX_DIGITS = re.compile(r"[0-9A-Fa-f]+")
# A value of "|" or ">", optionally with a chomping and an indentation
# indicator and a trailing comment: the key's value is the indented block that
# follows rather than text on the same line.
BLOCK_SCALAR = re.compile(r"^([|>])([+-]?[1-9]?|[1-9][+-]?)(?:\s+#.*)?$")

# CI runs in UTC while contributors may be ahead of it, so a file stamped with
# "today" in JST looks like tomorrow to the runner. One day of slack keeps that
# from failing a build that is actually correct.
FUTURE_TOLERANCE = datetime.timedelta(days=1)

errors = []
_frontmatter_cache = {}
_markdown_cache = {}


def error(msg: str) -> None:
    errors.append(msg)
    print(f"ERROR: {msg}")


def _read_quoted(raw: str, quote: str) -> tuple:
    """Read one YAML quoted scalar. Returns (value, rest); raises on no close."""
    out = []
    i = 1
    while i < len(raw):
        char = raw[i]
        if char == quote:
            if quote == "'" and raw[i + 1 : i + 2] == "'":
                out.append("'")
                i += 2
                continue
            return "".join(out), raw[i + 1 :]
        if char == "\\" and quote == '"':
            following = raw[i + 1 : i + 2]
            if not following:
                raise ValueError("value ends with a dangling backslash")
            width = HEX_ESCAPES.get(following)
            if width:
                digits = raw[i + 2 : i + 2 + width]
                if len(digits) != width or not HEX_DIGITS.fullmatch(digits):
                    raise ValueError(f"'\\{following}' escape needs {width} hex digits")
                try:
                    out.append(chr(int(digits, 16)))
                except ValueError:
                    raise ValueError(f"'\\{following}{digits}' is not a character") from None
                i += 2 + width
                continue
            out.append(DOUBLE_QUOTE_ESCAPES.get(following, following))
            i += 2
            continue
        out.append(char)
        i += 1
    raise ValueError(f"value is not closed with {quote}")


def _parse_scalar(label: str, key: str, raw: str) -> str:
    """Return a frontmatter scalar's value, reporting what YAML would reject.

    The value is returned best-effort even when invalid, so a malformed field
    is reported once here rather than also as a bogus "field is missing" from
    every downstream check.
    """
    if raw[:1] in ('"', "'"):
        quote = raw[0]
        try:
            value, rest = _read_quoted(raw, quote)
        except ValueError as exc:
            error(f"{label}: frontmatter '{key}': {exc}")
            return raw[1:].strip()
        if rest.strip():
            error(f"{label}: frontmatter '{key}': trailing text after the closing {quote}")
        return value

    value = raw.strip()
    if not value:
        return value
    if value[0] in YAML_INDICATORS or (
        value[0] in SPACED_INDICATORS and value[1:2] in ("", " ")
    ):
        error(
            f"{label}: frontmatter '{key}': unquoted value starts with the YAML "
            f"indicator '{value[0]}' — wrap the value in double quotes"
        )
        return value
    match = PLAIN_FORBIDDEN.search(value)
    if match:
        found = (
            "ends with ':'"
            if match.group() == ":" and match.end() == len(value)
            else f"contains {match.group()!r}"
        )
        error(
            f"{label}: frontmatter '{key}': unquoted value {found}, "
            f"which YAML rejects — wrap the value in double quotes"
        )
    return value


def _fold(lines: list) -> str:
    """Join lines the way YAML folds them: a line break becomes a space and a
    blank line becomes a newline."""
    out = ""
    for line in lines:
        if not line:
            out += "\n"
        elif not out or out.endswith("\n"):
            out += line
        else:
            out += " " + line
    return out


def _block_scalar(header, continuation: list) -> str:
    """Expand a `|` or `>` block into the string YAML would produce."""
    style, modifiers = header.group(1), header.group(2)
    chomp = next((c for c in modifiers if c in "+-"), "")
    explicit = next((c for c in modifiers if c.isdigit()), "")

    body = list(continuation)
    trailing = 0
    while body and not body[-1].strip():
        body.pop()
        trailing += 1
    if not body:
        return "\n" * trailing if chomp == "+" else ""

    # An explicit indentation indicator is relative to the parent node, and in
    # frontmatter the parent key always sits at column 0.
    indent = int(explicit) if explicit else min(
        len(line) - len(line.lstrip()) for line in body if line.strip()
    )
    body = [line[indent:] if line.strip() else "" for line in body]
    text = "\n".join(body) if style == "|" else _fold(body)
    if chomp == "-":
        return text
    if chomp == "+":
        return text + "\n" * (trailing + 1)
    return text + "\n"


def _entries(label: str, lines: list) -> list:
    """Group frontmatter lines into [key, raw, continuation, is_block] entries.

    A key at column 0 opens an entry and every line indented under it belongs
    to that entry. Grouping rather than rejecting is what lets block scalars,
    sequences and nested mappings through: YAML accepts all three, so a parser
    that errors on them fails frontmatter that loads perfectly at runtime.
    """
    entries = []
    for line in lines:
        stripped = line.strip()
        in_block = bool(entries) and entries[-1][3]
        if not stripped:
            # Blank lines are content inside a block scalar and separators
            # everywhere else; _value() drops the ones that turn out to be
            # separators.
            if entries:
                entries[-1][2].append(line)
            continue
        if not in_block:
            indent = line[: len(line) - len(line.lstrip())]
            if "\t" in indent:
                error(f"{label}: frontmatter line is indented with a tab, which YAML forbids")
                continue
            if stripped.startswith("#"):
                continue
        match = FIELD_PATTERN.match(line)
        if match and not in_block:
            raw = match.group(2)
            entries.append([match.group(1), raw, [], bool(BLOCK_SCALAR.match(raw.strip()))])
            continue
        if entries and (line[:1].isspace() or stripped[:1] == "-"):
            entries[-1][2].append(line)
            continue
        error(f"{label}: frontmatter line is not 'key: value': {stripped[:60]!r}")
    return entries


def _value(label: str, key: str, raw: str, continuation: list, is_block: bool):
    """Resolve one entry to the value YAML would produce for it."""
    if is_block:
        return _block_scalar(BLOCK_SCALAR.match(raw.strip()), continuation)

    body = list(continuation)
    while body and not body[-1].strip():
        body.pop()
    if not body:
        return _parse_scalar(label, key, raw)
    if raw.strip():
        # A scalar continued on the following lines, plain or quoted alike.
        return _parse_scalar(label, key, _fold([raw.strip()] + [c.strip() for c in body]))

    indent = min(len(c) - len(c.lstrip()) for c in body if c.strip())
    body = [c[indent:] if c.strip() else "" for c in body]
    if all(line == "-" or line.startswith("- ") for line in body if line):
        # Sequence items are kept as written: nothing downstream reads a
        # sequence, and scalar-checking an item that is itself a mapping
        # ("- name: x") would report an error YAML does not have.
        return [line[1:].strip() for line in body if line]
    return _fields(label, body)


def _fields(label: str, lines: list) -> dict:
    fields = {}
    for key, raw, continuation, is_block in _entries(label, lines):
        if key in fields:
            error(f"{label}: duplicate frontmatter key '{key}'")
        fields[key] = _value(label, key, raw, continuation, is_block)
    return fields


def parse_frontmatter(path: Path) -> dict:
    """Parse the YAML frontmatter between --- markers.

    Not a full YAML parser, but it accepts what a real YAML parser accepts and
    rejects what it rejects, so a file that passes here also loads at runtime.

    Cached: several checks read the same file, and without caching a single
    malformed file would be reported once per caller.
    """
    if path in _frontmatter_cache:
        return _frontmatter_cache[path]

    fields = {}
    label = str(path.relative_to(REPO))
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        error(f"{label}: missing frontmatter opening '---'")
    else:
        body, closed = [], False
        for line in lines[1:]:
            if line.strip() == "---":
                closed = True
                break
            body.append(line)
        if not closed:
            error(f"{label}: frontmatter never closed with '---'")
        fields = _fields(label, body)

    _frontmatter_cache[path] = fields
    return fields


def scalar(label: str, fields: dict, key: str) -> str:
    """One frontmatter scalar, or "" when it is absent.

    A key that holds a sequence or a mapping is reported here rather than
    reaching a caller that expects text and crashing it.
    """
    value = fields.get(key, "")
    if isinstance(value, str):
        return value
    error(f"{label}: frontmatter '{key}' is a {type(value).__name__}, not a scalar")
    return ""


def skill_markdown(skill_dir: Path = None) -> list:
    """Every markdown file in a skill, or in all of them, recursively.

    Both this module and freshness_table.py walk the tree through here. When
    they walked it separately one stopped at the top level, so a file in a
    subdirectory was listed as missing `last_verified` in the monthly reminder
    issue while CI never asked it for one.
    """
    root = SKILLS_DIR if skill_dir is None else skill_dir
    return sorted(root.rglob("*.md"))


def fenced_blocks(lines: list) -> tuple:
    """Scan a markdown file's code fences once.

    Returns (inside, blocks, unclosed): `inside[i]` is True when line i belongs
    to a fenced code block (fence lines included), `blocks` holds one dict per
    closed block, and `unclosed` is the opening line of a block that never
    closed, or None.

    One scan means the prose view and the code-block view cannot disagree.
    They did when they were two parsers: the block reader closed on any bare
    ``` and only ever opened on ```, so a ```` block containing an inner ```
    was mis-split and every ~~~json block went unvalidated.

    The opening fence's character and length are tracked so an inner ``` inside
    a ```` block does not close it.
    """
    inside = [False] * len(lines)
    blocks = []
    fence = None  # (char, run, start_line, info, content)
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        char = stripped[:1]
        run = len(stripped) - len(stripped.lstrip(char)) if char in ("`", "~") else 0

        if fence is None:
            if run >= 3:
                fence = (char, run, i + 1, stripped[run:].strip(), [])
                inside[i] = True
            continue

        inside[i] = True
        # A closing fence uses the same character, is at least as long, and
        # carries no info string.
        if char == fence[0] and run >= fence[1] and not stripped[run:].strip():
            blocks.append({"line": fence[2], "info": fence[3], "text": "\n".join(fence[4])})
            fence = None
        else:
            fence[4].append(line)

    return inside, blocks, fence[2] if fence else None


def parse_markdown(path: Path) -> dict:
    """Split a markdown file into prose lines and fenced code blocks.

    Cached for the same reason parse_frontmatter is: check_json_blocks and
    check_sync both parse every file, so without caching an unclosed fence was
    reported twice and every file was read and scanned twice.
    """
    if path in _markdown_cache:
        return _markdown_cache[path]

    lines = path.read_text(encoding="utf-8").splitlines()
    inside, blocks, unclosed = fenced_blocks(lines)
    if unclosed is not None:
        error(f"{path.relative_to(REPO)}:{unclosed}: unclosed code fence")

    parsed = {
        "prose": [line for line, fenced in zip(lines, inside) if not fenced],
        "blocks": blocks,
    }
    _markdown_cache[path] = parsed
    return parsed


def check_frontmatter(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        error(f"{skill_dir.relative_to(REPO)}: SKILL.md is missing")
        return
    label = str(skill_md.relative_to(REPO))
    fm = parse_frontmatter(skill_md)
    name = scalar(label, fm, "name")
    if name != skill_dir.name:
        error(
            f"{skill_md.relative_to(REPO)}: frontmatter name '{name}' "
            f"does not match directory '{skill_dir.name}'"
        )
    description = scalar(label, fm, "description")
    if not description:
        error(f"{skill_md.relative_to(REPO)}: frontmatter description is missing")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        # Measured on the parsed value, so surrounding quotes do not count.
        error(
            f"{skill_md.relative_to(REPO)}: description is {len(description)} chars "
            f"(limit {MAX_DESCRIPTION_LENGTH})"
        )


def check_freshness(skill_dir: Path) -> None:
    """Every reference file must declare when its content was last verified."""
    cutoff = datetime.date.today() + FUTURE_TOLERANCE
    for md in skill_markdown(skill_dir):
        label = str(md.relative_to(REPO))
        value = scalar(label, parse_frontmatter(md), "last_verified")
        if not value:
            error(f"{md.relative_to(REPO)}: frontmatter is missing 'last_verified'")
            continue
        if not DATE_PATTERN.match(value):
            error(f"{md.relative_to(REPO)}: last_verified '{value}' is not YYYY-MM-DD")
            continue
        try:
            parsed = datetime.date.fromisoformat(value)
        except ValueError as exc:
            error(f"{md.relative_to(REPO)}: last_verified '{value}' is not a real date ({exc})")
            continue
        if parsed > cutoff:
            error(f"{md.relative_to(REPO)}: last_verified '{value}' is in the future")


def check_json_blocks(skill_dir: Path) -> None:
    for md in skill_markdown(skill_dir):
        for block in parse_markdown(md)["blocks"]:
            if block["info"] != "json":
                continue
            try:
                json.loads(block["text"])
            except json.JSONDecodeError as exc:
                error(f"{md.relative_to(REPO)}:{block['line']}: invalid JSON block: {exc}")


def check_manifests() -> None:
    for manifest in MANIFESTS:
        if not manifest.is_file():
            error(f"{manifest.relative_to(REPO)}: missing")
            continue
        try:
            json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            error(f"{manifest.relative_to(REPO)}: invalid JSON: {exc}")


def check_versions(skill_dirs: list) -> None:
    """Every version must be declared, agree, and have a CHANGELOG section.

    Historically the versions did not agree: v1.2.1 and v1.2.2 shipped with the
    manifests still reading 1.2.0. A *missing* version is checked just as
    strictly, because release.yml only discovers it after the immutable tag has
    been pushed — at which point the fix means deleting and re-pushing the tag.
    """
    declared = {}

    for manifest in MANIFESTS:
        if not manifest.is_file():
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue  # already reported by check_manifests
        label = str(manifest.relative_to(REPO))
        found = False
        if "version" in data:
            declared[label] = data["version"]
            found = True
        for plugin in data.get("plugins", []):
            plugin_label = f"{label}#{plugin.get('name', '?')}"
            if "version" in plugin:
                declared[plugin_label] = plugin["version"]
                found = True
            else:
                error(f"{plugin_label}: plugin declares no 'version'")
        if not found:
            error(f"{label}: declares no 'version'")

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue  # already reported by check_frontmatter
        label = str(skill_md.relative_to(REPO))
        version = scalar(label, parse_frontmatter(skill_md), "version")
        if not version:
            error(f"{skill_md.relative_to(REPO)}: frontmatter is missing 'version'")
            continue
        declared[str(skill_md.relative_to(REPO))] = version

    versions = set(declared.values())
    if len(versions) > 1:
        detail = ", ".join(f"{k}={v}" for k, v in sorted(declared.items()))
        error(f"version mismatch across declarations: {detail}")
        return
    if versions:
        check_changelog(versions.pop())


def check_changelog(version: str) -> None:
    """release.yml hard-fails when the version has no CHANGELOG section."""
    if not CHANGELOG.is_file():
        error(f"{CHANGELOG.name}: missing")
        return
    text = CHANGELOG.read_text(encoding="utf-8")
    if not re.search(rf"^## \[{re.escape(version)}\]", text, re.MULTILINE):
        error(f"{CHANGELOG.name}: no '## [{version}]' section for the declared version")


def structure_signature(path: Path) -> dict:
    parsed = parse_markdown(path)
    sig = {"json_blocks": sum(1 for b in parsed["blocks"] if b["info"] == "json")}
    # Headings are counted outside fenced code blocks only: shell and robots.txt
    # samples contain `# comment` lines that are not document structure.
    for level in range(1, 5):
        prefix = "#" * level + " "
        sig[f"h{level}"] = sum(1 for line in parsed["prose"] if line.startswith(prefix))
    return sig


def check_sync(en_name: str, jp_name: str) -> None:
    en_dir, jp_dir = SKILLS_DIR / en_name, SKILLS_DIR / jp_name
    for skill_dir in (en_dir, jp_dir):
        if not skill_dir.is_dir():
            error(f"{skill_dir.relative_to(REPO)}: skill directory is missing")
            return

    en_files = {p.relative_to(en_dir).as_posix() for p in skill_markdown(en_dir)}
    jp_files = {p.relative_to(jp_dir).as_posix() for p in skill_markdown(jp_dir)}
    if not en_files:
        error(f"{en_name}: no markdown files found")
        return
    for missing in sorted(en_files - jp_files):
        error(f"{jp_name}: missing counterpart of {en_name}/{missing}")
    for extra in sorted(jp_files - en_files):
        error(f"{jp_name}/{extra}: has no counterpart in {en_name}")
    for name in sorted(en_files & jp_files):
        en_sig = structure_signature(en_dir / name)
        jp_sig = structure_signature(jp_dir / name)
        if en_sig != jp_sig:
            error(
                f"structure mismatch in {name}: "
                f"{en_name}={en_sig} vs {jp_name}={jp_sig}"
            )
        en_date = scalar(f"{en_name}/{name}", parse_frontmatter(en_dir / name), "last_verified")
        jp_date = scalar(f"{jp_name}/{name}", parse_frontmatter(jp_dir / name), "last_verified")
        if en_date != jp_date:
            error(
                f"last_verified mismatch in {name}: "
                f"{en_name}={en_date or 'missing'} vs {jp_name}={jp_date or 'missing'}"
            )


def main() -> int:
    if not SKILLS_DIR.is_dir():
        error(f"{SKILLS_DIR.relative_to(REPO)} does not exist")
        return 1

    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())
    if not skill_dirs:
        error("no skill directories found")
    for skill_dir in skill_dirs:
        check_frontmatter(skill_dir)
        check_freshness(skill_dir)
        check_json_blocks(skill_dir)
    check_manifests()
    check_versions(skill_dirs)
    for en_name, jp_name in SYNC_PAIRS:
        check_sync(en_name, jp_name)
    if errors:
        print(f"\n{len(errors)} error(s) found")
        return 1
    print("All checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
