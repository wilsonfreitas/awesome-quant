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

> **Note**: CONTRIBUTING.md states that certain PRs "will be closed" automatically. This agent deliberately deviates from that — non-compliant PRs are left open for manual review instead. The maintainer handles rejections personally.

## New Files

| File | Purpose |
|------|---------|
| `.github/workflows/pr-review.yml` | Workflow triggered on PR open/update |
| `scripts/review_pr.py` | Validation script implementing all CONTRIBUTING.md rules |

## Component 1: GitHub Actions Workflow (`pr-review.yml`)

**Trigger**: `pull_request_target` events (types: `opened`, `synchronize`, `reopened`, `edited`) targeting `main`.

> **Why `pull_request_target`?** Most contributions come from forks. The `pull_request` event gives a read-only `GITHUB_TOKEN` for fork PRs, which cannot merge. `pull_request_target` runs in the context of the base repo and has write access. This is safe because the validation script never executes code from the PR — it only reads the diff via the GitHub API.

**Steps**:
1. Checkout the base branch (not the PR branch — security measure with `pull_request_target`)
2. Set up Python + uv
3. Run the validation script: `uv run python scripts/review_pr.py`
4. On exit 0: squash-merge the PR directly (no approval step needed)
5. On non-zero exit: do nothing

> **Why no approval step?** The default `GITHUB_TOKEN` cannot submit an approving review on a PR triggered by the same workflow context. Since the repo does not require branch protection approvals, the workflow merges directly.

**Permissions**: `contents: write`, `pull-requests: write`.

**Concurrency**: No special concurrency controls needed — each PR runs independently.

## Component 2: Validation Script (`scripts/review_pr.py`)

A single Python script using `PyGithub` (already a project dependency) and `urllib.request` from the standard library (for URL reachability checks).

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
- From the PR diff via the GitHub API (not from a local checkout of the PR branch).
- Extract only lines added to `README.md`.
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
- Search the current `README.md` (from the base branch) for the project name (case-insensitive).
- Search for all URLs found in the entry.
- Query the GitHub API for open and recently closed PRs that contain the same project name or URL.
- If any match is found → skip.

#### 7. Section Placement Check
- Verify the entry is placed under a valid `##` (language) and `###` (category) heading.
- The entry must not be floating outside a recognized section.

#### 8. Activity Check
For any GitHub URL found in the entry (primary URL or `[GitHub](url)` link):
- Fetch the repo via GitHub API.
- `archived == true` → skip.
- Last push date older than 365 days from the workflow run date → skip.
- No README file in the repo → skip.

If the entry has **no GitHub URL at all** (e.g., a CRAN-only or PyPI-only entry without a `[GitHub]` link), skip auto-merge and leave for manual review. Activity cannot be verified without a GitHub repo.

#### 9. URL Reachability
- Verify the primary URL returns a non-error HTTP status (2xx or 3xx).
- Uses `urllib.request` with a 10-second timeout.

### Output
- Prints a structured summary to stdout (pass/fail per check) for workflow logs.
- Exit code 0 = all passed, non-zero = at least one check failed.

## Component 3: Merge & Notification Flow

### On All Checks Pass (exit 0)
1. The workflow squash-merges the PR to `main` with commit message: `Add [Project Name] (#PR_NUMBER)`.
2. A merge comment is posted: *"All checks passed. Thanks for the contribution!"*
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
- `urllib.request` — standard library, no installation needed
- No new dependencies

## Security Considerations

- The `GITHUB_TOKEN` provided by GitHub Actions has scoped permissions (only `contents: write` and `pull-requests: write`).
- Uses `pull_request_target` for fork write access, but the workflow checks out the **base branch only** — never the PR branch. The validation script reads the PR diff via the GitHub API, never executing PR code locally.
- URL reachability checks use HEAD/GET requests only via `urllib.request`.
