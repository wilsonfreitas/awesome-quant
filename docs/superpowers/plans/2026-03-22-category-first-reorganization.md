# Category-First README Reorganization

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize README.md from language-first to category-first structure, so all backtesting tools (Python, R, Julia, Rust, etc.) live in one section instead of being scattered across 6+ language headings.

**Architecture:** A migration script reads the current README.md, maps each entry to its new category section, prepends an inline language tag (e.g., `` `Python` ``), deduplicates, and writes the new README.md. Then `parse.py` and `site/generate.py` are updated to extract language from inline tags instead of `##` headings. The website gains multi-language filtering.

**Tech Stack:** Python 3.11+, regex, existing parse.py/generate.py pipeline, GitHub Actions CI.

---

## File Structure

```
README.md                              — Restructured: category-first with inline language tags
parse.py                               — Updated: extract language from backtick tags, h2=category
site/generate.py                       — Updated: parse_readme() + load_csv() + tags for new structure
site/static/main.js                    — Updated: multi-language filter support
site/static/style.css                  — Updated: language tag colors per language
scripts/migrate_readme.py              — NEW: one-time migration script
CONTRIBUTING.md                        — Updated: new entry format with language tags
CLAUDE.md                              — Updated: reflect new structure
.claude/skills/review-pr/SKILL.md      — Updated: new section list and format rules
```

---

## New Entry Format

**Current:**
```markdown
- [nautilus_trader](https://github.com/nautechsystems/nautilus_trader) - High-performance algorithmic trading platform.
```
(Language is implied by the `## Python` heading above it.)

**New:**
```markdown
- [nautilus_trader](https://github.com/nautechsystems/nautilus_trader) - `Python` `Rust` - High-performance algorithmic trading platform.
```

**Regex change:** The existing regex `^\s*- \[(.*)\]\((.*)\) - (.*)$` still matches. Group 3 now captures `` `Python` `Rust` - Description. `` — a secondary regex splits language tags from description.

