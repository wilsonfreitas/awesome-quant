# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**awesome-quant** is a curated list of quantitative finance libraries, packages, and resources. The primary content lives in `README.md` — a large markdown file **organized by category** (Numerical Libraries, Trading & Backtesting, Market Data, etc.) with inline language tags that identify which programming languages each project supports.

A companion website is generated from this data and deployed to GitHub Pages.

## Architecture

The pipeline works as follows:

1. **`README.md`** — The source of truth. All library entries follow the format: `- [name](url) - \`Language\` - Description.`
   - Entries are grouped under category headings (`##`), not language headings
   - Language is identified via inline backtick tags (e.g., `` `Python` ``, `` `Rust` ``) in the description
   - Multi-language projects have multiple tags (e.g., `` `Python` `Rust` ``)

2. **`parse.py`** — Parses `README.md`, extracts language from backtick tags, fetches last commit dates and stars via the GitHub API (using `PyGithub` with multithreading), and writes `site/projects.csv` with a `languages` column (comma-separated).

3. **`site/generate.py`** — Reads `site/projects.csv` (or parses `README.md` directly) and generates a static HTML site (`site/index.html`) with search, filtering by language/category/source, sorting, and dark mode. Front-end assets live in `site/static/` (`main.js`, `style.css`).

4. **CI** (`.github/workflows/build.yml`, workflow name "Update site") — Runs daily (cron `0 1 * * *`) and on push to `main` touching `README.md`, `parse.py`, or `site/**`: runs `parse.py`, runs `site/generate.py`, and deploys the `site/` directory to GitHub Pages via `peaceiris/actions-gh-pages`.

Supporting scripts:
- `cranscrape.py` — Scrapes CRAN package pages to find associated GitHub repos; writes `cran.csv`.
- `topic.py` — Searches GitHub for repos tagged with a topic (e.g., "quant") above a star threshold.
- `scripts/migrate_readme.py` — One-off migration that converted `README.md` from language-first to category-first organization (kept for reference).

## Commands

```bash
# Install dependencies (uses uv, requires Python 3.11+)
uv sync --no-install-project

# Run the parser (requires GITHUB_ACCESS_TOKEN env var)
GITHUB_ACCESS_TOKEN=<token> uv run python parse.py

# Generate the static site
uv run python site/generate.py
```

## Contributing Entries

See `CONTRIBUTING.md` for full guidelines. All entries must include language tags:

```
- [Project Name](https://github.com/owner/repo) - `Python` - Description ending with a period.
- [Project Name](https://github.com/owner/repo) - `Python` `Rust` - Multi-language project description.
- [Project Name](https://site.com) - `Python` - Description ending with a period. [GitHub](https://github.com/owner/repo)
- [Package Name](https://cran.r-project.org/package=pkg) - `R` - Description ending with a period.
- [package-name](https://pypi.org/project/pkg/) - `Python` - Description ending with a period.
```

CRAN and PyPI entries may optionally append `[GitHub](url)` after the description.

Entries are grouped under category headings (`##`), not language headings. Language is identified via inline backtick tags. Commercial/proprietary projects go under `## Commercial & Proprietary Services`.

`parse.py` and `site/generate.py` rely on this regex to extract entries: `^\s*- \[(.*)\]\((.*)\) - (.*)$`

The description text (group 3) may start with language tags in the format `` `Language1` `Language2` - `` followed by the actual description.

## PR Reviews

This repo receives most contributions as pull requests adding new entries. Use the **GitHub MCP tools** (e.g. `list_pull_requests`, `pull_request_read`, `merge_pull_request`, `add_issue_comment`, `update_pull_request`), **not** the `gh` CLI, for PR operations.

Dedicated skills drive the review workflow:
- `sprr` — Single PR reviewer: validate one PR's entry against the format rules.
- `bprr` — Bulk PR reviewer: review all open PRs lacking the "reviewed" label, then present a summary for selection before merging.
- `update-pypi-dates` — Refresh last-updated dates for PyPI entries in `README.md`.

Review checklist: always ask before merging; verify section placement (commercial entries belong under "Commercial & Proprietary Services", not Market Data); check for duplicates in `README.md`; apply the "reviewed" label after commenting.

See `AGENTS.md` for the agent-facing command and tool summary, and `CONTRIBUTING.md` for contributor guidelines.
