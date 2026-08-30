#!/usr/bin/env python3
"""Print a markdown table of every skill file's `last_verified` date.

Used by .github/workflows/freshness-reminder.yml. It reuses validate.py's
frontmatter parser and its file walk instead of re-implementing either: the
shell version read only the first 10 lines and split on a single space, so a
well-formed field could be reported as missing in the reminder issue, and a
second walk would have listed files CI never checks.

Stdlib only — no dependencies.
"""

import contextlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate import (  # noqa: E402
    REPO,
    SKILLS_DIR,
    errors,
    parse_frontmatter,
    scalar,
    skill_markdown,
)


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"{SKILLS_DIR} does not exist", file=sys.stderr)
        return 1

    print("| File | last_verified |")
    print("|------|---------------|")
    for md in skill_markdown():
        label = str(md.relative_to(REPO))
        # Frontmatter complaints belong on stderr; stdout is the table itself.
        with contextlib.redirect_stdout(sys.stderr):
            value = scalar(label, parse_frontmatter(md), "last_verified")
        print(f"| `{label}` | {value or '**missing**'} |")

    # Without this the table renders "**missing**" for a file whose frontmatter
    # is malformed and the step still passes green.
    if errors:
        print(f"{len(errors)} frontmatter error(s); see above", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
