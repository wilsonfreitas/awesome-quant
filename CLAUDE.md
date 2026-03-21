# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**awesome-quant** is a curated list of quantitative finance libraries, packages, and resources. The primary content lives in `README.md` — a large markdown file organized by programming language (Python, R, Matlab, Julia, Java, JavaScript, etc.) with categorized links to open-source projects.

A companion website is generated from this data and deployed to GitHub Pages.

## Architecture

The pipeline works as follows:

1. **`README.md`** — The source of truth. All library entries follow the format: `- [name](url) - Description.`
2. **`parse.py`** — Parses `README.md`, extracts GitHub repo URLs, fetches last commit dates via the GitHub API (using `PyGithub` with multithreading), and writes `site/projects.csv`.
3. **`site/`** — A [Quarto](https://quarto.org/) website project (`_quarto.yml`) that renders `projects.csv` into an interactive table. Output goes to `site/docs/`.
4. **CI** (`.github/workflows/build.yml`) — Runs daily and on push to `master`: runs `parse.py`, renders the Quarto site, and deploys to GitHub Pages via `gh-pages` branch.

Supporting scripts:
- `cranscrape.py` — Scrapes CRAN package pages to find associated GitHub repos; writes `cran.csv`.
- `topic.py` — Searches GitHub for repos tagged with a topic (e.g., "quant") above a star threshold.

## Commands

```bash
# Install dependencies (uses Poetry, requires Python 3.11+)
poetry install --no-root

# Run the parser (requires GITHUB_ACCESS_TOKEN env var)
GITHUB_ACCESS_TOKEN=<token> poetry run python parse.py

# Render the Quarto site (requires Quarto + R with knitr/rmarkdown/DT)
quarto render site
```

## Contributing Entries

Each entry in `README.md` must follow the pattern:
```
- [Project Name](https://url) - Short description ending with a period.
```

Entries are grouped under language headings (##) and category subheadings (###). `parse.py` relies on this exact regex pattern to extract entries: `^\s*- \[(.*)\]\((.*)\) - (.*)$`
