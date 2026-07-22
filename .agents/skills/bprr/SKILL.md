---
name: bprr
description: Bulk PR reviewer for awesome-quant. Use when the user asks to review all open PRs, review unreviewed PRs, bulk review, or mentions "bprr". Reviews open PRs lacking the reviewed label and presents a summary before any merge/comment/label action.
---

# BPRR: Bulk PR Reviewer

Review multiple open pull requests for README entry contributions.

## Hard Rules

1. Use GitHub MCP tools for PR operations. Do not use `gh` for PR review, comments, labels, closing, or merging.
2. Filter out PRs with the `reviewed` label unless the user asks to re-review them.
3. Do not comment, label, close, or merge until the user explicitly approves each action.
4. Do not auto-merge all approved PRs unless the user explicitly selects that option.
5. If GitHub MCP tools are unavailable, report the blocker and point to `docs/codex-setup.md`.

## Workflow

1. List open PRs sorted oldest first.
2. Filter to unreviewed PRs by default.
3. Fetch the default-branch `README.md` once for duplicate checks.
4. For each PR, fetch details, labels, files, body, and diff.
5. Review only added `README.md` entries unless the PR changes other files; flag other file changes as unusual.
6. Validate each PR with the same checks as `$sprr`. Use `scripts/validate_readme.py --diff-from <base-ref>` when the PR branch is available locally; otherwise apply the validator's rules manually from the MCP diff.

## Validation Checklist

For each added entry, check:

- Parser regex match.
- Required language tags for new non-commercial entries.
- Description period before optional `[GitHub](...)`.
- `https://` URLs.
- Exact optional `[GitHub](https://github.com/owner/repo)` format.
- Correct category section.
- Commercial placement under `Commercial & Proprietary Services`.
- Duplicate project names or URLs.
- Activity, archived status, and basic documentation for GitHub repos.
- Clear rationale for multiple related projects in one PR.

## Summary Output

Present a table:

```text
| PR | Title | Author | Entries | Format | URL | Section | Duplicate | Verdict |
|----|-------|--------|---------|--------|-----|---------|-----------|---------|
```

After the table, list any PRs that need detailed notes.

Ask what to do next. Accept selections like:

- `merge 123, 124`
- `comment 125`
- `close 126`
- `all approved`
- `none`

Confirm each merge before executing it.
