#!/usr/bin/env python3
"""Migrate README.md from language-first to category-first organization.

Reads the current README.md, classifies entries into new category sections,
adds inline language tags, deduplicates, and writes the result.
"""

import re
from pathlib import Path

# --- Configuration ---

# Map (old_language, old_category) → new_section
# Empty old_category means the language section had no subsections (flat list)
SECTION_MAP = {
    # Python
    ("Python", "Numerical Libraries & Data Structures"): "Numerical Libraries & Data Structures",
    ("Python", "Financial Instruments and Pricing"): "Financial Instruments & Pricing",
    ("Python", "Indicators"): "Technical Indicators",
    ("Python", "Trading & Backtesting"): "Trading & Backtesting",
    ("Python", "Risk Analysis"): "Portfolio Optimization & Risk Analysis",
    ("Python", "Factor Analysis"): "Factor Analysis",
    ("Python", "Sentiment Analysis"): "Sentiment Analysis & Alternative Data",
    ("Python", "Quant Research Environment"): "Quant Research Environments",
    ("Python", "Time Series"): "Time Series Analysis",
    ("Python", "Calendars"): "Calendars & Market Hours",
    ("Python", "Data Sources"): "Market Data & Data Sources",
    ("Python", "Excel Integration"): "Excel & Spreadsheet Integration",
    ("Python", "Visualization"): "Visualization",
    # R
    ("R", "Numerical Libraries & Data Structures"): "Numerical Libraries & Data Structures",
    ("R", "Data Sources"): "Market Data & Data Sources",
    ("R", "Financial Instruments and Pricing"): "Financial Instruments & Pricing",
    ("R", "Trading"): "Trading & Backtesting",
    ("R", "Backtesting"): "Trading & Backtesting",
    ("R", "Risk Analysis"): "Portfolio Optimization & Risk Analysis",
    ("R", "Factor Analysis"): "Factor Analysis",
    ("R", "Time Series"): "Time Series Analysis",
    ("R", "Calendars"): "Calendars & Market Hours",
    # Matlab
    ("Matlab", "Alternatives"): "Cross-Language Frameworks",
    ("Matlab", "FrameWorks"): "Trading & Backtesting",
    # Julia (flat)
    ("Julia", ""): "CLASSIFY_JULIA",
    # Java (flat)
    ("Java", ""): "Financial Instruments & Pricing",
    # JavaScript (flat + subcategory)
    ("JavaScript", ""): "CLASSIFY_JS",
    ("JavaScript", "Data Visualization"): "Visualization",
    # Haskell
    ("Haskell", ""): "Financial Instruments & Pricing",
    # Scala
    ("Scala", ""): "Financial Instruments & Pricing",
    # Ruby
    ("Ruby", ""): "Trading & Backtesting",
    # Elixir/Erlang
    ("Elixir/Erlang", ""): "Trading & Backtesting",
    # Golang
    ("Golang", ""): "CLASSIFY_GO",
    # CPP
    ("CPP", ""): "CLASSIFY_CPP",
    # CSharp
    ("CSharp", ""): "Trading & Backtesting",
    # Rust
    ("Rust", ""): "CLASSIFY_RUST",
    # Frameworks
    ("Frameworks", ""): "Cross-Language Frameworks",
    # Reproducing Works
    ("Reproducing Works, Training & Books", ""): "Reproducing Works, Training & Books",
    # Commercial
    ("Commercial & Proprietary Services", ""): "Commercial & Proprietary Services",
    # Related
    ("Related Lists", ""): "Related Lists",
}

