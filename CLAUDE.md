# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**awesome-quant** is a curated list of quantitative finance libraries, packages, and resources. The primary content lives in `README.md` — a large markdown file organized by programming language (Python, R, Matlab, Julia, Java, JavaScript, etc.) with categorized links to open-source projects.

A companion website is generated from this data and deployed to GitHub Pages.

## Architecture

The pipeline works as follows:

1. **`README.md`** — The source of truth. All library entries follow the format: `- [name](url) - Description.`
2. **`parse.py`** — Parses `README.md`, extracts GitHub/CRAN/PyPI URLs, fetches last commit dates and stars via the GitHub API (using `PyGithub` with multithreading), and writes `site/projects.csv`.
3. **`site/generate.py`** — Reads `projects.csv` (or parses `README.md` directly) and generates a static HTML site with search, filtering, sorting, and dark mode.
4. **CI** (`.github/workflows/build.yml`) — Runs daily and on push to `main`: runs `parse.py`, runs `site/generate.py`, and deploys to GitHub Pages via `gh-pages` branch.

Supporting scripts:
- `cranscrape.py` — Scrapes CRAN package pages to find associated GitHub repos; writes `cran.csv`.
- `topic.py` — Searches GitHub for repos tagged with a topic (e.g., "quant") above a star threshold.

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

See `CONTRIBUTING.md` for full guidelines. Accepted entry formats:

```
- [Project Name](https://github.com/owner/repo) - Description ending with a period.
- [Project Name](https://site.com) - Description ending with a period. [GitHub](https://github.com/owner/repo)
- [Package Name](https://cran.r-project.org/package=pkg) - Description ending with a period.
- [package-name](https://pypi.org/project/pkg/) - Description ending with a period.
```

CRAN and PyPI entries may optionally append `[GitHub](url)` after the description.

Entries are grouped under language headings (`##`) and category subheadings (`###`). Commercial/proprietary projects go under `## Commercial & Proprietary Services`.

`parse.py` relies on this regex to extract entries: `^\s*- \[(.*)\]\((.*)\) - (.*)$`
