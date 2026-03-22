#!/usr/bin/env python3
"""
Check PyPI projects for last updated dates and update README.md entries.
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple
from urllib.request import urlopen

# PyPI projects to track
PYPI_PROJECTS = {
    "qfrm": "qfrm",
    "chinesestockapi": "chinesestockapi",
    "tushare": "tushare",
    "metatrader5": "MetaTrader5",
}

README_PATH = Path(__file__).parent.parent.parent.parent.parent / "README.md"


def get_pypi_last_updated(package_name: str) -> Optional[str]:
    """
    Fetch the last updated date for a PyPI package.

    Returns: date string in format "YYYY-MM-DD" or None if not found
    """
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        with urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())

        # Get releases (ordered dict, latest first after sorting)
        releases = data.get("releases", {})
        if not releases:
            return None

        # Find the latest release with upload time
        for version in sorted(releases.keys(), reverse=True):
            release_data = releases[version]
            if release_data and len(release_data) > 0:
                upload_time = release_data[0].get("upload_time_iso_8601")
                if upload_time:
                    # Extract just the date part (YYYY-MM-DD)
                    return upload_time.split("T")[0]

        return None
    except Exception as e:
        print(f"  ❌ Error fetching {package_name}: {e}", file=sys.stderr)
        return None


def find_readme_entry(readme_content: str, package_display_name: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Find a README entry for a package.

    Returns: (line_number, match_text) or (None, None)
    """
    # Pattern to match the entry - look for [package_name](pypi.org...)
    pattern = rf"\- \[{re.escape(package_display_name)}\]\(https://pypi\.org/project/\w+/\)[^\n]*"

    for line_num, line in enumerate(readme_content.split("\n"), 1):
        if re.search(pattern, line):
            return line_num, line.strip()

    return None, None


def update_readme_entry(readme_content: str, package_display_name: str, new_date: str) -> Tuple[str, bool]:
    """
    Update or add the last updated date to a README entry.

    Returns: (updated_content, was_changed)
    """
    lines = readme_content.split("\n")
    line_num, entry_text = find_readme_entry(readme_content, package_display_name)

    if line_num is None:
        return readme_content, False

    old_line = lines[line_num - 1]

    # Check if entry already has a date
    existing_date_pattern = r"\(Last updated: \d{4}-\d{2}-\d{2}\)"
    existing_match = re.search(existing_date_pattern, old_line)

    if existing_match:
        old_date = existing_match.group(0)
        new_date_str = f"(Last updated: {new_date})"
        if old_date == new_date_str:
            return readme_content, False  # No change needed
        new_line = old_line.replace(old_date, new_date_str)
    else:
        # Add date to the end of the entry (before period if present)
        if old_line.endswith("."):
            new_line = old_line[:-1] + f" (Last updated: {new_date})."
        else:
            new_line = old_line + f" (Last updated: {new_date})"

    lines[line_num - 1] = new_line
    return "\n".join(lines), True


def main():
    """Check PyPI projects and update README.md."""
    if not README_PATH.exists():
        print(f"❌ README.md not found at {README_PATH}")
        sys.exit(1)

    readme_content = README_PATH.read_text(encoding="utf-8")
    updated_content = readme_content
    changes_made = []

    print("📦 Checking PyPI projects for last updated dates...\n")

    for display_name, pypi_name in PYPI_PROJECTS.items():
        print(f"Checking {display_name}...")

        last_updated = get_pypi_last_updated(pypi_name)
        if last_updated is None:
            print(f"  ⚠️  Could not find last updated date")
            continue

        updated_content, was_changed = update_readme_entry(
            updated_content, display_name, last_updated
        )

        if was_changed:
            print(f"  ✅ Updated to {last_updated}")
            changes_made.append((display_name, last_updated))
        else:
            print(f"  ✓ {last_updated} (no change)")

    print()

    if changes_made:
        print(f"📝 Found {len(changes_made)} update(s):")
        for pkg_name, date in changes_made:
            print(f"  - {pkg_name}: {date}")

        README_PATH.write_text(updated_content, encoding="utf-8")
        print(f"\n✅ Updated {README_PATH.name}")
        return 0
    else:
        print("✓ All packages up to date!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
