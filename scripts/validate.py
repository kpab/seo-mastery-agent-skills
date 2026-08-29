#!/usr/bin/env python3
"""Repository validation for CI.

Checks:
1. Every skill has a SKILL.md with valid frontmatter (name matches the
   directory, description present and within length limits).
2. Every markdown file in a skill carries a `last_verified: YYYY-MM-DD`
   frontmatter field that is a real date and is not in the future.
3. Every ```json code block in skill markdown files parses as JSON.
4. marketplace manifests are valid JSON.
5. Every declared version agrees: both marketplace manifests and every
   SKILL.md frontmatter.
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
SYNC_PAIRS = [("seo-mastery", "seo-mastery-jp")]
MAX_DESCRIPTION_LENGTH = 1024
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FIELD_PATTERN = re.compile(r"^(\w[\w-]*):\s*(.*)$")

# CI runs in UTC while contributors may be ahead of it, so a file stamped with
# "today" in JST looks like tomorrow to the runner. One day of slack keeps that
# from failing a build that is actually correct.
FUTURE_TOLERANCE = datetime.timedelta(days=1)

errors = []
_frontmatter_cache = {}


def error(msg: str) -> None:
    errors.append(msg)
    print(f"ERROR: {msg}")


def parse_frontmatter(path: Path) -> dict:
    """Parse simple `key: value` frontmatter between --- markers.

    Cached: several checks read the same file, and without caching a single
    malformed file would be reported once per caller.
    """
    if path in _frontmatter_cache:
        return _frontmatter_cache[path]

    fields = {}
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        error(f"{path.relative_to(REPO)}: missing frontmatter opening '---'")
    else:
        closed = False
        for line in lines[1:]:
            if line.strip() == "---":
                closed = True
                break
            match = FIELD_PATTERN.match(line)
            if match:
                fields[match.group(1)] = match.group(2).strip()
        if not closed:
            error(f"{path.relative_to(REPO)}: frontmatter never closed with '---'")

    _frontmatter_cache[path] = fields
    return fields


def fenced_regions(lines: list) -> list:
    """Return a bool per line: True if the line is inside a fenced code block.

    Tracks the opening fence's character and length so an inner ``` inside a
    ```` block does not close it, and so an indented fence is matched by its
    own closing fence rather than by the next unrelated one.
    """
    inside = [False] * len(lines)
    fence = None  # (char, length, indent)
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        char = stripped[:1]
        if char in ("`", "~"):
            run = len(stripped) - len(stripped.lstrip(char))
        else:
            run = 0

        if fence is None:
            if run >= 3:
                fence = (char, run)
                inside[i] = True
            continue

        inside[i] = True
        # A closing fence uses the same character, is at least as long, and
        # carries no info string.
        if char == fence[0] and run >= fence[1] and not stripped[run:].strip():
            fence = None
    return inside


def parse_markdown(path: Path) -> dict:
    """Split a markdown file into prose lines and fenced code blocks."""
    lines = path.read_text(encoding="utf-8").splitlines()
    inside = fenced_regions(lines)

    prose = [line for line, fenced in zip(lines, inside) if not fenced]

    blocks, current, start, info = [], None, 0, ""
    for i, (line, fenced) in enumerate(zip(lines, inside), 1):
        stripped = line.strip()
        if current is None:
            if fenced and stripped.startswith("```"):
                current, start, info = [], i, stripped[3:].strip()
            continue
        if stripped == "```":
            blocks.append({"line": start, "info": info, "text": "\n".join(current)})
            current = None
        else:
            current.append(line)
    if current is not None:
        error(f"{path.relative_to(REPO)}:{start}: unclosed ``` block")

    return {"prose": prose, "blocks": blocks}


def check_frontmatter(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        error(f"{skill_dir.relative_to(REPO)}: SKILL.md is missing")
        return
    fm = parse_frontmatter(skill_md)
    name = fm.get("name", "")
    if name != skill_dir.name:
        error(
            f"{skill_md.relative_to(REPO)}: frontmatter name '{name}' "
            f"does not match directory '{skill_dir.name}'"
        )
    description = fm.get("description", "")
    if not description:
        error(f"{skill_md.relative_to(REPO)}: frontmatter description is missing")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        error(
            f"{skill_md.relative_to(REPO)}: description is {len(description)} chars "
            f"(limit {MAX_DESCRIPTION_LENGTH})"
        )


def check_freshness(skill_dir: Path) -> None:
    """Every reference file must declare when its content was last verified."""
    cutoff = datetime.date.today() + FUTURE_TOLERANCE
    for md in sorted(skill_dir.glob("*.md")):
        value = parse_frontmatter(md).get("last_verified", "")
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
    for md in sorted(skill_dir.glob("*.md")):
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
    """All declared versions must agree.

    Historically they did not: v1.2.1 and v1.2.2 shipped with the manifests
    still reading 1.2.0. Checking here (rather than only in the release
    workflow) catches the drift at pull-request time.
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
        if "version" in data:
            declared[label] = data["version"]
        for plugin in data.get("plugins", []):
            if "version" in plugin:
                declared[f"{label}#{plugin.get('name', '?')}"] = plugin["version"]

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if skill_md.is_file():
            version = parse_frontmatter(skill_md).get("version")
            if version:
                declared[str(skill_md.relative_to(REPO))] = version

    if len(set(declared.values())) > 1:
        detail = ", ".join(f"{k}={v}" for k, v in sorted(declared.items()))
        error(f"version mismatch across declarations: {detail}")


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

    en_files = {p.name for p in en_dir.glob("*.md")}
    jp_files = {p.name for p in jp_dir.glob("*.md")}
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
        en_date = parse_frontmatter(en_dir / name).get("last_verified", "")
        jp_date = parse_frontmatter(jp_dir / name).get("last_verified", "")
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
