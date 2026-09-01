---
name: bprr
description: Bulk PR reviewer for awesome-quant. Use when the user asks to review all open PRs, review unreviewed PRs, bulk review, or mentions "bprr". Reviews open PRs lacking the reviewed label and presents a summary before any merge/comment/label action.
---

# BPRR: Bulk PR Reviewer

Review multiple open pull requests for README entry contributions.

**REQUIRED SUB-SKILL:** Use `sprr` as the canonical policy for reviewing each pull request. Read
it before starting the bulk review and apply its hard rules, workflow evidence rules, validation
checklist, verdicts, output fields, and approved-action rules unless this skill defines a
bulk-specific presentation step.

## Hard Rules

1. Use GitHub MCP tools for PR operations. Do not use `gh` for PR review, comments, labels,
   closing, or merging.
2. Filter out PRs with the `reviewed` label unless the user asks to re-review them.
3. Apply `sprr` independently to every PR. Shared retrieval may reduce repeated work, but evidence,
   findings, and verdicts never carry from one PR to another.
4. Do not comment, label, close, or merge until the user explicitly approves each action.
5. Do not auto-merge all approved PRs unless the user explicitly selects that option.
6. If GitHub MCP tools are unavailable, report the blocker and point to `docs/codex-setup.md`.

## Bulk Workflow

1. List open PRs sorted oldest first and filter to unreviewed PRs by default.
2. Fetch the default-branch `README.md` once and reuse it where `sprr` requires a base-README
   duplicate check.
3. For every included PR, fetch the data and both required workflow attempts specified by `sprr`.
4. Apply `sprr` independently to every PR, including its manual checks and cross-PR duplicate
   search over open PRs and PRs closed within the last 365 days.
5. Present the bulk summary below before asking the user to select any actions.

## Summary Output

Present a table:

```text
| PR | Title | Author | Head | Validate PR | PR Review | Entries | Format/URL | Section | Duplicate | Verdict |
|----|-------|--------|------|-------------|-----------|---------|------------|---------|-----------|---------|
```

For each row, copy the workflow states, mechanical-check result, and verdict from that PR's `sprr`
review. `Section` remains a manual semantic judgment. In `Duplicate`, report both
`README PASS|FAIL` and `PR SEARCH PASS|FAIL`.

After the table, list any PRs that need detailed notes. Include failed workflow steps, reasons
workflow evidence was not accepted, manual findings, and commercial free-tier or transparency
evidence when it affects the verdict.

Ask what to do next. Accept selections such as:

- `merge 123, 124`
- `comment 125`
- `close 126`
- `all approved`
- `none`

Apply `sprr`'s approved-action rules to each selected PR. Confirm every merge before executing it.
