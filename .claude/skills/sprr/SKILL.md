---
name: sprr
description: Single PR reviewer. Review and validate pull requests that add new library entries to the awesome-quant README.md. Use this skill whenever the user asks to review PRs, check contributions, validate submissions, triage pull requests, or mentions anything about incoming entries or additions to the curated list. Also triggers for "review pr", "check prs", "merge contributions", "sprr", or any PR-related workflow in this repo.
---

# SPRR: Single PR Reviewer

Review and validate PRs that add new library entries to the awesome-quant README.md.

## CRITICAL RULES

### 1. Only Review PRs You Are Asked To Review
- **NEVER** proactively find or review other PRs on your own
- Only review the specific PR number you are asked to review
- If no PR number is given, ask the user which PR to review
- Do NOT auto-select the oldest PR or any PR - wait for explicit instruction

### 2. Never Modify PRs Without User Consent
- **NEVER** comment on, merge, close, label, or take any action on a PR without explicit user approval
- Present your findings and ask "Should I proceed?" or similar
- Wait for user confirmation before taking any action that modifies the PR
- The user must explicitly say "yes", "proceed", "go ahead", etc. before you act

### 3. Be Strict With CONTRIBUTING.md
- Enforce ALL format requirements from CONTRIBUTING.md
- Do not accept requests that deviate from the established format
- Reject entries that don't match the required format, even for small issues
- Point contributors to CONTRIBUTING.md for exact requirements

**IMPORTANT: Always use GitHub MCP tools for all GitHub operations.** Do not fall back to bash commands like `gh` or other tools — use the GitHub MCP interface exclusively.

## Workflow

### Step 1: Confirm the PR (if not given)

If the user provides a PR number, confirm it. If not, ask the user which PR they want you to review. DO NOT auto-select a PR.

### Step 2: Check for merge conflicts

Use the `mcp__github__pull_request_read` tool with method `get` to read the PR details. If the PR has merge conflicts, report this to the user and stop — the contributor needs to resolve conflicts before review can proceed. Use the `mcp__github__add_issue_comment` tool to leave a polite comment asking them to rebase.

### Step 3: Check for prior review

Use `github_get_pull_request` to check for the "reviewed" label, then use `github_get_pull_request_comments` to check for comments from maintainer.

Report at start of review:
```
Prior review: YES/NO
- Label: "reviewed" present (if yes)
- Comments: X new comments from maintainer (if any)
- Status: Full revalidation proceeding
```

Always proceed with full validation regardless of prior review status.

### Step 4: Fetch the diff and extract added lines

Use the `mcp__github__pull_request_read` tool with method `get_diff` to read the PR diff. Focus only on changes to `README.md`. If the PR modifies files other than `README.md` (like `parse.py`, `site/`, etc.), flag this as unusual — most contributions should only touch `README.md`.

### Step 5: Automatic rejection checks

Reject the PR immediately (close with a polite comment) if any of these apply:

- **Multiple unrelated projects** — multiple projects should only be submitted together if they are closely related (same market/exchange, same author, same service, or address a specific domain gap). Check the PR description for clear rationale. If unrelated, ask the contributor to split into separate PRs.
- **Empty PR description** — the contributor must explain what they're adding and why (especially if multiple projects).
- **Duplicate entries** — the same project name or URL appears multiple times within the PR or already in `README.md`.
- **Archived or abandoned** — the project has no activity in 12+ months.

### Step 6: Validate each added entry

For every new line added to `README.md`, check the following:

#### 6a. Entry format

Each entry MUST include one or more language tags and match one of these accepted formats:

**Single language:**
```
- [Project Name](https://github.com/owner/repo) - `Python` - Short description ending with a period.
```

**Multiple languages:**
```
- [Project Name](https://github.com/owner/repo) - `Python` `Rust` - Short description ending with a period.
```

**Project with website and GitHub repo:**
```
- [Project Name](https://project-site.com) - `Python` - Short description ending with a period. [GitHub](https://github.com/owner/repo)
```

**CRAN project (with optional GitHub link):**
```
- [Package Name](https://cran.r-project.org/package=pkgname) - `R` - Short description ending with a period.
- [Package Name](https://cran.r-project.org/package=pkgname) - `R` - Short description ending with a period. [GitHub](https://github.com/owner/repo)
```

**PyPI project (with optional GitHub link):**
```
- [package-name](https://pypi.org/project/package-name/) - `Python` - Short description ending with a period.
- [package-name](https://pypi.org/project/package-name/) - `Python` - Short description ending with a period. [GitHub](https://github.com/owner/repo)
```

The core regex used by `parse.py` to extract entries is: `^\s*- \[(.*)\]\((.*)\) - (.*)$`

