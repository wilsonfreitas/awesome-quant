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

### Step 4: Validate each added entry

For every new line added to `README.md`, check the following:

#### 4a. Entry format

Each entry MUST match this exact pattern:

```
- [Project Name](https://url) - Short description ending with a period.
```

Specifically:
- Starts with `- ` (dash + space)
- Followed by a markdown link `[Name](URL)`
- Followed by ` - ` (space, dash, space)
- Followed by a description that ends with a period `.`

The regex used by `parse.py` to extract entries is: `^\s*- \[(.*)\]\((.*)\) - (.*)$`

If the entry doesn't match, report exactly what's wrong (missing period, wrong separator, etc.).

#### 4b. URL validation

- **GitHub URLs are preferred.** If the URL points to `github.com`, that's ideal — no warning needed.
- **Non-GitHub URLs**: If the URL points somewhere else (PyPI, personal site, docs site, etc.), flag it with a warning: "This is not a GitHub URL. GitHub repos are preferred because they allow automated tracking of activity and archive status. Consider whether a GitHub link exists for this project."
- Check that the URL looks well-formed (starts with `https://`).

#### 4c. Section placement

Look at which `##` (language) and `###` (category) heading the entry was added under. Evaluate whether the project fits that section based on its description and URL:

- Does the project's language match the section? (e.g., a Python library should be under `## Python`)
- Does the project's purpose match the category? (e.g., a backtesting framework should be under `### Trading & Backtesting`, not `### Indicators`)
- If the placement seems wrong, suggest a better section.

The current sections in the README are:

**Python**: Numerical Libraries & Data Structures, Financial Instruments and Pricing, Indicators, Trading & Backtesting, Risk Analysis, Factor Analysis, Sentiment Analysis, Quant Research Environment, Time Series, Calendars, Data Sources, Excel Integration, Visualization

**R**: Numerical Libraries & Data Structures, Data Sources, Financial Instruments and Pricing, Trading, Backtesting, Risk Analysis, Factor Analysis, Time Series, Calendars

**Other languages**: Matlab, Julia, Java, JavaScript, Haskell, Scala, Ruby, Elixir/Erlang, Golang, CPP, CSharp, Rust

**Cross-language**: Frameworks, Reproducing Works Training & Books

If the project doesn't fit any existing section, suggest the closest match or recommend creating a new subsection (rare).

#### 4d. Duplicate check

Grep the current `README.md` for the project name and URL to ensure it's not already listed.

### Step 5: Summarize findings

Present a clear summary:

```
PR #<number>: <title>
Author: <author>
Created: <date>

Entries reviewed: <count>

<For each entry>
  - [Name](URL) - Description
    Format: OK / ISSUE: <details>
    URL: GitHub / WARNING: Non-GitHub URL (<domain>)
    Section: OK (<section>) / SUGGESTION: Move to <section>
    Duplicate: No / YES: Already listed at line <N>
</For each entry>

Conflicts: None / YES: Needs rebase

Verdict: APPROVE / NEEDS CHANGES
```

### Step 6: Take action

- **If everything passes**: Ask the user for confirmation, then approve and merge the PR.
- **If there are issues**: Leave a constructive review comment on the PR listing what needs to be fixed. Be polite and specific — these are open-source contributors.

When leaving comments, be friendly and grateful for the contribution. Example tone:
> Thanks for the contribution! A couple of things to address before we can merge:
> - The description should end with a period.
> - Consider linking to the GitHub repo instead of the docs site so we can track activity.
