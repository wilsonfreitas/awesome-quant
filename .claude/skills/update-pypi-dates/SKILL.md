---
name: update-pypi-dates
description: Check PyPI projects for last updated dates and update README.md entries. Use this skill to keep PyPI project information current with latest release dates from PyPI. Run periodically to maintain up-to-date metadata on Python packages listed in awesome-quant.
---

# Update PyPI Dates

Automatically check PyPI projects for their latest update dates and update corresponding README.md entries with the "(Last updated: YYYY-MM-DD)" information.

## How it works

The skill maintains a list of PyPI projects in awesome-quant and:
1. Queries the PyPI JSON API for each package
2. Extracts the last release date
3. Updates README.md entries with the new date if changed
4. Commits changes to git if updates were made

## PyPI Projects to Track

Current projects tracked:
- qfrm
- chinesestockapi
- tushare
- metatrader5

## Steps

### 1. Fetch PyPI data for each project

For each PyPI project, query: `https://pypi.org/pypi/{package_name}/json`

Extract the last release date from the releases data.

### 2. Update README.md entries

For each project with a new date:
- Find the entry in README.md
- Update or add the "(Last updated: YYYY-MM-DD)" note
- Use the exact entry format: `(Last updated: 2024-08-27)`

### 3. Verify changes

Show the user:
- Which packages were checked
- Which packages have new update dates
- The differences (old date → new date)

### 4. Commit if changes detected

If any updates were made:
```bash
git add README.md non-github-urls.md
git commit -m "Update PyPI project last updated dates"
git push origin main
```

## Usage

The user can:
- Run the skill directly: `/update-pypi-dates`
- Schedule it to run weekly/monthly via cron
- Include it in CI/CD pipelines to keep data fresh

## Script

Use `scripts/check_pypi_dates.sh` for the core update logic.
