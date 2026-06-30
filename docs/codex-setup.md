# Codex Setup

This repo is ready for Codex through `AGENTS.md` and repo-scoped skills in
`.agents/skills`.

## What Codex Loads

- `AGENTS.md` contains durable repository instructions.
- `.agents/skills/sprr` reviews one PR.
- `.agents/skills/bprr` reviews open PRs in bulk.
- `.agents/skills/update-pypi-dates` refreshes tracked PyPI dates.

Restart Codex after adding or changing skills if they do not appear in skill
selection.

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

## Parser And Site Commands

`parse.py` needs a GitHub token because it enriches entries with GitHub metadata:

```bash
GITHUB_ACCESS_TOKEN=<token> uv run python parse.py
```

The site generator can run locally without a token when it can use existing CSV
data or parse `README.md` directly:

```bash
uv run python site/generate.py
```

## Claude Files

The existing `.claude/` files and `CLAUDE.md` are kept for compatibility. Codex
uses `AGENTS.md` and `.agents/skills` as the canonical workflow surfaces.
