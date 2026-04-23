# AGENTS.md

## Commands

```bash
# Install deps (requires Python 3.11+)
uv sync --no-install-project

# Run parser (requires GitHub token)
GITHUB_ACCESS_TOKEN=<token> uv run python parse.py

# Generate static site
uv run python site/generate.py
```

## GitHub MCP Tools

This repo uses GitHub MCP tools for PR operations (not `gh` CLI). Key tools:
- `github_list_pull_requests` - list open PRs
- `github_get_pull_request` - get PR details
- `github_get_pull_request_files` - get files changed
- `github_merge_pull_request` - merge PRs
- `github_add_issue_comment` - comment on PRs
- `github_update_issue` - close/update issues and PRs
- `github_get_file_contents` - fetch README.md from repo

## Entry Format

The critical regex: `^\s*- \[(.*)\]\((.*)\) - (.*)$`

- Must include backtick language tags (e.g., `` `Python` ``)
- Description must end with period
- Commercial sites in "Commercial & Proprietary Services" section
- Language tag optional for commercial sites

See CLAUDE.md and CONTRIBUTING.md for full details.

## PR Review Workflow

1. Always ask user before merging
2. Check section placement (not Market Data if commercial)
3. Check for duplicates in README
4. Use "reviewed" label after commenting
