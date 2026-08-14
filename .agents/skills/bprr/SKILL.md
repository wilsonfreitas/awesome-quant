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
4. For each PR, fetch details, current head SHA, labels, files, body, diff, and the latest `Validate PR` workflow/check attempt for that SHA.
5. Review only added `README.md` entries unless the PR changes other files; flag other file changes as unusual.
6. Apply the CI evidence rules below, then perform the remaining `$sprr` checks. Use `scripts/validate_readme.py --diff-from <base-ref>` only when current-head CI does not establish mechanical validity and the PR branch is available locally; otherwise apply the validator's rules manually from the MCP diff.

## CI Evidence Rules

Evaluate each PR independently. Use only the latest attempt for the current head SHA; a newer
queued or pending attempt supersedes an older success for that SHA. A result for one PR or
commit never applies to another.

| Current-head result | Review behavior |
|---|---|
| `success` | Accept parser format, tag syntax, separators, the required final period, HTTPS, GitHub-link syntax, recognized section, and base-README duplicate checks as passed. Do not repeat those mechanical checks. |
| `failure` | Inspect the failing job or step. Use `NEEDS CHANGES` when validation failed; if another step failed or details are unavailable, reproduce mechanical validation before deciding. |
| queued, pending, awaiting approval | Mark the review incomplete and do not return `APPROVE`. |
| skipped, cancelled, missing | Treat mechanical validation as unverified and reproduce it before deciding. |
| success only on an older SHA | Report `STALE`, ignore it, and reproduce mechanical validation for the current head SHA. |

For every PR, still inspect the diff and manually review tag meaning and concision, description
quality, relevance, semantic section suitability, commercial classification, repository
activity/archive/documentation/community evidence, duplicates in open PRs and PRs closed
within the last 365 days, and multi-project relatedness.

## Validation Checklist

For each added entry, check:

- Parser regex match.
- Required backtick tags for new non-commercial entries. Treat them as a compact tag cloud:
  accept concise languages, runtimes, protocols, interfaces, data types, and domain terms.
- Separate concepts must use adjacent tags, such as `` `Python` `C++` `MCP` ``; do not require
  every tag to be a programming language.
- Description period before optional `[GitHub](...)`.
- `https://` URLs.
- Exact optional `[GitHub](https://github.com/owner/repo)` format.
- Correct category section.
- Commercial placement under `Commercial & Proprietary Services`.
- Duplicate project names or URLs.
- Treat any verifiable GitHub repository mentioned as the main URL or exact `[GitHub](...)`
  suffix as a strong positive relevance signal.
- For GitHub repos, check source availability, activity, archived status, documentation, and
  community evidence. GitHub relevance does not waive duplicate, format, or quality checks.
- Clear rationale for multiple related projects in one PR.

## Summary Output

Present a table:

```text
| PR | Title | Author | Head | Validate PR | Entries | Format/URL | Section | Duplicate | Verdict |
|----|-------|--------|------|-------------|---------|------------|---------|-----------|---------|
```

Use the entry count in `Entries`. Use `PASS`, `FAIL`, `PENDING`, `UNVERIFIED`, or
`STALE` in `Validate PR`. Use `CI PASS`, `CI FAIL`, `REPRODUCED PASS`,
`REPRODUCED FAIL`, or `INCOMPLETE` in `Format/URL`. `Section` remains a manual
semantic judgment. In `Duplicate`, report both `README PASS|FAIL` and
`PR SEARCH PASS|FAIL`.

After the table, list any PRs that need detailed notes, including the failing workflow step or the reason CI evidence was not accepted.

Ask what to do next. Accept selections like:

- `merge 123, 124`
- `comment 125`
- `close 126`
- `all approved`
- `none`

Confirm each merge before executing it.
