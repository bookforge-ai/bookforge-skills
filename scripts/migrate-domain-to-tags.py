#!/usr/bin/env python3
"""Migrate domain field to tags[0] in all SKILL.md frontmatter files."""

import re
import sys
from pathlib import Path


def migrate_skill_md(path: Path) -> bool:
    """Migrate a single SKILL.md. Returns True if changed."""
    content = path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return False

    end = content.find("\n---", 3)
    if end == -1:
        return False

    frontmatter = content[3:end]
    body = content[end:]

    # Extract domain value
    domain_match = re.search(r"^domain:\s*(.+)$", frontmatter, re.MULTILINE)
    if not domain_match:
        return False

    domain_value = domain_match.group(1).strip().strip("\"'")

    # Extract existing tags
    tags_match = re.search(r"^tags:\s*\[(.+)\]$", frontmatter, re.MULTILINE)
    if tags_match:
        raw_tags = tags_match.group(1)
        existing_tags = [t.strip().strip("\"'") for t in raw_tags.split(",")]
    else:
        existing_tags = []

    # Prepend domain to tags if not already present
    if domain_value not in existing_tags:
        new_tags = [domain_value] + existing_tags
    else:
        existing_tags.remove(domain_value)
        new_tags = [domain_value] + existing_tags

    # Remove domain line
    frontmatter = re.sub(r"^domain:\s*.+\n", "", frontmatter, flags=re.MULTILINE)

    # Replace tags line
    tags_str = ", ".join(new_tags)
    if tags_match:
        frontmatter = re.sub(
            r"^tags:\s*\[.+\]$",
            f"tags: [{tags_str}]",
            frontmatter,
            flags=re.MULTILINE,
        )
    else:
        frontmatter = frontmatter.rstrip() + f"\ntags: [{tags_str}]\n"

    new_content = "---" + frontmatter + body
    path.write_text(new_content, encoding="utf-8")
    return True


def main():
    books_dir = Path(__file__).parent.parent / "books"
    if not books_dir.is_dir():
        print(f"Error: {books_dir} not found", file=sys.stderr)
        sys.exit(1)

    changed = 0
    total = 0

    for skill_md in sorted(books_dir.glob("*/skills/*/SKILL.md")):
        total += 1
        if migrate_skill_md(skill_md):
            changed += 1
            print(f"  Migrated: {skill_md.relative_to(books_dir)}")
        else:
            print(f"  Skipped:  {skill_md.relative_to(books_dir)}")

    print(f"\nDone: {changed}/{total} skills migrated.")


if __name__ == "__main__":
    main()