# Per-project overrides for misplaced entries or entries in flat sections
# that need manual classification.
# Key = (project_name, old_language) to avoid collisions between same-named
# projects in different sections (e.g., TA-Lib in Python vs Frameworks).
PROJECT_OVERRIDES = {
    # Misplaced: should be Portfolio Optimization & Risk
    ("PyPortfolioOpt", "Python"): "Portfolio Optimization & Risk Analysis",
    ("skfolio", "Python"): "Portfolio Optimization & Risk Analysis",
    ("riskparity.py", "Python"): "Portfolio Optimization & Risk Analysis",
    ("DeepDow", "Python"): "Portfolio Optimization & Risk Analysis",
    ("Eiten", "Python"): "Portfolio Optimization & Risk Analysis",
    ("mlfinlab", "Python"): "Portfolio Optimization & Risk Analysis",
    # Misplaced: should be Technical Indicators
    ("bta-lib", "Python"): "Technical Indicators",
    ("ta", "Python"): "Technical Indicators",
    ("TuneTA", "Python"): "Technical Indicators",
    ("TA-Lib", "Python"): "Technical Indicators",  # Python wrapper → Indicators
    # Note: ("TA-Lib", "Frameworks") is NOT overridden — stays in Cross-Language Frameworks
    # Misplaced: should be Market Data
    ("OpenBB Terminal", "Python"): "Market Data & Data Sources",
    ("Fincept Terminal", "Python"): "Market Data & Data Sources",
    # Prediction Markets
    ("pmxt", "Python"): "Prediction Markets",
    ("pmxt", "JavaScript"): "Prediction Markets",
    ("Polymarket Scanner API", "Python"): "Prediction Markets",
    ("polymarket-whales", "Python"): "Prediction Markets",
    ("SimpleFunctions", "JavaScript"): "Prediction Markets",
    ("Parsec", "Commercial & Proprietary Services"): "Commercial & Proprietary Services",  # Keep commercial
    ("Telonex", "Commercial & Proprietary Services"): "Commercial & Proprietary Services",  # Keep commercial
    # Julia classification
    ("QuantLib.jl", "Julia"): "Financial Instruments & Pricing",
    ("Miletus.jl", "Julia"): "Financial Instruments & Pricing",
    ("Ito.jl", "Julia"): "Financial Instruments & Pricing",
    ("Fastback.jl", "Julia"): "Trading & Backtesting",
    ("Lucky.jl", "Julia"): "Trading & Backtesting",
    ("Strategems.jl", "Julia"): "Trading & Backtesting",
    ("TALib.jl", "Julia"): "Technical Indicators",
    ("Indicators.jl", "Julia"): "Technical Indicators",
    ("OnlineTechnicalIndicators.jl", "Julia"): "Technical Indicators",
    ("TechnicalIndicatorCharts.jl", "Julia"): "Technical Indicators",
    ("MarketTechnicals.jl", "Julia"): "Technical Indicators",
    ("LightweightCharts.jl", "Julia"): "Visualization",
    ("MarketData.jl", "Julia"): "Market Data & Data Sources",
    ("CryptoExchangeAPIs.jl", "Julia"): "Market Data & Data Sources",
    ("CcyConv.jl", "Julia"): "Market Data & Data Sources",
    ("TimeSeries.jl", "Julia"): "Time Series Analysis",
    ("Temporal.jl", "Julia"): "Numerical Libraries & Data Structures",
    ("DataFrames.jl", "Julia"): "Numerical Libraries & Data Structures",
    ("TSFrames.jl", "Julia"): "Numerical Libraries & Data Structures",
    ("TimeArrays.jl", "Julia"): "Numerical Libraries & Data Structures",
    ("TimeFrames.jl", "Julia"): "Time Series Analysis",
    ("OnlinePortfolioAnalytics.jl", "Julia"): "Portfolio Optimization & Risk Analysis",
    ("RiskPerf.jl", "Julia"): "Portfolio Optimization & Risk Analysis",
    ("OnlineResamplers.jl", "Julia"): "Market Data & Data Sources",
    # Java classification
    ("ta4j", "Java"): "Technical Indicators",
    # Golang classification
    ("Kelp", "Golang"): "Trading & Backtesting",
    ("marketstore", "Golang"): "Market Data & Data Sources",
    ("IndicatorGo", "Golang"): "Technical Indicators",
    # CPP classification
    ("QuantLib", "CPP"): "Cross-Language Frameworks",
    ("QuantLibRisks", "CPP"): "Cross-Language Frameworks",
    ("XAD", "CPP"): "Cross-Language Frameworks",
    ("TradeFrame", "CPP"): "Trading & Backtesting",
    ("Hikyuu", "CPP"): "Trading & Backtesting",
    ("PandoraTrader", "CPP"): "Trading & Backtesting",
    ("OrderMatchingEngine", "CPP"): "Trading & Backtesting",
    ("NexusFix", "CPP"): "Trading & Backtesting",
    # Rust classification
    ("QuantMath", "Rust"): "Financial Instruments & Pricing",
    ("RustQuant", "Rust"): "Financial Instruments & Pricing",
    ("Barter", "Rust"): "Trading & Backtesting",
    ("LFEST", "Rust"): "Trading & Backtesting",
    ("TradeAggregation", "Rust"): "Technical Indicators",
    ("SlidingFeatures", "Rust"): "Technical Indicators",
    ("fin-primitives", "Rust"): "Technical Indicators",
    ("fin-stream", "Rust"): "Market Data & Data Sources",
    ("finalytics", "Rust"): "Market Data & Data Sources",
    ("OpenFinClaw", "Rust"): "Trading & Backtesting",
    ("RunMat", "Rust"): "Cross-Language Frameworks",
    ("Special-Relativity-in-Financial-Modeling", "Rust"): "Reproducing Works, Training & Books",
    # JavaScript classification
    ("finance.js", "JavaScript"): "Financial Instruments & Pricing",
    ("portfolio-allocation", "JavaScript"): "Portfolio Optimization & Risk Analysis",
    ("Ghostfolio", "JavaScript"): "Portfolio Optimization & Risk Analysis",
    ("IndicatorTS", "JavaScript"): "Technical Indicators",
    ("chart-patterns", "JavaScript"): "Technical Indicators",
    ("orderflow", "JavaScript"): "Technical Indicators",
    ("ccxt", "JavaScript"): "Trading & Backtesting",
    ("PENDAX", "JavaScript"): "Market Data & Data Sources",
    ("PreReason", "JavaScript"): "Market Data & Data Sources",
    ("rebalance", "JavaScript"): "Portfolio Optimization & Risk Analysis",
    ("QUANTAXIS_Webkit", "JavaScript"): "Visualization",
    # R overrides for misplaced items
    ("PortfolioAnalytics", "R"): "Portfolio Optimization & Risk Analysis",
    ("riskParityPortfolio", "R"): "Portfolio Optimization & Risk Analysis",
    ("portfolio", "R"): "Portfolio Optimization & Risk Analysis",
    ("sparseIndexTracking", "R"): "Portfolio Optimization & Risk Analysis",
    ("covFactorModel", "R"): "Factor Analysis",
    ("TTR", "R"): "Technical Indicators",
    # Note: fPortfolio is a sub-entry under Rmetrics, not a standalone entry.
    # It will be preserved as a sub-line under Rmetrics in Financial Instruments.
}

