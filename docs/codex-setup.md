# Codex Setup

This repo is ready for Codex through `AGENTS.md` and repo-scoped skills in
`.agents/skills`.

## What Codex Loads

- `AGENTS.md` contains durable repository instructions.
- `.agents/skills/sprr` reviews one PR.
- `.agents/skills/bprr` reviews open PRs in bulk.
- `.agents/skills/update-pypi-dates` refreshes tracked PyPI dates.
- `.agents/skills/create-entry` drafts or adds README entries from project URLs,
  GitHub issues, or Linear issues, checking `CONTRIBUTING.md` for eligibility.

Restart Codex after adding or changing skills if they do not appear in skill
selection.

## Creating Entries

Example requests:

```text
$create-entry suggest an entry for https://github.com/owner/project
$create-entry draft an entry from GitHub issue #123
$create-entry add the project from Linear issue TEAM-123 to README.md
```

The skill recommends the entry text, tags, and category with supporting evidence.
Suggestion requests leave the README untouched; requests to add an eligible project
apply and validate the local edit. GitHub issue lookup and PR duplicate searches use
GitHub MCP; Linear issue lookup requires a connected Linear tool. If issue access is
unavailable, provide the issue text or project URL to continue with a provisional
proposal until any required checks can be completed.

## GitHub MCP Requirement

PR review workflows require a GitHub MCP server. Configure it in your own Codex
configuration, usually `~/.codex/config.toml`. Do not commit personal access
tokens or local auth files to this repository.

After configuring GitHub MCP, start Codex in this repository and run:

```text
/mcp
```

Confirm that a GitHub MCP server is enabled and exposes tools that can:

- list pull requests,
- read PR details, files, labels, comments, and diffs,
- read `README.md` from the default branch,
- add comments and labels,
- merge pull requests after explicit user approval.

If those tools are missing, `$sprr` and `$bprr` should report that PR operations
are blocked instead of falling back to `gh`.

## Local Validation

Install dependencies once:

```bash
uv sync --no-install-project
```

Validate README entries added relative to the base branch:

```bash
uv run python scripts/validate_readme.py --diff-from origin/main
```

Validate the full README:

```bash
uv run python scripts/validate_readme.py
```

Full validation reports legacy duplicate, URL, and format issues as warnings by
default. PR-added entries treat those issues as errors.

Run the offline regression suite:

```bash
uv run python -m unittest discover -s tests -q
```

The `Tests` workflow runs this suite on pull requests, pushes to main, and manual
dispatch. It has read-only permissions and no persisted checkout credentials.
Tests mock external services and use temporary outputs; do not substitute live
metadata refreshes or the issue-writing audit CLI. `PR Review` retains trusted-base
execution. The existing two-workflow admission policy and branch protection are
unchanged by the additional test workflow.

## Parser And Site Commands

`parse.py` needs a GitHub token because it enriches entries with GitHub metadata:

```bash
GITHUB_ACCESS_TOKEN=<token> uv run python parse.py
```

The token-free default preview always reads the current README, even when an old
CSV is present:

```bash
uv run python site/generate.py
```

Production runs the parser first, then `uv run python site/generate.py --source csv`.
Explicit CSV mode fails if the CSV is unavailable; it never falls back to README.
Use `--readme PATH`, `--csv PATH`, and `--output PATH` for isolated previews.
The generated `site/projects.csv` and `site/index.html` are ignored source-tree
outputs, rebuilt for deployment. Source assets and `site/.nojekyll` remain tracked.

## Agent Instructions

This repository uses Codex only. `AGENTS.md` and `.agents/skills` are the
canonical workflow surfaces.

## Operational Map

- Automated core: `parse.py` enriches catalogue metadata, `site/generate.py`
  builds the site, and the PR validation/review and README audit workflows
  perform their documented checks. The audit CLI can update a GitHub issue;
  do not run it as an offline test.
- Manual catalogue maintenance: use the four Codex skills listed above. The
  PyPI updater edits README dates but never commits or pushes automatically.
- Manual CRAN discovery: `uv run python cranscrape.py` fetches its fixed package
  list and writes ignored `cran.csv` in the working directory. This file is
  not a site input. No credentials are needed.
- Manual topic discovery: `uv run python topic.py` requires
  `GITHUB_ACCESS_TOKEN` and prints GitHub quant-topic candidates. Its existing
  discovery heuristic is not an admission policy. It writes no catalogue files.
- Optional developer tooling: `uv run mypy <paths>` is available for manual
  checks; this cleanup does not introduce a strict typing requirement.

Importing the manual discovery modules performs no network calls or file writes.
