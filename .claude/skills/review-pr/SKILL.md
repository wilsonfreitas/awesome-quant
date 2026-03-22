---
name: review-pr
description: Review and validate pull requests that add new library entries to the awesome-quant README.md. Use this skill whenever the user asks to review PRs, check contributions, validate submissions, triage pull requests, or mentions anything about incoming entries or additions to the curated list. Also triggers for "review pr", "check prs", "merge contributions", or any PR-related workflow in this repo.
---

# Review PR Skill

Review one open pull request at a time for the awesome-quant curated list. Always start with the oldest unreviewed open PR.

## Workflow

### Step 1: Find the oldest open PR

Use the GitHub MCP tools to list open pull requests sorted by creation date (ascending). Pick the oldest one. Show the user which PR you're reviewing (number, title, author, creation date).

### Step 2: Check for merge conflicts

Use the GitHub MCP tools to read the PR details. If the PR has merge conflicts, report this to the user and stop — the contributor needs to resolve conflicts before review can proceed. Leave a polite comment asking them to rebase.

### Step 3: Fetch the diff and extract added lines

Read the PR diff. Focus only on changes to `README.md`. If the PR modifies files other than `README.md` (like `parse.py`, `site/`, etc.), flag this as unusual — most contributions should only touch `README.md`.

### Step 4: Automatic rejection checks

Reject the PR immediately (close with a polite comment) if any of these apply:

- **Multiple projects in one PR** — each PR should add exactly one project.
- **Empty PR description** — the contributor must explain what they're adding.
- **Duplicate** — the project name or URL is already in `README.md` or in a recently closed PR.
- **Archived or abandoned** — the project has no activity in 12+ months.

### Step 5: Validate each added entry

For every new line added to `README.md`, check the following:

#### 5a. Entry format

Each entry MUST match one of these accepted formats:

**GitHub project:**
```
- [Project Name](https://github.com/owner/repo) - Short description ending with a period.
```

**Project with website and GitHub repo:**
```
- [Project Name](https://project-site.com) - Short description ending with a period. [GitHub](https://github.com/owner/repo)
```

**CRAN project (with optional GitHub link):**
```
- [Package Name](https://cran.r-project.org/package=pkgname) - Short description ending with a period.
- [Package Name](https://cran.r-project.org/package=pkgname) - Short description ending with a period. [GitHub](https://github.com/owner/repo)
```

**PyPI project (with optional GitHub link):**
```
- [package-name](https://pypi.org/project/package-name/) - Short description ending with a period.
- [package-name](https://pypi.org/project/package-name/) - Short description ending with a period. [GitHub](https://github.com/owner/repo)
```

The core regex used by `parse.py` to extract entries is: `^\s*- \[(.*)\]\((.*)\) - (.*)$`

Specifically check:
- Starts with `- ` (dash + space)
- Followed by a markdown link `[Name](URL)`
- Followed by ` - ` (space, dash, space)
- Followed by a description that ends with a period `.`
- The period must come before the optional `[GitHub](url)` link
- The `[GitHub]` link, if present, must use the exact format `[GitHub](https://github.com/owner/repo)`

If the entry doesn't match, report exactly what's wrong (missing period, wrong separator, etc.).

#### 5b. URL validation

- **GitHub URLs are preferred.** If the primary URL points to `github.com`, that's ideal.
- **CRAN URLs** (`cran.r-project.org`) are acceptable for R packages.
- **PyPI URLs** (`pypi.org`) are acceptable for Python packages.
- **Non-GitHub URLs with `[GitHub]` link**: If the primary URL is a project website but includes a `[GitHub](url)` link in the description, that's the preferred format for non-GitHub projects.
- **Non-GitHub URLs without `[GitHub]` link**: Flag with a suggestion to add a `[GitHub](url)` link if one exists, since GitHub repos enable automated tracking of stars and activity.
- All URLs must use `https://`.

#### 5c. Section placement

Look at which `##` (language) and `###` (category) heading the entry was added under. Evaluate whether the project fits that section:

- Does the project's language match the section? (e.g., a Python library should be under `## Python`)
- Does the project's purpose match the category? (e.g., a backtesting framework should be under `### Trading & Backtesting`, not `### Indicators`)
- Commercial/proprietary projects must go under `## Commercial & Proprietary Services`.
- If the placement seems wrong, suggest a better section.

The current sections in the README are:

**Python**: Numerical Libraries & Data Structures, Financial Instruments and Pricing, Indicators, Trading & Backtesting, Risk Analysis, Factor Analysis, Sentiment Analysis, Quant Research Environment, Time Series, Calendars, Data Sources, Excel Integration, Visualization

**R**: Numerical Libraries & Data Structures, Data Sources, Financial Instruments and Pricing, Trading, Backtesting, Risk Analysis, Factor Analysis, Time Series, Calendars

**Other languages**: Matlab, Julia, Java, JavaScript, Haskell, Scala, Ruby, Elixir/Erlang, Golang, CPP, CSharp, Rust

**Cross-language**: Frameworks, Reproducing Works Training & Books

**Commercial & Proprietary Services**

If the project doesn't fit any existing section, suggest the closest match or recommend creating a new subsection (rare).

#### 5d. Duplicate check

Grep the current `README.md` for the project name and URL to ensure it's not already listed.

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

- **If everything passes**: Ask the user for confirmation, then approve and merge the PR.
- **If there are fixable issues**: Leave a constructive review comment on the PR listing what needs to be fixed. Be polite and specific — these are open-source contributors. Link to `CONTRIBUTING.md` for reference.
- **If it should be rejected** (automatic rejection criteria): Close the PR with a polite explanation and link to `CONTRIBUTING.md`.

When leaving comments, be friendly and grateful for the contribution. Example tone:
> Thanks for the contribution! A couple of things to address before we can merge:
> - The description should end with a period.
> - Consider adding a `[GitHub](url)` link so we can track activity.
>
> Please see our [contributing guidelines](https://github.com/wilsonfreitas/awesome-quant/blob/master/CONTRIBUTING.md) for the accepted entry formats.
