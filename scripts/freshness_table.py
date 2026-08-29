#!/usr/bin/env python3
"""Print a markdown table of every skill file's `last_verified` date.

Used by .github/workflows/freshness-reminder.yml. It reuses validate.py's
frontmatter parser instead of re-implementing one in sed/grep: the shell
version read only the first 10 lines and split on a single space, so a
well-formed field could be reported as missing in the reminder issue.

Stdlib only — no dependencies.
"""

import contextlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate import REPO, SKILLS_DIR, parse_frontmatter  # noqa: E402


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"{SKILLS_DIR} does not exist", file=sys.stderr)
        return 1

    print("| File | last_verified |")
    print("|------|---------------|")
    for md in sorted(SKILLS_DIR.rglob("*.md")):
        # Frontmatter complaints belong on stderr; stdout is the table itself.
        with contextlib.redirect_stdout(sys.stderr):
            value = parse_frontmatter(md).get("last_verified", "")
        print(f"| `{md.relative_to(REPO)}` | {value or '**missing**'} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
