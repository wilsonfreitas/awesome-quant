---
name: review-pr
description: Review and validate pull requests that add new library entries to the awesome-quant README.md. Use this skill whenever the user asks to review PRs, check contributions, validate submissions, triage pull requests, or mentions anything about incoming entries or additions to the curated list. Also triggers for "review pr", "check prs", "merge contributions", or any PR-related workflow in this repo.
---

# Review PR Skill

Review one open pull request at a time for the awesome-quant curated list. Always start with the oldest unreviewed open PR.

**IMPORTANT: Always use GitHub MCP tools for all GitHub operations.** Do not fall back to bash commands like `gh` or other tools — use the GitHub MCP interface exclusively.

## Workflow

### Step 1: Find the oldest open PR

Use the `mcp__github__list_pull_requests` tool to list open pull requests sorted by creation date (ascending). Pick the oldest one. Show the user which PR you're reviewing (number, title, author, creation date).

### Step 2: Check for merge conflicts

Use the `mcp__github__pull_request_read` tool with method `get` to read the PR details. If the PR has merge conflicts, report this to the user and stop — the contributor needs to resolve conflicts before review can proceed. Use the `mcp__github__add_issue_comment` tool to leave a polite comment asking them to rebase.

### Step 3: Fetch the diff and extract added lines

Use the `mcp__github__pull_request_read` tool with method `get_diff` to read the PR diff. Focus only on changes to `README.md`. If the PR modifies files other than `README.md` (like `parse.py`, `site/`, etc.), flag this as unusual — most contributions should only touch `README.md`.

### Step 4: Automatic rejection checks

Reject the PR immediately (close with a polite comment) if any of these apply:

- **Multiple unrelated projects** — multiple projects should only be submitted together if they are closely related (same market/exchange, same author, same service, or address a specific domain gap). Check the PR description for clear rationale. If unrelated, ask the contributor to split into separate PRs.
- **Empty PR description** — the contributor must explain what they're adding and why (especially if multiple projects).
- **Duplicate entries** — the same project name or URL appears multiple times within the PR or already in `README.md`.
- **Archived or abandoned** — the project has no activity in 12+ months.

### Step 5: Validate each added entry

For every new line added to `README.md`, check the following:

#### 5a. Entry format

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

#### 5b. URL validation

- **GitHub URLs are preferred.** If the primary URL points to `github.com`, that's ideal.
- **CRAN URLs** (`cran.r-project.org`) are acceptable for R packages.
- **PyPI URLs** (`pypi.org`) are acceptable for Python packages.
- **Non-GitHub URLs with `[GitHub]` link**: If the primary URL is a project website but includes a `[GitHub](url)` link in the description, that's the preferred format for non-GitHub projects.
- **Non-GitHub URLs without `[GitHub]` link**: Flag with a suggestion to add a `[GitHub](url)` link if one exists, since GitHub repos enable automated tracking of stars and activity.
- All URLs must use `https://`.

#### 5c. Section placement

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

#### 5d. Duplicate check

Use the `mcp__github__get_file_contents` tool to fetch the current `README.md` from the repository, then search through it to ensure the project name and URL are not already listed.

#### 5e. Quality check

- **Active**: Project should show recent activity (commits within the last 12 months).
- **Documented**: Project should have a clear README with usage examples.

### Step 6: Summarize findings

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

### Step 7: Take action

Use GitHub MCP tools exclusively for all PR interactions:

- **If everything passes**: Ask the user for confirmation, then use the `mcp__github__merge_pull_request` tool to merge the PR.
- **If there are fixable issues**: Use the `mcp__github__add_issue_comment` tool to leave a constructive review comment on the PR listing what needs to be fixed. Be polite and specific — these are open-source contributors. Link to `CONTRIBUTING.md` for reference.
- **If it should be rejected** (automatic rejection criteria): Use the `mcp__github__update_pull_request` tool to close the PR with a polite explanation and link to `CONTRIBUTING.md`. Then leave a comment using `mcp__github__add_issue_comment` explaining the closure reason.

When leaving comments, be friendly and grateful for the contribution. Example tone:
> Thanks for the contribution! A couple of things to address before we can merge:
> - The description should end with a period.
> - Consider adding a `[GitHub](url)` link so we can track activity.
>
> Please see our [contributing guidelines](https://github.com/wilsonfreitas/awesome-quant/blob/main/CONTRIBUTING.md) for the accepted entry formats.

**For multiple-project PRs:** If entries have mixed results (some pass, some need fixes), list all issues together and ask the contributor to fix all at once rather than cherry-picking individual entries. If the relationship between projects isn't clear from the description, ask for clarification of why they should be grouped.