**New secondary regex:**
```python
re_langs = re.compile(r'^((?:`[^`]+`\s*)+)-\s*(.*)$')
```

---

## New Section Structure

| New Section (h2) | Sources (old sections mapped here) |
|---|---|
| Numerical Libraries & Data Structures | Python > Numerical, R > Numerical, Julia data libs |
| Financial Instruments & Pricing | Python > Financial Instruments, R > Financial Instruments, Java, Haskell, Scala, Julia pricing libs, Matlab > Frameworks |
| Technical Indicators | Python > Indicators, R > TTR, Julia indicator libs, JS > chart-patterns/orderflow, Go > IndicatorGo, Rust > SlidingFeatures, plus misplaced TA libs from Python > Trading (bta-lib, ta, TuneTA) |
| Trading & Backtesting | Python > Trading (minus portfolio/indicator tools), R > Trading + Backtesting, Julia trading libs, Ruby, Elixir/Erlang, Go > Kelp, Rust > Barter/LFEST, C++ > TradeFrame/PandoraTrader, C# > all, JS > ccxt/Ghostfolio/etc |
| Portfolio Optimization & Risk Analysis | Python > Risk Analysis + misplaced portfolio tools (PyPortfolioOpt, skfolio, riskparity.py, DeepDow, Eiten from Trading), R > Risk Analysis + PortfolioAnalytics/fPortfolio/riskParityPortfolio from Financial Instruments |
| Factor Analysis | Python > Factor Analysis, R > Factor Analysis |
| Sentiment Analysis & Alternative Data | Python > Sentiment Analysis |
| Time Series Analysis | Python > Time Series, R > Time Series |
| Market Data & Data Sources | Python > Data Sources, R > Data Sources, Julia > MarketData.jl/CryptoExchangeAPIs.jl, Rust > fin-stream/finalytics, JS > PENDAX/pmxt |
| Prediction Markets | pmxt (Python, JS), Polymarket Scanner API, polymarket-whales, SimpleFunctions, Parsec, Telonex |
| Calendars & Market Hours | Python > Calendars, R > Calendars |
| Visualization | Python > Visualization, Julia > LightweightCharts.jl/TechnicalIndicatorCharts.jl, JS > QUANTAXIS_Webkit |
| Excel & Spreadsheet Integration | Python > Excel Integration (unchanged) |
| Quant Research Environments | Python > Quant Research Environment (unchanged) |
| Cross-Language Frameworks | Current Frameworks section (QuantLib ecosystem, TA-Lib, XAD) |
| Reproducing Works, Training & Books | Unchanged |
| Commercial & Proprietary Services | Unchanged |
| Related Lists | Unchanged |

---

## Duplicates to Remove

| Project | Duplicate Locations | Keep |
|---|---|---|
| Hikyuu | Python > Trading, CPP | Single entry with `Python` `C++` tags in Trading & Backtesting |
| fast-trade | Python > Trading (lines 144, 149) | Single entry |
| wallstreet | Python > Data Sources (lines 245, 301) | Single entry |
| pmxt | Python > Numerical, JS (lines 42, 486, 487) | Single entry with `Python` `JavaScript` in Prediction Markets |
| QuantLib | CPP, Frameworks | Keep in Cross-Language Frameworks only |
| QuantLibRisks | Python > Risk, CPP | Single entry with `Python` `C++` |
| XAD | Python > Risk, CPP, Frameworks | Keep in Cross-Language Frameworks only |
| fecon235 | Python > Risk, Reproducing Works | Keep both (different contexts) |
| OpenFinClaw | Python > Trading, Rust | Single entry with `Python` `Rust` |
| RunMat | Matlab > Alternatives, Rust | Single entry with `Matlab` `Rust` |

## Misplaced Projects to Move

| Project | Current Section | Correct Section | Reason |
|---|---|---|---|
| PyPortfolioOpt | Trading & Backtesting | Portfolio Optimization & Risk | Portfolio optimization tool |
| skfolio | Trading & Backtesting | Portfolio Optimization & Risk | Portfolio optimization (scikit-learn based) |
| riskparity.py | Trading & Backtesting | Portfolio Optimization & Risk | Risk parity portfolio design |
| DeepDow | Trading & Backtesting | Portfolio Optimization & Risk | Deep learning portfolio optimization |
| Eiten | Trading & Backtesting | Portfolio Optimization & Risk | Eigen/Min Var/Max Sharpe portfolios |
| bta-lib | Trading & Backtesting | Technical Indicators | TA library |
| ta | Trading & Backtesting | Technical Indicators | TA library |
| TuneTA | Trading & Backtesting | Technical Indicators | TA indicator optimizer |
| TA-Lib (Python wrapper) | Trading & Backtesting | Technical Indicators | TA library wrapper |
| OpenBB Terminal | Financial Instruments | Market Data & Data Sources | Research terminal / data platform |
| Fincept Terminal | Financial Instruments | Market Data & Data Sources | Research terminal / data platform |

---

## Task 1: Write the Migration Script

**Files:**
- Create: `scripts/migrate_readme.py`

This script automates the README restructure. It reads the current README, classifies each entry, adds language tags, deduplicates, and writes the new file.

- [ ] **Step 1: Create the migration script**

```python
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
```

- [ ] **Step 2: Fix malformed entry before migration**

The `quantra` entry at README.md line 72 is missing the ` - ` separator:
```
- [quantra](https://github.com/joseprupi/quantraserver) High-performance pricing engine...
```
Fix it to:
```
- [quantra](https://github.com/joseprupi/quantraserver) - High-performance pricing engine...
```

- [ ] **Step 3: Run the migration script**

```bash
cd /home/wilson/dev/python/awesome-quant
uv run python scripts/migrate_readme.py
```

Expected: Prints entry counts per section, creates `README.md.new`.

- [ ] **Step 4: Review the output and fix classification issues**

```bash
# Check section sizes
grep -c "^- \[" README.md.new
# Check for WARNING lines in the script output
# Diff to see what moved
diff <(grep "^- \[" README.md | sort) <(grep "^- \[" README.md.new | sort)
```

Iterate: fix `PROJECT_OVERRIDES` and `SECTION_MAP` in the script, rerun until all entries are correctly classified.

- [ ] **Step 5: Replace README.md**

```bash
mv README.md README.md.bak
mv README.md.new README.md
```

- [ ] **Step 6: Manual review pass**

Read through each section in README.md. Check:
- All entries have correct language tags
- No duplicates remain
- Descriptions still end with periods
- Sub-entries (Rmetrics, QuantLib ecosystem) are preserved
- The QuantLib entry in Cross-Language Frameworks keeps all its sub-items

- [ ] **Step 7: Commit**

```bash
git add scripts/migrate_readme.py README.md
git commit -m "Reorganize README: category-first with inline language tags

Restructure from language-first (## Python > ### Category) to
category-first (## Category) organization. Each entry now has
inline language tags (e.g. \`Python\` \`Rust\`).

Deduplicates: Hikyuu, fast-trade, wallstreet, pmxt, OpenFinClaw.
Fixes misplacements: portfolio tools moved from Trading to Risk,
TA libs moved from Trading to Indicators."
```

---

## Task 2: Update parse.py — Extract Language from Inline Tags

**Files:**
- Modify: `parse.py:225-270` (README parsing loop)
- Modify: `parse.py:157-223` (Project class)

The parser currently gets `language` from `## heading` and `category` from `### heading`. In the new structure, `## heading` = category and language comes from inline backtick tags in the entry description.

- [ ] **Step 1: Add language tag extraction function**

Add after the existing `slugify` function (~line 138):

```python
re_langs = re.compile(r'^((?:`[^`]+`\s*)+)-\s*(.*)$')

def extract_languages(description: str) -> tuple[list[str], str]:
    """Extract inline language tags from description.

    Returns (languages, clean_description).
    E.g. "`Python` `Rust` - High-performance..." -> (["Python", "Rust"], "High-performance...")
    """
    m = re_langs.match(description)
    if m:
        lang_str = m.group(1)
        clean_desc = m.group(2)
        langs = re.findall(r'`([^`]+)`', lang_str)
        return langs, clean_desc
    return [], description
```

- [ ] **Step 2: Update the README parsing loop**

In the main parsing loop (~line 229+), change the heading logic:

```python
# OLD: h2 = language, h3 = category
# NEW: h2 = category (no more h3 subcategories)
# Language comes from inline tags in each entry

current_category = ""

for line in f:
    line = re_badge.sub(" ", line)
    m = rex.match(line)
    if m:
        name = m.group(1).strip()
        url = m.group(2).strip()
        raw_desc = m.group(3).strip()

        # Extract language tags from description
        languages, description = extract_languages(raw_desc)
        primary_language = languages[0] if languages else ""

        p = Project(m, primary_language, current_category, current_category)
        p.languages = languages
        p.clean_description = description
        p.start()
        projects.append(p)
    else:
        m = ret.match(line)
        if m:
            hrs = m.group(1)
            title = m.group(2).strip()
            if len(hrs) == 2 and title != "Contents":
                current_category = title
```

- [ ] **Step 3: Update the Project class to use extracted language**

Update `Project.__init__` to accept the new fields and `Project.run` to write `clean_description` and `languages` to the CSV row:

```python
# In Project.run(), update the regs dict:
self.regs["languages"] = ",".join(self.languages)
self.regs["description"] = self.clean_description
```

- [ ] **Step 4: Update CSV columns**

In the DataFrame creation (~line 273), ensure the new `languages` column is included. The old `language` column stays (primary language) and `languages` is added (comma-separated list).

- [ ] **Step 5: Test parse.py locally**

```bash
cd /home/wilson/dev/python/awesome-quant
uv run python parse.py 2>&1 | head -20
# Check CSV output
head -5 site/projects.csv
```

Expected: CSV has `languages` column. Primary `language` column still works.

- [ ] **Step 6: Commit**

```bash
git add parse.py
git commit -m "Update parse.py: extract language from inline backtick tags

h2 headings are now categories (not languages). Language is extracted
from inline tags like \`Python\` \`Rust\` at the start of descriptions.
Adds 'languages' column to CSV for multi-language projects."
```

---

## Task 3: Update site/generate.py — New Structure Support

**Files:**
- Modify: `site/generate.py:26-107` (parse_readme function)
- Modify: `site/generate.py:110-136` (load_csv function)
- Modify: `site/generate.py:146-191` (build_tags_html function)
- Modify: `site/generate.py:194-387` (generate_html function)

- [ ] **Step 1: Update parse_readme() for new heading structure**

```python
def parse_readme(path: str) -> list[dict]:
    """Parse README.md and return a list of project entries (no API data)."""
    entries = []
    current_category = ""

    re_h2 = re.compile(r"^## (.+)$")
    re_entry = re.compile(r"^\s*- \[(.+?)\]\((.+?)\) - (.+)$")
    re_github = re.compile(r"\[GitHub\]\((https://github\.com/[\w-]+/[-\w\.]+)\)")
    re_badge = re.compile(r"\s*!\[[^\]]*\]\([^)]*\)\s*")
    re_langs = re.compile(r'^((?:`[^`]+`\s*)+)-\s*(.*)$')

    skip_sections = {"Contents"}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = re_badge.sub(" ", line).rstrip("\n")

            m = re_h2.match(line)
            if m:
                current_category = m.group(1).strip()
                continue

            if current_category in skip_sections:
                continue

            m = re_entry.match(line)
            if m:
                name = m.group(1).strip()
                url = m.group(2).strip()
                raw_desc = m.group(3).strip()

                # Extract inline language tags
                m_lang = re_langs.match(raw_desc)
                if m_lang:
                    lang_str = m_lang.group(1)
                    desc = m_lang.group(2)
                    languages = re.findall(r'`([^`]+)`', lang_str)
                else:
                    desc = raw_desc
                    languages = []

                primary_language = languages[0] if languages else ""

                github_url = ""
                gh_match = re_github.search(desc)
                if gh_match:
                    github_url = gh_match.group(1)
                    desc = re_github.sub("", desc).rstrip(". ").rstrip() + "."
                elif "github.com" in url:
                    github_url = url

                repo = ""
                if github_url:
                    repo_match = re.match(
                        r"https://github\.com/([\w-]+/[-\w\.]+)", github_url
                    )
                    if repo_match:
                        repo = repo_match.group(1)

                is_cran = "cran.r-project.org" in url
                is_pypi = "pypi.org" in url or "pypi.python.org" in url
                is_commercial = current_category == "Commercial & Proprietary Services"
                section_slug = slugify(current_category)

                entries.append(
                    {
                        "project": name,
                        "language": primary_language,
                        "languages": ",".join(languages),
                        "category": current_category,
                        "section_slug": section_slug,
                        "url": url,
                        "description": desc,
                        "github": bool(github_url),
                        "cran": is_cran,
                        "pypi": is_pypi,
                        "commercial": is_commercial,
                        "github_url": github_url,
                        "repo": repo,
                        "stars": 0,
                        "last_commit": "",
                    }
                )

    return entries
```

- [ ] **Step 2: Update load_csv() for languages column**

Add to `load_csv()`:
```python
row["languages"] = row.get("languages", row.get("language", ""))
```

- [ ] **Step 3: Update build_tags_html() for language tags**

Replace the single language tag with multi-language tags:

```python
def build_tags_html(e: dict) -> str:
    """Build tag pills for an entry."""
    esc = html.escape
    tags = []

    # Language tags (from inline backtick tags)
    languages_str = e.get("languages", e.get("language", ""))
    languages = [l.strip() for l in languages_str.split(",") if l.strip()]
    skip_langs = {"Commercial & Proprietary Services", "Related Lists",
                  "Reproducing Works, Training & Books", "Cross-Language Frameworks"}
    for lang in languages:
        if lang and lang not in skip_langs:
            tags.append(
                f'<button class="tag tag-lang" data-filter-type="language" '
                f'data-filter-value="{esc(lang)}">{esc(lang.lower())}</button>'
            )

    # Category tag
    category = e.get("category", "")
    section_slug = e.get("section_slug", "")
    if section_slug:
        tags.append(
            f'<button class="tag tag-section" data-filter-type="category" '
            f'data-filter-value="{esc(category)}">{esc(section_slug)}</button>'
        )

    # Source tags (unchanged)
    if e.get("github"):
        tags.append(
            '<button class="tag tag-source tag-github" '
            'data-filter-type="source" data-filter-value="github">github</button>'
        )
    if e.get("cran"):
        tags.append(
            '<button class="tag tag-source tag-cran" '
            'data-filter-type="source" data-filter-value="cran">cran</button>'
        )
    if e.get("pypi"):
        tags.append(
            '<button class="tag tag-source tag-pypi" '
            'data-filter-type="source" data-filter-value="pypi">pypi</button>'
        )
    if e.get("commercial"):
        tags.append(
            '<button class="tag tag-source tag-commercial" '
            'data-filter-type="source" data-filter-value="commercial">commercial</button>'
        )

    return "\n          ".join(tags)
```

- [ ] **Step 4: Update data attributes in generate_html()**

Change `data-language` to `data-languages` (space-separated) in the row template:

```python
languages_attr = esc(" ".join(
    l.strip() for l in e.get("languages", e.get("language", "")).split(",") if l.strip()
))

# In the row template:
f"""<tr class="row" data-languages="{languages_attr}" data-category="{category}" ..."""
```

- [ ] **Step 5: Update languages count in hero section**

Replace the language counting logic:
```python
languages = sorted(
    set(
        lang.strip()
        for e in entries
        for lang in e.get("languages", e.get("language", "")).split(",")
        if lang.strip()
        and lang.strip() not in {
            "Commercial & Proprietary Services",
            "Related Lists",
            "Reproducing Works, Training & Books",
            "Cross-Language Frameworks",
        }
    )
)
```

- [ ] **Step 6: Test generate.py locally**

```bash
uv run python site/generate.py
# Open site/index.html in browser and verify:
# - Language tags appear on entries
# - Category tags show section names
# - Filtering by language tag works
# - Search still works
```

- [ ] **Step 7: Commit**

```bash
git add site/generate.py
git commit -m "Update generate.py for category-first README structure

parse_readme() now reads h2 as category and extracts language from
inline backtick tags. build_tags_html() generates per-language tag
buttons. data-languages attribute supports multi-language filtering."
```

---

## Task 4: Update site/static/main.js — Multi-Language Filter

> **Important:** Tasks 3 and 4 rename `data-language` to `data-languages`. These changes must be committed together (or in the same deploy) — if generate.py writes `data-languages` but main.js still reads `data-language`, language filtering breaks.

**Files:**
- Modify: `site/static/main.js` (applyFilters function)

- [ ] **Step 1: Update filter logic for data-languages**

Change from `row.dataset.language` (single value) to `row.dataset.languages` (space-separated):

```javascript
// OLD:
const language = row.dataset.language || "";
if (ft === "language" && language !== fv) show = false;

// NEW:
const languages = (row.dataset.languages || "").split(" ");
if (ft === "language" && !languages.includes(fv)) show = false;
```

- [ ] **Step 2: Test in browser**

Open `site/index.html`, click a language tag (e.g., "python"), verify filtering shows only Python entries. Click a multi-language project's tag, verify it appears in both language filters.

- [ ] **Step 3: Commit**

```bash
git add site/static/main.js
git commit -m "Update main.js: support multi-language filtering

data-languages is now space-separated. Filter checks includes()
instead of exact match, so multi-language projects appear in
both language filters."
```

---

## Task 5: Update site/static/style.css — Language Tag Colors

**Files:**
- Modify: `site/static/style.css` (tag styles section)

- [ ] **Step 1: Add per-language color classes**

Add CSS for language-specific tag colors so users can visually distinguish languages at a glance:

```css
/* Language-specific tag colors */
.tag-lang[data-filter-value="Python"] { background: #306998; color: #FFD43B; }
.tag-lang[data-filter-value="R"] { background: #276DC3; color: #fff; }
.tag-lang[data-filter-value="Julia"] { background: #9558B2; color: #fff; }
.tag-lang[data-filter-value="JavaScript"] { background: #F7DF1E; color: #000; }
.tag-lang[data-filter-value="Rust"] { background: #CE412B; color: #fff; }
.tag-lang[data-filter-value="C++"] { background: #00599C; color: #fff; }
.tag-lang[data-filter-value="C#"] { background: #68217A; color: #fff; }
.tag-lang[data-filter-value="Java"] { background: #ED8B00; color: #fff; }
.tag-lang[data-filter-value="Golang"] { background: #00ADD8; color: #fff; }
.tag-lang[data-filter-value="Haskell"] { background: #5D4F85; color: #fff; }
.tag-lang[data-filter-value="Scala"] { background: #DC322F; color: #fff; }
.tag-lang[data-filter-value="Ruby"] { background: #CC342D; color: #fff; }
.tag-lang[data-filter-value="Matlab"] { background: #E16737; color: #fff; }
.tag-lang[data-filter-value="Elixir/Erlang"] { background: #4B275F; color: #fff; }
```

- [ ] **Step 2: Commit**

```bash
git add site/static/style.css
git commit -m "Add per-language color coding for tag pills"
```

---

## Task 6: Update Documentation

**Files:**
- Modify: `CONTRIBUTING.md`
- Modify: `CLAUDE.md`
- Modify: `.claude/skills/review-pr/SKILL.md`

- [ ] **Step 1: Update CONTRIBUTING.md entry formats**

Add the new format with language tags. Update section placement guidance:

```markdown
## Entry Format

Each entry must include a language tag and follow this format:

### Single language
\```markdown
- [Project Name](https://github.com/owner/repo) - `Python` - Short description ending with a period.
\```

### Multiple languages
\```markdown
- [Project Name](https://github.com/owner/repo) - `Python` `Rust` - Short description ending with a period.
\```

### With website and GitHub repo
\```markdown
- [Project Name](https://project-site.com) - `Python` - Short description ending with a period. [GitHub](https://github.com/owner/repo)
\```

### CRAN project
\```markdown
- [Package Name](https://cran.r-project.org/package=pkgname) - `R` - Short description ending with a period.
\```

### PyPI project
\```markdown
- [package-name](https://pypi.org/project/package-name/) - `Python` - Short description ending with a period.
\```
```

Update Section Placement to list the new category sections instead of language sections.

- [ ] **Step 2: Update CLAUDE.md**

Update the Architecture and Contributing sections to reflect:
- README is organized by category, not by language
- Entry format includes inline language tags
- `parse.py` extracts language from backtick tags
- CSV has `languages` column

- [ ] **Step 3: Update review-pr skill**

Update `.claude/skills/review-pr/SKILL.md`:
- Step 5a: New entry format with language tags
- Step 5c: Section list uses new category names
- Validation: check that language tag is present and valid

- [ ] **Step 4: Commit**

```bash
git add CONTRIBUTING.md CLAUDE.md .claude/skills/review-pr/SKILL.md
git commit -m "Update docs for category-first README organization

CONTRIBUTING.md: new entry format with inline language tags.
CLAUDE.md: updated architecture and contributing sections.
review-pr skill: updated validation rules and section list."
```

---

## Task 7: Final Integration Test

- [ ] **Step 1: Run the full pipeline locally**

```bash
# Generate site from README directly (no CSV/API needed)
rm -f site/projects.csv
uv run python site/generate.py
```

Expected: `site/index.html` generated with all entries, language tags visible, category tags visible.

- [ ] **Step 2: Open in browser and verify**

Check:
- [ ] All sections appear in correct order
- [ ] Language tags display with correct colors
- [ ] Clicking a language tag filters correctly
- [ ] Clicking a category tag filters correctly
- [ ] Search works across all entries
- [ ] Sorting by stars/name/date works
- [ ] Expand rows show correct description and links
- [ ] Dark mode toggle works
- [ ] Hero stats show correct project count and language count

- [ ] **Step 3: Run parse.py (if GitHub token available)**

```bash
GITHUB_ACCESS_TOKEN=<token> uv run python parse.py
uv run python site/generate.py
```

Verify CSV is generated correctly and site renders from CSV.

- [ ] **Step 4: Clean up**

```bash
rm -f README.md.bak
```

- [ ] **Step 5: Final commit and push**

```bash
git add -A
git commit -m "Complete category-first reorganization"
git push origin main
```
