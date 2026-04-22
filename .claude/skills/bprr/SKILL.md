---
name: bprr
description: Bulk review all unreviewed pull requests for the awesome-quant curated list. Review all open PRs without the "reviewed" label in one session, then present a summary table for user selection before merging. Use this skill when asked to "bulk review", "review all prs", "bprr", or "review unreviewed".
---

# Bulk PR Reviewer (bprr)

Review all open pull requests at once for the awesome-quant curated list, then present a summary and merge selected PRs.

**IMPORTANT: Always use GitHub MCP tools for all GitHub operations.** Do not fall back to bash commands like `gh` or other tools — use the GitHub MCP interface exclusively.

## Workflow

### Step 1: Fetch and filter PRs

1. Use `github_list_pull_requests` with `state=open`, `sort=created`, `direction=asc`, `per_page=30` to get all open PRs.

2. Filter out PRs that have the "reviewed" label (these were already commented on and are waiting for contributor response).

3. Report the count:
```
Found X open PRs total, Y unreviewed (no "reviewed" label)
```

### Step 2: Fetch current README (cache for duplicate checks)

1. Use `github_get_file_contents` owner=wilsonfreitas, repo=awesome-quant, path=README.md to fetch current README once.

2. Cache this for all duplicate checks during review.

### Step 3: Parallel PR review

For each unreviewed PR, fetch in parallel:
- `github_get_pull_request` for PR details (check mergeable status, labels)
- Use webfetch to fetch the diff from `https://github.com/wilsonfreitas/awesome-quant/pull/{number}.diff`

Then validate each entry using the logic from review-pr skill:

#### Entry format check

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

**CRAN project:**
```
- [Package Name](https://cran.r-project.org/package=pkgname) - `R` - Short description ending with a period.
```

**PyPI project:**
```
- [package-name](https://pypi.org/project/package-name/) - `Python` - Short description ending with a period.
```

The core regex: `^\s*- \[(.*)\]\((.*)\) - (.*)$`

Specifically check:
- Starts with `- ` (dash + space)
- Followed by markdown link `[Name](URL)`
- Followed by ` - ` (space, dash, space)
- **MUST include language tags in backticks** (e.g., `` `Python` ``) followed by ` - `
- Description ends with a period `.`
- The optional `[GitHub]` link comes after the period

#### URL validation check

- **GitHub URLs preferred**
- **CRAN URLs** (`cran.r-project.org`) acceptable for R packages
- **PyPI URLs** (`pypi.org`) acceptable for Python packages
- Non-GitHub URLs should have `[GitHub]` link in description
- All URLs must use `https://`

#### Section placement check

The README categories are:
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

#### Duplicate check

Search the cached README for the project name and URL to ensure not already listed.

#### Quality check

- Active: Recent commits within 12 months
- Documented: Clear README with examples

### Step 4: Present summary table

Format the results as:

```
## Bulk Review Summary

| # | Title | Author | Entries | Format | URL | Section | Duplicate | Verdict |
|---|-------|--------|---------|--------|-----|---------|-----------|---------|
| 335 | Apex Quant | sst19910323 | 1 | ISSUE | GitHub | Trading | No | NEEDS CHANGES |
| 336 | Alpha Skills | VernonOY | 1 | OK | GitHub | Factor | No | APPROVE |
...
```

For each PR, show:
- **Number** and title
- Author
- Entry count
- Format status (OK / ISSUE: details)
- URL type (GitHub / CRAN / PyPI / WARNING)
- Section placement (OK / SUGGESTION: move to X)
- Duplicate status (No / YES: line N)
- Overall verdict

After the table, ask:
```
Which PRs would you like to merge? (e.g., "336, 340" or "all approved")
```

### Step 5: User selection

Parse user response. Options:
- Specific PR numbers: "336, 340"
- "all approved" - merge all with APPROVE verdict
- "all" - merge all regardless of verdict
- "none" - skip merging

If user asks about a specific PR, provide details before asking novamente.

### Step 6: Merge selected PRs (confirm-each)

For each PR to merge:

1. Ask confirmation: "Merge PR #336? (Alpha Skills)"
2. Wait for user "yes"/"no"
3. If yes: use `github_merge_pull_request` with merge_method="squash"
4. Report success/failure

**Note:** Do NOT auto-merge without explicit user confirmation for each PR.

### Automatic rejection criteria

Reject immediately (close with polite comment) if:
- Multiple unrelated projects without clear rationale
- Empty PR description
- Duplicate entry already in README
- Archived/abandoned project (no commits in 12+ months)

For fixable issues (missing language tag, wrong section), comment and add "reviewed" label instead.

## GitHub MCP Tool Reference

Key tools:
- `github_list_pull_requests` - list open PRs
- `github_get_pull_request` - get PR details
- `github_add_issue_comment` - comment on PR
- `github_merge_pull_request` - merge PR
- `github_update_issue` - add label / close PR
- `github_get_file_contents` - fetch README for duplicate check