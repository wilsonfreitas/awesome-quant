#!/usr/bin/env python3
"""Report awesome-quant entries whose last commit is older than 12 months.

Reads site/projects.csv (produced by parse.py) and prints a markdown report
of entries violating the 12-month activity bar — name, url, last commit, and
days stale — sorted worst-first. Entries with no known date are listed
separately at the end.

Usage:
    python3 scripts/staleness_report.py [path/to/projects.csv]
"""

from __future__ import annotations

import csv
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "site" / "projects.csv"
STALE_DAYS = 365  # the 12-month activity bar


def main() -> int:
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    if not csv_path.exists():
        print(f"ERROR: {csv_path} not found (run parse.py first)", file=sys.stderr)
        return 2

    with csv_path.open("r", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    today = date.today()
    stale: list[tuple[int, dict]] = []
    unknown: list[dict] = []
    for row in rows:
        last_commit = (row.get("last_commit") or "").strip()
        if not last_commit or last_commit == "error":
            # Skip categories that never have dates (commercial etc.) only if
            # there is also no repo/package source to be stale about.
            if row.get("repo") or row.get("cran") == "True" or row.get("pypi") == "True":
                unknown.append(row)
            continue
        try:
            commit_date = datetime.strptime(last_commit, "%Y-%m-%d").date()
        except ValueError:
            unknown.append(row)
            continue
        days = (today - commit_date).days
        if days > STALE_DAYS:
            stale.append((days, row))

    stale.sort(key=lambda item: item[0], reverse=True)

    print("# Staleness report")
    print()
    print(f"Generated {today.isoformat()} from `{csv_path.name}` ({len(rows)} entries).")
    print()
    print(
        f"{len(stale)} entries have no commit in the last {STALE_DAYS} days "
        f"(12-month bar), sorted worst-first."
    )
    print()
    print("| Project | URL | Last commit | Days stale |")
    print("| --- | --- | --- | ---: |")
    for days, row in stale:
        name = row.get("project", "")
        url = row.get("url", "")
        print(f"| {name} | {url} | {row.get('last_commit', '')} | {days} |")

    if unknown:
        print()
        print(f"## No date available ({len(unknown)} entries)")
        print()
        print("Lookup failed or no release date found; check manually.")
        print()
        print("| Project | URL |")
        print("| --- | --- |")
        for row in unknown:
            print(f"| {row.get('project', '')} | {row.get('url', '')} |")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
