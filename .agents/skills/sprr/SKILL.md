---
name: sprr
description: Single PR reviewer for awesome-quant. Use when the user asks to review, validate, comment on, label, close, or merge one specific pull request that adds README.md entries. Triggers include "sprr", "review PR", "check PR", and "validate contribution".
---

# SPRR: Single PR Reviewer

Review one pull request that adds entries to `README.md`.

## Hard Rules

1. Review only the PR number the user requested. If no PR number is given, ask for one.
2. Use GitHub MCP tools for PR operations. Do not use `gh` for PR review, comments, labels, closing, or merging.
3. Do not modify the PR until the user explicitly approves that action.
4. Always present findings before asking whether to comment, label, close, or merge.
5. Always ask before merging.
6. Enforce `CONTRIBUTING.md` and `AGENTS.md` strictly for new entries.

If GitHub MCP tools are unavailable, report that PR operations are blocked and point the user to `docs/codex-setup.md`.

## Workflow

1. Fetch PR details, files changed, labels, comments, and diff with GitHub MCP.
2. Confirm whether the `reviewed` label or prior maintainer comments exist, then proceed with full validation anyway.
3. Focus on added lines in `README.md`. Flag any other changed files as unusual for a normal contribution.
4. Save or reconstruct the PR diff locally only if needed, then validate added README entries with:

```bash
uv run python scripts/validate_readme.py --diff-from <base-ref>
```

If a base ref is not locally available, apply the same checks manually from the fetched diff.

## Validation Checklist

For every added entry:

- It matches `^\s*- \[(.*)\]\((.*)\) - (.*)$`.
- New non-commercial entries include one or more backtick tags followed by ` - `. Treat these
  as a compact tag cloud: accept concise languages, runtimes, protocols, interfaces, data
  types, and domain terms.
- Separate concepts use adjacent tags, such as `` `Python` `C++` `MCP` ``; do not reject a tag
  merely because it is not a programming language.
- Description ends with a period before optional `[GitHub](...)`.
- URLs use `https://`.
- Optional GitHub link uses `[GitHub](https://github.com/owner/repo)`.
- Section placement matches the project's purpose.
- Commercial/proprietary projects are under `Commercial & Proprietary Services`.
- Project name and URLs are not duplicates of existing README entries.
- Any verifiable GitHub repository mentioned as the main URL or exact `[GitHub](...)` suffix
  is a strong positive relevance signal.
- GitHub projects are checked for source availability, activity, archived status,
  documentation, and community evidence. GitHub relevance does not waive duplicate, format,
  or quality checks.
- Multiple projects in one PR are closely related and explained in the PR body.

## Verdicts

Use these verdicts:

- `APPROVE`: entry is ready to merge.
- `NEEDS CHANGES`: fixable format, section, URL, description, or documentation issue.
- `REJECT`: duplicate, unrelated multi-project PR, empty PR description, archived/abandoned project, or other hard rejection.

## Output Shape

Report:

```text
PR #<number>: <title>
Author: <author>
Prior review: YES/NO
Files changed: <files>
Entries reviewed: <count>

Findings:
- <entry>: <status and reason>

Verdict: APPROVE | NEEDS CHANGES | REJECT
Recommended action: <merge/comment/close/no action>
```

Then ask for explicit approval before doing the recommended action.

## Approved Actions After User Consent

- If approved and user says to merge: merge with squash unless user requests otherwise.
- If needs changes and user says to comment: leave one concise comment with all requested fixes, then add `reviewed` if available.
- If rejected and user says to close: leave a polite rejection comment and close the PR.
