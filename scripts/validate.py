#!/usr/bin/env python3
"""Repository validation for CI.

Checks:
1. Every skill has a SKILL.md with valid frontmatter (name matches the
   directory, description present and within length limits).
2. Every markdown file in a skill carries a `last_verified: YYYY-MM-DD`
   frontmatter field, and it is not dated in the future.
3. Every ```json code block in skill markdown files parses as JSON.
4. marketplace manifests are valid JSON.
5. The EN and JP skills stay structurally in sync (same file list, same
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
SYNC_PAIRS = [("seo-mastery", "seo-mastery-jp")]
MAX_DESCRIPTION_LENGTH = 1024
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FENCE_PATTERN = re.compile(r"^```.*?^```", flags=re.M | re.S)

errors = []


def error(msg: str) -> None:
    errors.append(msg)
    print(f"ERROR: {msg}")


def parse_frontmatter(path: Path) -> dict:
    """Parse simple `key: value` frontmatter between --- markers."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        error(f"{path.relative_to(REPO)}: missing frontmatter opening '---'")
        return {}
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        match = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    error(f"{path.relative_to(REPO)}: frontmatter never closed with '---'")
    return fields


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
    today = datetime.date.today()
    for md in sorted(skill_dir.glob("*.md")):
        value = parse_frontmatter(md).get("last_verified", "")
        if not value:
            error(f"{md.relative_to(REPO)}: frontmatter is missing 'last_verified'")
            continue
        if not DATE_PATTERN.match(value):
            error(
                f"{md.relative_to(REPO)}: last_verified '{value}' is not YYYY-MM-DD"
            )
            continue
        if datetime.date.fromisoformat(value) > today:
            error(f"{md.relative_to(REPO)}: last_verified '{value}' is in the future")


def json_blocks(path: Path) -> list:
    """Return (line_number, text) for each top-level ```json code block."""
    blocks = []
    lines = path.read_text(encoding="utf-8").splitlines()
    current, start = None, 0
    for i, line in enumerate(lines, 1):
        if current is None:
            if line.strip() == "```json":
                current, start = [], i
        elif line.strip() == "```":
            blocks.append((start, "\n".join(current)))
            current = None
        else:
            current.append(line)
    if current is not None:
        error(f"{path.relative_to(REPO)}:{start}: unclosed ```json block")
    return blocks


def check_json_blocks(skill_dir: Path) -> None:
    for md in sorted(skill_dir.glob("*.md")):
        for line_no, text in json_blocks(md):
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                error(f"{md.relative_to(REPO)}:{line_no}: invalid JSON block: {exc}")


def check_manifests() -> None:
    for manifest in [REPO / "marketplace.json", REPO / ".claude-plugin" / "marketplace.json"]:
        if not manifest.is_file():
            continue
        try:
            json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            error(f"{manifest.relative_to(REPO)}: invalid JSON: {exc}")


def structure_signature(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    sig = {"json_blocks": len(re.findall(r"^```json\s*$", text, flags=re.M))}
    # Headings are counted outside fenced code blocks only: shell/robots.txt
    # samples contain `# comment` lines that are not document structure.
    prose = FENCE_PATTERN.sub("", text)
    for level in range(1, 5):
        pattern = rf"^{'#' * level} "
        sig[f"h{level}"] = len(re.findall(pattern, prose, flags=re.M))
    return sig


def check_sync(en_name: str, jp_name: str) -> None:
    en_dir, jp_dir = SKILLS_DIR / en_name, SKILLS_DIR / jp_name
    en_files = {p.name for p in en_dir.glob("*.md")}
    jp_files = {p.name for p in jp_dir.glob("*.md")}
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
    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())
    if not skill_dirs:
        error("no skill directories found")
    for skill_dir in skill_dirs:
        check_frontmatter(skill_dir)
        check_freshness(skill_dir)
        check_json_blocks(skill_dir)
    check_manifests()
    for en_name, jp_name in SYNC_PAIRS:
        check_sync(en_name, jp_name)
    if errors:
        print(f"\n{len(errors)} error(s) found")
        return 1
    print("All checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
