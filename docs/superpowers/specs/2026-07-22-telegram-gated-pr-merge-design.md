# Telegram-Notified, GitHub-Gated PR Merge — Design Spec

**Date:** 2026-07-22  
**Status:** Approved for planning

## Overview

Replace direct automatic merging in the PR reviewer workflow with a human approval gate. When `scripts/review_pr.py` passes, the workflow sends the maintainer a Telegram notification and creates a merge job that waits for approval through a protected GitHub Environment. Approval remains inside GitHub and works from GitHub Mobile on iPhone.

The Telegram message is informational. It never contains credentials and cannot itself authorize a merge.

## Goals

- Never merge solely because the deterministic reviewer passed.
- Notify the maintainer on Telegram whenever a PR becomes eligible for approval.
- Allow approval or rejection from GitHub Mobile.
- Bind approval to one workflow run and one PR head commit.
- Revalidate immediately before merging and fail closed if state changed.

## Non-Goals

- Approving or merging directly inside Telegram.
- Sending Telegram messages for failed reviews.
- Automatically commenting on or closing rejected PRs.
- Expanding the deterministic acceptance rules in `scripts/review_pr.py`.

## Workflow

The existing workflow is split into three jobs:

1. **Review:** Run `scripts/review_pr.py` against the PR using the base-branch implementation. Record the PR number, title, author, URL, and exact head SHA.
2. **Notify:** If review passes, call Telegram's `sendMessage` API using repository secrets. Include an inline URL button that opens the exact GitHub Actions run.
3. **Approve and merge:** Reference the protected `auto-merge-approval` GitHub Environment. GitHub holds this job until a required reviewer approves or rejects it. After approval, verify the PR is open and its head SHA is unchanged, rerun the reviewer against current base state, confirm mergeability, and squash-merge using the captured SHA.

Any error, ambiguity, stale SHA, failed revalidation, rejected deployment, or merge conflict prevents the merge.

## Telegram Message

The message clearly distinguishes eligibility from approval:

> Deterministic PR checks passed. Human approval is required.
>
> PR #123 — Project title  
> Author: contributor  
> Commit: abc1234

It includes links to the PR and the exact workflow run. The workflow escapes all contributor-controlled fields for Telegram's selected parse mode, or sends plain text, so titles and usernames cannot alter message markup.

## GitHub Environment

Create a repository Environment named `auto-merge-approval` with the maintainer as a required reviewer. GitHub Mobile displays protected-environment review requests and supports approving or rejecting them on iPhone.

Self-review prevention remains disabled so maintainer-authored PRs can use the same mechanism. Environment approval waits expire according to GitHub's platform limit, currently 30 days.

## Secrets and Permissions

Repository Actions secrets:

- `TELEGRAM_BOT_TOKEN`: token issued by BotFather.
- `TELEGRAM_CHAT_ID`: the maintainer's destination chat ID.

The notification job needs no GitHub write permission. The merge job receives only the GitHub permissions required to inspect and merge the PR. Telegram receives public PR metadata only; GitHub tokens and repository secrets are never placed in message text or URLs.

The workflow continues using `pull_request_target` while checking out only trusted base-branch code. It never executes code from the contributor branch.

## Race and Failure Handling

- Existing per-PR concurrency cancels obsolete runs after a new commit or relevant PR edit.
- The merge call is pinned to the captured PR head SHA.
- Final revalidation catches duplicates or conflicts introduced while approval was pending.
- A failed Telegram request prevents the approval job from being created, ensuring the maintainer is not silently bypassed.
- A rejected or expired Environment review leaves the PR open.
- The workflow must inspect the merge API result and fail if GitHub declines the merge.

## Repository Setup

One-time manual configuration:

1. Create a Telegram bot and obtain its token.
2. Send the bot a message and determine the destination chat ID.
3. Add both values as repository Actions secrets.
4. Create the `auto-merge-approval` GitHub Environment.
5. Add the maintainer as a required reviewer.
6. Enable protected-deployment push notifications in GitHub Mobile.

## Verification

Tests cover pass/fail reviewer outcomes, Telegram-safe message construction, stale head SHA rejection, changed base-state revalidation, merge conflicts, and unsuccessful merge API responses.

A controlled test PR verifies the end-to-end behavior:

1. Passing review sends Telegram notification.
2. Merge job waits for Environment approval.
3. Rejection leaves the PR open.
4. Approval from GitHub Mobile runs final validation and merges.
5. Updating the PR while approval is pending makes the old run incapable of merging the new head.
