# AGENTS.md

## Project Overview

`awesome-quant` is a curated list of quantitative finance libraries, packages,
and resources. The source of truth is `README.md`; the static website is
generated into `site/index.html`.

The README is organized by category headings (`##`), not by language headings.
Project metadata is stored in inline backtick tags inside each entry. Tags commonly identify
languages, but may also identify runtimes, protocols, interfaces, data types, or domains.

## Architecture

1. `README.md` contains curated entries.
2. `parse.py` parses `README.md`, enriches GitHub/CRAN/PyPI metadata, and writes
   `site/projects.csv`.
3. `site/generate.py` reads `site/projects.csv` when present, otherwise parses
   `README.md` directly for local previews, then writes `site/index.html`.
4. `.github/workflows/build.yml` runs the parser and generator, then deploys
   `site/` to GitHub Pages.

## Commands

```bash
# Install deps (requires Python 3.11+)
uv sync --no-install-project

# Validate README entries changed in a PR
uv run python scripts/validate_readme.py --diff-from origin/main

# Validate the full README; legacy format/duplicate/URL issues are warnings by default
uv run python scripts/validate_readme.py

# Run parser (requires GitHub token)
GITHUB_ACCESS_TOKEN=<token> uv run python parse.py

# Generate static site
uv run python site/generate.py
```

## Entry Format

The critical parser regex is:

```text
^\s*- \[(.*)\]\((.*)\) - (.*)$
```

Accepted entry examples:

```markdown
- [Project Name](https://github.com/owner/repo) - `Python` - Description ending with a period.
- [Project Name](https://github.com/owner/repo) - `Python` `Rust` - Description ending with a period.
- [Project Name](https://site.com) - `Python` - Description ending with a period. [GitHub](https://github.com/owner/repo)
- [Package Name](https://cran.r-project.org/package=pkg) - `R` - Description ending with a period.
- [package-name](https://pypi.org/project/pkg/) - `Python` - Description ending with a period.
```

Rules:

- New non-commercial entries must include one or more concise backtick tags followed by ` - `.
  Tags form a compact tag cloud and are not restricted to programming languages.
- Each tag must use its own backtick pair, for example `` `Python` `C++` `MCP` ``.
- Descriptions must end with a period before the optional `[GitHub](...)` link.
- URLs in new entries must use `https://`.
- A valid GitHub repository used as the main URL or exact `[GitHub](...)` suffix is a strong
  positive relevance signal. Review its activity and documentation rather than treating
  non-language tags as format errors.
- Commercial/proprietary projects belong in `## Commercial & Proprietary Services`.
- Backtick tags are optional only for commercial services and other metadata-free
  sections such as `Related Lists`.
- Use `CONTRIBUTING.md` as the user-facing source for contribution rules.

## PR Review Workflow

This repo receives most contributions as pull requests adding README entries.
Use Codex repo skills for repeatable review workflows:

- `$sprr` - single PR reviewer.
- `$bprr` - bulk PR reviewer.
- `$update-pypi-dates` - refresh tracked PyPI last-updated dates.

Review requirements:

1. Only review the PRs the user asked you to review.
2. Use GitHub MCP tools for PR operations, not the `gh` CLI.
3. Present findings before any PR-modifying action.
4. Always ask the user before commenting, labeling, closing, or merging.
5. Check section placement, duplicates in `README.md`, entry format, URL format,
   and project activity/documentation. Give substantial positive weight to a verifiable
   GitHub repository mentioned as either the main URL or exact suffix.
6. Use the `reviewed` label only after the user approves a review comment.

## GitHub MCP Tools

This project expects Codex to have a GitHub MCP server configured for PR work.
Useful tool capabilities include:

- List open pull requests.
- Get PR details, files, comments, labels, and diffs.
- Fetch `README.md` from the default branch for duplicate checks.
- Add PR comments and labels.
- Merge pull requests after explicit user approval.

See `docs/codex-setup.md` for local Codex setup notes. If GitHub MCP tools are
not available in a session, report that PR operations are blocked and ask the
user to configure the MCP server.

## Local Validation Notes

- `scripts/validate_readme.py --diff-from <ref>` is intended for PR checks. It
  validates only added README entries and treats duplicates/URL issues as errors
  for those additions.
- `scripts/validate_readme.py` validates the full README. Legacy format, duplicate, and
  URL problems are reported as warnings unless strict flags are used.
- `parse.py` requires `GITHUB_ACCESS_TOKEN`; `site/generate.py` can run without
  the token if `site/projects.csv` already exists or if it falls back to direct
  README parsing.
