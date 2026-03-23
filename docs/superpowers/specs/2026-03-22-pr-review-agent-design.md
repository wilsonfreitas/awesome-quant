# PR Review Agent — Design Spec

**Date**: 2026-03-22
**Status**: Approved

## Overview

An automated GitHub Actions workflow that evaluates every new pull request against the rules in `CONTRIBUTING.md`. Compliant PRs are auto-merged to `main`. Non-compliant PRs are left untouched for manual review.

## Goals

- Auto-merge PRs that fully comply with all contributing rules
- Zero false positives — only merge when every check passes
- No action on non-compliant PRs (no comments, no closing, no labels)
- Notifications via GitHub's built-in notification system

## New Files

| File | Purpose |
|------|---------|
| `.github/workflows/pr-review.yml` | Workflow triggered on PR open/update |
| `scripts/review_pr.py` | Validation script implementing all CONTRIBUTING.md rules |

## Component 1: GitHub Actions Workflow (`pr-review.yml`)

**Trigger**: `pull_request` events (types: `opened`, `synchronize`) targeting `main`.

**Steps**:
1. Checkout the repo (with the PR merge ref)
2. Set up Python + uv
3. Run the validation script: `uv run python scripts/review_pr.py`
4. On exit 0: approve the PR via GitHub API and squash-merge it
5. On exit 0: the merge comment thanks the contributor
6. On non-zero exit: do nothing

**Permissions**: `contents: write`, `pull-requests: write`.

**Concurrency**: No special concurrency controls needed — each PR runs independently.

## Component 2: Validation Script (`scripts/review_pr.py`)

A single Python script using `PyGithub` (already a project dependency) and the standard library.

### Input

Environment variables set by the workflow:
- `GITHUB_TOKEN` — GitHub Actions token
- `PR_NUMBER` — the pull request number
- `GITHUB_REPOSITORY` — `owner/repo` string

### Validation Pipeline

All checks must pass for auto-merge. The script exits 0 only if every check passes, non-zero otherwise.

#### 1. PR Description Check
- Reject if the PR body is empty or whitespace-only.

#### 2. Files Changed Check
- Only `README.md` should be modified.
- Any other file changed → skip (exit non-zero).

#### 3. Extract Added Lines
- From the PR diff, extract only lines added to `README.md`.
- Ignore blank lines, section headers (`##`, `###`), and other non-entry lines.

#### 4. Single Entry Check
- Exactly one new entry line must be added.
- Zero or more than one → skip.

#### 5. Format Validation
The entry must match the regex used by `parse.py`:
```
^\s*- \[(.*)\]\((.*)\) - (.*)$
```

Additional checks:
- Description ends with a period (`.`) before the optional `[GitHub]` link.
- All URLs use `https://`.
- `[GitHub](url)` link, if present, uses the exact format `[GitHub](https://github.com/owner/repo)`.

#### 6. Duplicate Check
- Search the current `README.md` for the project name (case-insensitive).
- Search for all URLs found in the entry.
- If any match is found → skip.

#### 7. Section Placement Check
- Verify the entry is placed under a valid `##` (language) and `###` (category) heading.
- The entry must not be floating outside a recognized section.

#### 8. Activity Check
For any GitHub URL found in the entry (primary URL or `[GitHub](url)` link):
- Fetch the repo via GitHub API.
- `archived == true` → skip.
- Last push date older than 12 months → skip.
- No README file in the repo → skip.

#### 9. URL Reachability
- Verify the primary URL returns a non-error HTTP status (2xx or 3xx).

### Output
- Prints a structured summary to stdout (pass/fail per check) for workflow logs.
- Exit code 0 = all passed, non-zero = at least one check failed.

## Component 3: Merge & Notification Flow

### On All Checks Pass (exit 0)
1. The workflow submits an approving review via `GITHUB_TOKEN` with message: *"All checks passed. Auto-merging. Thanks for the contribution!"*
2. Squash-merges the PR to `main`.
3. This triggers the existing `build.yml` workflow (push to `main` with `README.md` change), so the site auto-updates.

### On Any Check Fails (non-zero exit)
- The workflow does nothing.
- The PR remains open for manual review.

### Notifications
GitHub's built-in notifications cover all cases:
- **New PR opened** → notified as repo owner.
- **PR auto-merged** → notified via merge event.
- **PR left open** → visible in open PR list.

No additional notification infrastructure required.

## Dependencies

- `PyGithub` — already in `pyproject.toml`
- No new dependencies needed

## Security Considerations

- The `GITHUB_TOKEN` provided by GitHub Actions has scoped permissions (only `contents: write` and `pull-requests: write`).
- The script never executes code from the PR — it only reads the diff and queries the GitHub API.
- URL reachability checks use HEAD/GET requests only.
