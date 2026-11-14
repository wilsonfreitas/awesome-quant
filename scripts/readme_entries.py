"""Shared README entry parsing helpers for awesome-quant."""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ENTRY_RE = re.compile(r"^\s*- \[(.*)\]\((.*)\) - (.*)$")
HEADING_RE = re.compile(r"^(#+) (.*)$")
BADGE_RE = re.compile(r"\s*!\[[^\]]*\]\([^)]*\)\s*")
LANGUAGE_PREFIX_RE = re.compile(r"^((?:`[^`]+`\s*)+)-\s*(.*)$")
GITHUB_LINK_RE = re.compile(r"\[GitHub\]\((https://github\.com/[\w-]+/[-\w.]+)\)")
MARKDOWN_URL_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
AUTOLINK_URL_RE = re.compile(r"<(https?://[^>\s]+)>")
HISTORICAL_SECTION = "Historical & Archived Projects"
HISTORICAL_TAG = "Historical"

NO_LANGUAGE_REQUIRED_SECTIONS = {
    "Commercial & Proprietary Services",
    "Cross-Language Frameworks",
    "Reproducing Works, Training & Books",
    "Related Lists",
}

VALID_SECTIONS = [
    "Numerical Libraries & Data Structures",
    "Financial Instruments & Pricing",
    "Technical Indicators",
    "Trading & Backtesting",
    "Portfolio Optimization & Risk Analysis",
    "Factor Analysis",
    "Sentiment Analysis & Alternative Data",
    "Time Series Analysis",
    "Market Data & Data Sources",
    "Prediction Markets",
    "Calendars & Market Hours",
    "Visualization",
    "Excel & Spreadsheet Integration",
    "Quant Research Environments",
    "Cross-Language Frameworks",
    "Reproducing Works, Training & Books",
    "Commercial & Proprietary Services",
    HISTORICAL_SECTION,
    "Related Lists",
]


@dataclass(frozen=True)
class ReadmeEntry:
    line_number: int
    raw_line: str
    section: str
    name: str
    url: str
    tail: str
    languages: list[str]
    description: str

    @property
    def markdown_urls(self) -> list[str]:
        return MARKDOWN_URL_RE.findall(self.raw_line)

    @property
    def external_urls(self) -> list[str]:
        matches = [
            (match.start(), match.group(1))
            for pattern in (MARKDOWN_URL_RE, AUTOLINK_URL_RE)
            for match in pattern.finditer(self.raw_line)
        ]
        urls = [url for _, url in sorted(matches)]
        return list(dict.fromkeys(urls))

    @property
    def github_url(self) -> str:
        if "github.com" in self.url:
            return self.url
        match = GITHUB_LINK_RE.search(self.description)
        return match.group(1) if match else ""


def slugify(text: str) -> str:
    """Convert text to lowercase hyphen-separated slug."""
    text = text.lower().strip()
    text = re.sub(r"[&/]+", "-", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def extract_languages(description: str) -> tuple[list[str], str]:
    """Extract leading backtick language tags from an entry description."""
    match = LANGUAGE_PREFIX_RE.match(description)
    if not match:
        return [], description
    lang_str = match.group(1)
    clean_description = match.group(2)
    return re.findall(r"`([^`]+)`", lang_str), clean_description


def iter_readme_entries(path: str | Path) -> Iterable[ReadmeEntry]:
    """Yield parsed README entries with line numbers and current h2 section."""
    current_section = ""
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, 1):
            line = BADGE_RE.sub(" ", raw_line.rstrip("\n"))
            heading = HEADING_RE.match(line)
            if heading:
                level, title = heading.groups()
                if len(level) == 2 and title.strip() != "Contents":
                    current_section = title.strip()
                continue

            match = ENTRY_RE.match(line)
            if not match:
                continue

            tail = match.group(3).strip()
            languages, description = extract_languages(tail)
            yield ReadmeEntry(
                line_number=line_number,
                raw_line=raw_line.rstrip("\n"),
                section=current_section,
                name=match.group(1).strip(),
                url=match.group(2).strip(),
                tail=tail,
                languages=languages,
                description=description.strip(),
            )


def nested_reference_repairs(base: str, head: str) -> list[tuple[int, int, str, str]]:
    """Find existing nested references with only one repository URL changed.

    Results contain zero-based old/new line indexes and URLs. This checks
    structure only; the authenticated reviewer must verify repository identity.
    """
    before, after = base.splitlines(), head.splitlines()

    def contexts(lines: list[str]) -> list[tuple[str, int | None]]:
        section = ""
        parent = None
        result = []
        for index, line in enumerate(lines):
            if line.startswith("## "):
                section, parent = line, None
            elif line.startswith("- "):
                parent = index if ENTRY_RE.match(line) else None
            result.append((section, parent))
        return result

    old_context, new_context = contexts(before), contexts(after)
    operations = difflib.SequenceMatcher(
        a=before, b=after, autojunk=False
    ).get_opcodes()
    unchanged_lines = {
        old: new
        for operation, a, b, c, d in operations if operation == "equal"
        for old, new in zip(range(a, b), range(c, d))
    }
    repairs = []
    repository_url = re.compile(
        r"https://github\.com/[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+/?"
    )
    for operation, a, b, c, d in operations:
        if operation != "replace" or b - a != d - c:
            continue
        for old_index, new_index in zip(range(a, b), range(c, d)):
            old, new = before[old_index], after[new_index]
            if not re.match(r"^[ \t]+- ", new) or ENTRY_RE.match(new):
                continue
            old_section, old_parent = old_context[old_index]
            new_section, new_parent = new_context[new_index]
            if (ENTRY_RE.match(old) or not old_section or old_section != new_section
                    or old_parent is None or new_parent is None):
                continue
            # Anchor to the same unchanged parent occurrence, not merely its text.
            # A URL repair cannot change the reference's position below that parent.
            if (unchanged_lines.get(old_parent) != new_parent
                    or old_index - old_parent != new_index - new_parent):
                continue
            old_links = list(MARKDOWN_URL_RE.finditer(old))
            new_links = list(MARKDOWN_URL_RE.finditer(new))
            if len(old_links) != len(new_links):
                continue
            changed = [
                (a, b) for a, b in zip(old_links, new_links)
                if a.group(1) != b.group(1)
            ]
            if len(changed) != 1:
                continue
            old_link, new_link = changed[0]
            old_url, new_url = old_link.group(1), new_link.group(1)
            if not all(repository_url.fullmatch(url) for url in (old_url, new_url)):
                continue
            if (old[:old_link.start(1)], old[old_link.end(1):]) != (
                new[:new_link.start(1)], new[new_link.end(1):]
            ):
                continue
            repairs.append((old_index, new_index, old_url, new_url))
    return repairs