Specifically check:
- Starts with `- ` (dash + space)
- Followed by a markdown link `[Name](URL)`
- Followed by ` - ` (space, dash, space)
- **MUST include one or more language tags in backticks** (e.g., `` `Python` ``, `` `Python` `Rust` ``) followed by ` - `
- Followed by a description that ends with a period `.`
- The period must come before the optional `[GitHub](url)` link
- The `[GitHub]` link, if present, must use the exact format `[GitHub](https://github.com/owner/repo)`

If the entry doesn't match, report exactly what's wrong (missing language tags, missing period, wrong separator, etc.).

#### 6b. URL validation

- **GitHub URLs are preferred.** If the primary URL points to `github.com`, that's ideal.
- **CRAN URLs** (`cran.r-project.org`) are acceptable for R packages.
- **PyPI URLs** (`pypi.org`) are acceptable for Python packages.
- **Non-GitHub URLs with `[GitHub]` link**: If the primary URL is a project website but includes a `[GitHub](url)` link in the description, that's the preferred format for non-GitHub projects.
- **Non-GitHub URLs without `[GitHub]` link**: Flag with a suggestion to add a `[GitHub](url)` link if one exists, since GitHub repos enable automated tracking of stars and activity.
- All URLs must use `https://`.

#### 6c. Section placement

The README is now organized by **category** (not by language). Look at which `##` (category) heading the entry was added under. Evaluate whether the project fits that section:

- Does the project's purpose match the category? (e.g., a backtesting framework should be under `## Trading & Backtesting`, not under `## Technical Indicators`)
- Commercial/proprietary projects must go under `## Commercial & Proprietary Services`.
- If the placement seems wrong, suggest a better section.

The current category sections in the README are:

1. Numerical Libraries & Data Structures
2. Financial Instruments & Pricing
3. Technical Indicators
4. Trading & Backtesting
5. Portfolio Optimization & Risk Analysis
6. Factor Analysis
7. Sentiment Analysis & Alternative Data
8. Time Series Analysis
9. Market Data & Data Sources
10. Prediction Markets
11. Calendars & Market Hours
12. Visualization
13. Excel & Spreadsheet Integration
14. Quant Research Environments
15. Cross-Language Frameworks
16. Reproducing Works, Training & Books
17. Commercial & Proprietary Services
18. Related Lists

If the project doesn't fit any existing section, suggest the closest match or recommend creating a new category section (rare).

#### 6d. Duplicate check

Use the `mcp__github__get_file_contents` tool to fetch the current `README.md` from the repository, then search through it to ensure the project name and URL are not already listed.

#### 6e. Quality check

- **Active**: Project should show recent activity (commits within the last 12 months).
- **Documented**: Project should have a clear README with usage examples.

### Step 7: Summarize findings

Present a clear summary:

```
PR #<number>: <title>
Author: <author>
Created: <date>

Entries reviewed: <count>

<For each entry>
  - [Name](URL) - Description
    Format: OK / ISSUE: <details>
    URL: GitHub / CRAN / PyPI / WARNING: <details>
    Section: OK (<section>) / SUGGESTION: Move to <section>
    Duplicate: No / YES: Already listed at line <N>
    Quality: OK / WARNING: <details>
</For each entry>

Conflicts: None / YES: Needs rebase

Verdict: APPROVE / NEEDS CHANGES / REJECT
```

### Step 8: Present findings and ask for user consent

**NEVER take any action that modifies the PR without user consent.** Present your findings and ask for explicit approval before proceeding.

Use GitHub MCP tools exclusively for all PR interactions:

- **If everything passes**: Present summary and ask "Should I merge this PR?" (or similar). ONLY merge after user explicitly says yes.
- **If there are fixable issues**: Present summary and ask "Should I leave a comment listing these issues?" ONLY comment after user explicitly says yes.
- **If it should be rejected** (automatic rejection criteria): Present summary and ask "Should I close this PR with a rejection reason?" ONLY close after user explicitly says yes.

When leaving comments, be friendly and grateful for the contribution. Example tone:
> Thanks for the contribution! A couple of things to address before we can merge:
> - The description should end with a period.
> - Consider adding a `[GitHub](url)` link so we can track activity.
>
> Please see our [contributing guidelines](https://github.com/wilsonfreitas/awesome-quant/blob/main/CONTRIBUTING.md) for the accepted entry formats.

**For multiple-project PRs:** If entries have mixed results (some pass, some need fixes), list all issues together and ask the contributor to fix all at once rather than cherry-picking individual entries. If the relationship between projects isn't clear from the description, ask for clarification of why they should be grouped.
