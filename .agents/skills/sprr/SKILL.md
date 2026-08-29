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
6. Enforce `CONTRIBUTING.md` and `AGENTS.md` strictly for new entries, using the
   sentence-count interpretation in the Validation Checklist below.

If GitHub MCP tools are unavailable, report that PR operations are blocked and point the user to `docs/codex-setup.md`.

## Workflow

1. Fetch PR details, current head SHA, files changed, labels, comments, and diff with GitHub MCP.
2. Confirm whether the `reviewed` label or prior maintainer comments exist, then proceed with full validation anyway.
3. Fetch the latest `Validate PR` workflow/check attempt for the current head SHA and apply the CI evidence rules below.
4. Focus on added lines in `README.md`. Flag any other changed files as unusual for a normal contribution.
5. When mechanical validation is not established by current-head CI, save or reconstruct the PR diff locally only if needed, then validate added README entries with:

```bash
uv run python scripts/validate_readme.py --diff-from <base-ref>
```

If a base ref is not locally available, apply the same checks manually from the fetched diff.

## CI Evidence Rules

Use only the latest attempt whose commit SHA exactly matches the PR's current head SHA. A newer
queued or pending attempt supersedes an older successful attempt for the same SHA.

| Current-head result | Review behavior |
|---|---|
| `success` | Accept parser format, tag syntax, separators, the required final period, HTTPS, GitHub-link syntax, recognized section, and base-README duplicate checks as passed. Do not rerun those mechanical checks. |
| `failure` | Inspect the failing job or step. Return `NEEDS CHANGES` when validation failed; if another step failed or details are unavailable, reproduce mechanical validation before deciding. |
| queued, pending, awaiting approval | Report the review as incomplete and do not return `APPROVE`. |
| skipped, cancelled, missing | Treat mechanical validation as unverified and reproduce it before deciding. |
| success on an older SHA | Ignore it and evaluate the current SHA using these rules. |

CI never replaces inspection of the diff or the manual checks below. A successful check confirms
only mechanical rules; it does not establish tag meaning or concision, description quality,
relevance, semantic section suitability, commercial classification, repository quality,
commercial free-tier eligibility or transparency, URL tracking, cross-PR uniqueness, or
multi-project relatedness. CI cannot establish any of these manual criteria. Search open PRs and PRs
closed within the last 365 days for duplicate names and URLs.

## Validation Checklist

For every added entry:

- It matches `^\s*- \[(.*)\]\((.*)\) - (.*)$`.
- New non-commercial entries include one or more backtick tags followed by ` - `. Treat these
  as a compact tag cloud: accept concise languages, runtimes, protocols, interfaces, data
  types, and domain terms.
- Separate concepts use adjacent tags, such as `` `Python` `C++` `MCP` ``; do not reject a tag
  merely because it is not a programming language.
- Description ends with a period before optional `[GitHub](...)`.
- Treat `CONTRIBUTING.md`'s "one sentence" wording as concision guidance, not a sentence-count
  gate. Accept two or more short sentences when the overall description remains concise, factual,
  relevant, and non-promotional. Never return `NEEDS CHANGES` solely because of sentence count;
  request wording changes only for actual quality problems such as verbosity, repetition,
  unsupported claims, promotional language, or poor readability.
- URLs use `https://`.
- Optional GitHub link uses `[GitHub](https://github.com/owner/repo)`.
- Section placement matches the project's purpose.
- Distinguish repositories containing substantive implementation from thin SDK, integration,
  examples, generated-data, or marketing repositories.
- Hosted proprietary products without substantive public source are under
  `Commercial & Proprietary Services`, even when a thin repository exists.
- For repository-less commercial entries, verify a useful permanent free tier for quantitative
  finance that requires no payment information and is not a trial, demo, or waitlist.
- Treat a commercial service with only a thin SDK, integration, examples, generated-data, or
  marketing repository as repository-less for every eligibility check.
- Verify that these commercial entries publish pricing and free-tier limits plus public
  documentation, methodology, or usage examples; use a stable HTTPS URL without affiliate or
  tracking parameters; and have a concise, factual, non-promotional description.
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
- Sentence count alone does not affect the verdict; evaluate description quality using the criteria
  in the Validation Checklist.
- Commercial submissions without a qualifying permanent free tier—including paid-only,
  trial-only, demo-only, and waitlist-only offerings—are `REJECT`.
- Reserve `NEEDS CHANGES` for correctable evidence or disclosure, wording, URL, documentation, or
  placement defects when the underlying offering can qualify.
- Other `REJECT` cases include duplicates, unrelated multi-project PRs, empty PR descriptions,
  archived or abandoned projects, and other hard rejections.

## Output Shape

Report:

```text
PR #<number>: <title>
Author: <author>
Prior review: YES/NO
Files changed: <files>
Entries reviewed: <count>

Automated validation:
- Validate PR: PASS | FAIL | PENDING | UNVERIFIED
- Commit: <checked-sha> (CURRENT | STALE)
- Mechanical checks: accepted from CI | reproduced manually | incomplete

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
