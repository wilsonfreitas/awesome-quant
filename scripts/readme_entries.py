"""Shared README entry parsing helpers for awesome-quant."""

from __future__ import annotations

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
