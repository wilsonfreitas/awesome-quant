#!/usr/bin/env python3
"""Validate awesome-quant README entries.

Default mode validates the full README and reports legacy duplicate/http URL
issues as warnings. With --diff-from, only added README entry lines are checked
and duplicate/url issues are errors for those additions.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.readme_entries import (
    ENTRY_RE,
    GITHUB_LINK_RE,
    HEADING_RE,
    MARKDOWN_URL_RE,
    NO_LANGUAGE_REQUIRED_SECTIONS,
    VALID_SECTIONS,
    ReadmeEntry,
    extract_languages,
    iter_readme_entries,
)


@dataclass(frozen=True)
class Issue:
    severity: str
    line_number: int
    code: str
    message: str


def normalize_name(name: str) -> str:
    return " ".join(name.casefold().split())


def normalize_url(url: str) -> str:
    return url.strip().rstrip("/").casefold()


def read_added_line_numbers(diff_from: str, readme_path: Path) -> set[int]:
    path_arg = str(readme_path)
    commands = [
        ["git", "diff", "--unified=0", f"{diff_from}...HEAD", "--", path_arg],
        ["git", "diff", "--unified=0", diff_from, "--", path_arg],
    ]
    last_error = ""
    for command in commands:
        proc = subprocess.run(command, text=True, capture_output=True, check=False)
        if proc.returncode == 0:
            return parse_added_lines_from_diff(proc.stdout)
        last_error = proc.stderr.strip()
    raise RuntimeError(f"git diff failed for {diff_from}: {last_error}")


def parse_added_lines_from_diff(diff_text: str) -> set[int]:
    added: set[int] = set()
    new_line: int | None = None

    for line in diff_text.splitlines():
        if line.startswith("@@ "):
            marker = line.split(" ")[2]
            start = marker.split(",", 1)[0].lstrip("+")
            new_line = int(start)
            continue

        if new_line is None:
            continue

        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            added.add(new_line)
            new_line += 1
        elif line.startswith("-"):
            continue
        else:
            new_line += 1

    return added


def build_duplicate_indexes(entries: list[ReadmeEntry]) -> tuple[dict[str, list[ReadmeEntry]], dict[str, list[ReadmeEntry]]]:
    names: dict[str, list[ReadmeEntry]] = defaultdict(list)
    urls: dict[str, list[ReadmeEntry]] = defaultdict(list)
    for entry in entries:
        names[normalize_name(entry.name)].append(entry)
        for url in entry.markdown_urls:
            urls[normalize_url(url)].append(entry)
    return names, urls


def validate_entry(
    entry: ReadmeEntry,
    *,
    duplicate_names: dict[str, list[ReadmeEntry]],
    duplicate_urls: dict[str, list[ReadmeEntry]],
    strict_duplicates: bool,
    strict_urls: bool,
    strict_format: bool,
) -> list[Issue]:
    issues: list[Issue] = []
    line = entry.line_number

    if entry.section not in VALID_SECTIONS:
        issues.append(Issue("error", line, "section", f"entry is under unknown section {entry.section!r}"))

    format_severity = "error" if strict_format else "warning"

    if entry.section not in NO_LANGUAGE_REQUIRED_SECTIONS and not entry.languages:
        issues.append(Issue(format_severity, line, "language", "missing required backtick language tag prefix"))

    if entry.languages:
        _languages, clean_description = extract_languages(entry.tail)
        if clean_description == entry.tail:
            issues.append(Issue(format_severity, line, "language", "language tags must be followed by ' - '"))

    github_label_count = entry.description.count("[GitHub](")
    if github_label_count and not GITHUB_LINK_RE.search(entry.description):
        issues.append(Issue(format_severity, line, "github-link", "optional GitHub link must use [GitHub](https://github.com/owner/repo)"))

    github_match = GITHUB_LINK_RE.search(entry.description)
    description_to_check = entry.description[: github_match.start()].rstrip() if github_match else entry.description.rstrip()
    # Allow trailing reference links after the sentence, e.g. [GitHub], [Website], or ([Demo](...)).
    previous = None
    while previous != description_to_check:
        previous = description_to_check
        description_to_check = re.sub(r"\s*\[[^\]]+\]\([^)]+\)\s*$", "", description_to_check).rstrip()
        description_to_check = re.sub(r"\s*\(\[[^\]]+\]\([^)]+\)\)\s*$", "", description_to_check).rstrip()
    if description_to_check and not description_to_check.endswith("."):
        issues.append(Issue(format_severity, line, "period", "description must end with a period before optional trailing link"))

    for url in entry.markdown_urls:
        if not url.startswith("https://"):
            severity = "error" if strict_urls else "warning"
            issues.append(Issue(severity, line, "url", f"URL should use https://: {url}"))

    duplicate_name_entries = [item for item in duplicate_names[normalize_name(entry.name)] if item.line_number != line]
    if duplicate_name_entries:
        severity = "error" if strict_duplicates else "warning"
        lines = ", ".join(str(item.line_number) for item in duplicate_name_entries)
        issues.append(Issue(severity, line, "duplicate-name", f"project name duplicates line(s): {lines}"))

    seen_duplicate_url_lines: set[int] = set()
    for url in entry.markdown_urls:
        duplicate_url_entries = [item for item in duplicate_urls[normalize_url(url)] if item.line_number != line]
        for item in duplicate_url_entries:
            seen_duplicate_url_lines.add(item.line_number)
    if seen_duplicate_url_lines:
        severity = "error" if strict_duplicates else "warning"
        lines = ", ".join(str(line_number) for line_number in sorted(seen_duplicate_url_lines))
        issues.append(Issue(severity, line, "duplicate-url", f"URL duplicates line(s): {lines}"))

    return issues


def validate_malformed_added_lines(readme_path: Path, added_lines: set[int]) -> list[Issue]:
    issues: list[Issue] = []
    lines = readme_path.read_text(encoding="utf-8").splitlines()
    for line_number in sorted(added_lines):
        if line_number < 1 or line_number > len(lines):
            continue
        line = lines[line_number - 1]
        stripped = line.strip()
        if not stripped or HEADING_RE.match(stripped):
            continue
        if stripped.startswith("- ") and not ENTRY_RE.match(line):
            issues.append(Issue("error", line_number, "format", "added README bullet does not match entry regex"))
    return issues


def format_issue(issue: Issue) -> str:
    location = f"line {issue.line_number}" if issue.line_number else "README"
    return f"{issue.severity.upper()} {location} [{issue.code}] {issue.message}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate awesome-quant README entries.")
    parser.add_argument("--readme", default="README.md", help="README path to validate")
    parser.add_argument("--diff-from", help="validate only README lines added relative to this git ref")
    parser.add_argument("--strict-duplicates", action="store_true", help="treat duplicate names/URLs as errors in full validation")
    parser.add_argument("--strict-urls", action="store_true", help="treat non-https URLs as errors in full validation")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    readme_path = Path(args.readme)
    if not readme_path.exists():
        print(f"ERROR README not found: {readme_path}", file=sys.stderr)
        return 2

    entries = list(iter_readme_entries(readme_path))
    duplicate_names, duplicate_urls = build_duplicate_indexes(entries)

    added_lines: set[int] | None = None
    if args.diff_from:
        try:
            added_lines = read_added_line_numbers(args.diff_from, readme_path)
        except RuntimeError as exc:
            print(f"ERROR {exc}", file=sys.stderr)
            return 2
        selected_entries = [entry for entry in entries if entry.line_number in added_lines]
        strict_duplicates = True
        strict_urls = True
        strict_format = True
    else:
        selected_entries = entries
        strict_duplicates = args.strict_duplicates
        strict_urls = args.strict_urls
        strict_format = False

    issues: list[Issue] = []
    if added_lines is not None:
        issues.extend(validate_malformed_added_lines(readme_path, added_lines))

    for entry in selected_entries:
        issues.extend(
            validate_entry(
                entry,
                duplicate_names=duplicate_names,
                duplicate_urls=duplicate_urls,
                strict_duplicates=strict_duplicates,
                strict_urls=strict_urls,
                strict_format=strict_format,
            )
        )

    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]

    scope = f"added README lines relative to {args.diff_from}" if args.diff_from else "full README"
    print(f"Validated {len(selected_entries)} entries in {scope}.")
    for issue in sorted(issues, key=lambda item: (item.line_number, item.severity, item.code)):
        print(format_issue(issue))

    if errors:
        print(f"Validation failed: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    if warnings:
        print(f"Validation passed with {len(warnings)} warning(s).")
    else:
        print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