# Multi-language projects: name -> list of languages
MULTI_LANG = {
    "Hikyuu": ["Python", "C++"],
    "Lean": ["Python", "C#"],
    "ccxt": ["JavaScript", "Python", "PHP"],
    "OpenFinClaw": ["Python", "Rust"],
    "RunMat": ["Matlab", "Rust"],
    "pmxt": ["Python", "JavaScript"],
    "nautilus_trader": ["Python", "Rust"],
}

# Projects to remove as duplicates (keep the first occurrence)
DUPLICATES_TO_REMOVE = {
    # (name, url) pairs to skip on second occurrence
    ("fast-trade", "https://github.com/jrmeier/fast-trade"),
    ("wallstreet", "https://github.com/mcdallas/wallstreet"),
}

# Additional dedup: entries with same name but different URLs (keep first by default)
# pmxt has 3 entries: pmxt-dev (Python), pmxt-dev (JS), qoery-com (JS)
# Keep pmxt-dev/pmxt, skip qoery-com/pmxt
URLS_TO_SKIP = {
    "https://github.com/qoery-com/pmxt",  # duplicate of pmxt-dev/pmxt
}

# Section display order
SECTION_ORDER = [
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

# Sections where we DON'T add language tags (not language-specific)
NO_LANG_TAG_SECTIONS = {
    "Cross-Language Frameworks",
    "Reproducing Works, Training & Books",
    "Commercial & Proprietary Services",
    "Related Lists",
}


def parse_current_readme(path: str):
    """Parse the current language-first README and return entries."""
    re_h2 = re.compile(r"^## (.+)$")
    re_h3 = re.compile(r"^### (.+)$")
    re_entry = re.compile(r"^\s*- \[(.+?)\]\((.+?)\) - (.+)$")
    re_badge = re.compile(r"\s*!\[[^\]]*\]\([^)]*\)\s*")
    # Match indented sub-entries (e.g., Rmetrics sub-packages, QuantLib ports)
    re_sub_entry = re.compile(r"^\s{2,}- ")

    entries = []
    current_language = ""
    current_category = ""
    skip_sections = {"Languages"}
    # Track sub-entries that belong to a parent
    pending_sub_lines = []
    last_entry = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = re_badge.sub(" ", line).rstrip("\n")

            m = re_h2.match(line)
            if m:
                current_language = m.group(1).strip()
                current_category = ""
                continue

            m = re_h3.match(line)
            if m:
                current_category = m.group(1).strip()
                continue

            if current_language in skip_sections:
                continue

            # Check for sub-entries (indented items under a parent)
            if re_sub_entry.match(line) and last_entry:
                last_entry["sub_lines"].append(line)
                continue

            m = re_entry.match(line)
            if m:
                name = m.group(1).strip()
                url = m.group(2).strip()
                desc = m.group(3).strip()

                entry = {
                    "name": name,
                    "url": url,
                    "description": desc,
                    "language": current_language,
                    "category": current_category,
                    "raw_line": line,
                    "sub_lines": [],
                }
                entries.append(entry)
                last_entry = entry

    return entries


def classify_entry(entry: dict) -> str:
    """Determine the new section for an entry."""
    name = entry["name"]
    lang = entry["language"]
    cat = entry["category"]

    # Check project-level overrides first (composite key: name + language)
    override_key = (name, lang)
    if override_key in PROJECT_OVERRIDES:
        return PROJECT_OVERRIDES[override_key]

    # Check section map
    key = (lang, cat)
    if key in SECTION_MAP:
        section = SECTION_MAP[key]
        if not section.startswith("CLASSIFY_"):
            return section

    # Fallback: flag unmapped entries
    print(f"  WARNING: No mapping for ({lang!r}, {cat!r}) — project {name!r}")
    print(f"           Add to SECTION_MAP or PROJECT_OVERRIDES and rerun.")
    return "Trading & Backtesting"


def get_languages(entry: dict) -> list[str]:
    """Get language tags for an entry."""
    name = entry["name"]
    if name in MULTI_LANG:
        return MULTI_LANG[name]
    lang = entry["language"]
    # Don't tag entries from non-language sections
    if lang in (
        "Frameworks",
        "Reproducing Works, Training & Books",
        "Commercial & Proprietary Services",
        "Related Lists",
    ):
        return []
    return [lang]


def format_entry(entry: dict, section: str) -> str:
    """Format an entry with inline language tags."""
    name = entry["name"]
    url = entry["url"]
    desc = entry["description"]
    langs = get_languages(entry)

    # Build language tag string
    if langs and section not in NO_LANG_TAG_SECTIONS:
        lang_tags = " ".join(f"`{l}`" for l in langs)
        line = f"- [{name}]({url}) - {lang_tags} - {desc}"
    else:
        line = f"- [{name}]({url}) - {desc}"

    # Append sub-lines (e.g., QuantLib ports, Rmetrics sub-packages)
    result = line
    for sub in entry.get("sub_lines", []):
        result += "\n" + sub

    return result


def slugify(text: str) -> str:
    """Convert text to lowercase hyphen-separated slug (matches site/generate.py)."""
    text = text.lower().strip()
    text = re.sub(r"[&/]+", "-", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def build_toc(sections: list[str]) -> str:
    """Build the table of contents."""
    lines = ["## Contents", ""]
    for s in sections:
        lines.append(f"- [{s}](#{slugify(s)})")
    return "\n".join(lines)


def main():
    root = Path(__file__).resolve().parent.parent
    readme_path = root / "README.md"
    output_path = root / "README.md.new"

    print(f"Parsing {readme_path}...")
    entries = parse_current_readme(str(readme_path))
    print(f"Found {len(entries)} entries")

    # Classify and deduplicate
    sections: dict[str, list[str]] = {s: [] for s in SECTION_ORDER}
    seen = set()

    for entry in entries:
        # Skip explicitly blocked URLs
        if entry["url"] in URLS_TO_SKIP:
            print(f"  Skipping blocked URL: {entry['name']} ({entry['url']})")
            continue

        key = (entry["name"], entry["url"])
        if key in DUPLICATES_TO_REMOVE and key in seen:
            print(f"  Skipping duplicate: {entry['name']}")
            continue
        seen.add(key)

        section = classify_entry(entry)
        if section not in sections:
            print(f"  WARNING: Unknown section {section!r}, adding it")
            sections[section] = []
            SECTION_ORDER.append(section)

        formatted = format_entry(entry, section)
        sections[section].append(formatted)

    # Build output
    header = [
        "# Awesome Quant",
        "",
        "A curated list of insanely awesome libraries, packages and resources "
        "for Quants (Quantitative Finance).",
        "",
        "[![](https://awesome.re/badge.svg)](https://awesome.re)",
        "",
    ]

    active_sections = [s for s in SECTION_ORDER if sections.get(s)]
    toc = build_toc(active_sections)

    body_parts = []
    for section_name in SECTION_ORDER:
        items = sections.get(section_name, [])
        if not items:
            continue
        body_parts.append(f"\n## {section_name}\n")
        body_parts.append("\n".join(items))

    output = "\n".join(header) + "\n" + toc + "\n" + "\n".join(body_parts) + "\n"

    output_path.write_text(output, encoding="utf-8")
    print(f"\nWrote {output_path}")
    print(f"Sections: {len(active_sections)}")
    for s in active_sections:
        print(f"  {s}: {len(sections[s])} entries")
    print(f"\nReview the output, then: mv README.md.new README.md")


if __name__ == "__main__":
    main()
