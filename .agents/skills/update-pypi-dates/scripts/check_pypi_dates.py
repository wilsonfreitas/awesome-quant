#!/usr/bin/env python3
"""Check tracked PyPI projects and update README.md last-updated notes."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.request import urlopen

PYPI_PROJECTS = {
    "qfrm": "qfrm",
    "chinesestockapi": "chinesestockapi",
    "tushare": "tushare",
    "metatrader5": "MetaTrader5",
}

README_PATH = Path(__file__).resolve().parents[4] / "README.md"


def get_pypi_last_updated(package_name: str) -> str | None:
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        with urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        print(f"ERROR fetching {package_name}: {exc}", file=sys.stderr)
        return None

    releases = data.get("releases", {})
    for version in sorted(releases.keys(), reverse=True):
        files = releases[version]
        if not files:
            continue
        upload_time = files[0].get("upload_time_iso_8601")
        if upload_time:
            return upload_time.split("T", 1)[0]
    return None


def find_readme_entry(readme_content: str, display_name: str) -> tuple[int | None, str | None]:
    pattern = rf"- \[{re.escape(display_name)}\]\(https://pypi\.org/project/[\w.-]+/\)[^\n]*"
    for line_num, line in enumerate(readme_content.splitlines(), 1):
        if re.search(pattern, line):
            return line_num, line
    return None, None


def update_readme_entry(readme_content: str, display_name: str, new_date: str) -> tuple[str, bool]:
    lines = readme_content.splitlines()
    line_num, entry = find_readme_entry(readme_content, display_name)
    if line_num is None or entry is None:
        print(f"WARN {display_name}: README entry not found")
        return readme_content, False

    old_line = lines[line_num - 1]
    new_date_text = f"(Last updated: {new_date})"
    existing_date_pattern = r"\(Last updated: \d{4}-\d{2}-\d{2}\)"

    if re.search(existing_date_pattern, old_line):
        new_line = re.sub(existing_date_pattern, new_date_text, old_line)
    elif old_line.endswith("."):
        new_line = old_line[:-1] + f" {new_date_text}."
    else:
        new_line = old_line + f" {new_date_text}"

    if new_line == old_line:
        return readme_content, False

    lines[line_num - 1] = new_line
    trailing_newline = "\n" if readme_content.endswith("\n") else ""
    return "\n".join(lines) + trailing_newline, True


def main() -> int:
    if not README_PATH.exists():
        print(f"ERROR README.md not found at {README_PATH}", file=sys.stderr)
        return 1

    readme_content = README_PATH.read_text(encoding="utf-8")
    updated_content = readme_content
    changes: list[tuple[str, str]] = []

    print("Checking PyPI projects for last-updated dates...")
    for display_name, package_name in PYPI_PROJECTS.items():
        last_updated = get_pypi_last_updated(package_name)
        if last_updated is None:
            print(f"{display_name}: skipped")
            continue

        updated_content, changed = update_readme_entry(updated_content, display_name, last_updated)
        if changed:
            changes.append((display_name, last_updated))
            print(f"{display_name}: updated to {last_updated}")
        else:
            print(f"{display_name}: {last_updated} (no change)")

    if changes:
        README_PATH.write_text(updated_content, encoding="utf-8")
        print("Updated README.md:")
        for name, date in changes:
            print(f"- {name}: {date}")
    else:
        print("All tracked PyPI dates are current.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
