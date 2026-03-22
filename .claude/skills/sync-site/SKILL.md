---
name: sync-site
description: Sync site/index.qmd with README.md content. Use this skill whenever README.md has been updated and the site needs to reflect those changes — after merging PRs, editing entries, adding libraries, or any modification to README.md. Also triggers for "update site", "sync site", "deploy site", "update qmd", or mentions of site/index.qmd being out of date.
---

# Sync Site

Update `site/index.qmd` to match the current `README.md` content, then commit and push.

## How it works

`site/index.qmd` is composed of two parts:

1. **YAML frontmatter** (lines 1-11) — Quarto metadata that never changes. Preserve it exactly as-is.
2. **Body content** — Everything from `## Python` to the end of the file. This must match `README.md` from the `## Python` heading onward.

The preamble in README.md (title, badges, language table of contents) is intentionally excluded from `index.qmd` because the Quarto frontmatter replaces it.

## Steps

### 1. Extract the frontmatter from index.qmd

Read `site/index.qmd` and capture everything up to and including the closing `---` and the blank line + description + badge lines that follow it (lines 1-16).

The header looks like this:
```
---
title: "Awesome Quant"
...
---

A curated list of insanely awesome libraries, packages and resources for Quants (Quantitative Finance).

[![](https://awesome.re/badge.svg)](https://awesome.re)
```

### 2. Extract the body from README.md

Read `README.md` and capture everything starting from the line `## Python` (inclusive) to the end of the file.

### 3. Combine and write

Concatenate the frontmatter header and the README body, then write to `site/index.qmd`.

Use a shell script for reliability:

```bash
# Extract line number where "## Python" starts in README.md
START=$(grep -n '^## Python' README.md | head -1 | cut -d: -f1)

# Extract frontmatter + preamble from index.qmd (up to the badge line)
END=$(grep -n 'awesome.re/badge' site/index.qmd | head -1 | cut -d: -f1)

# Combine: header from qmd + body from README
{ head -n "$END" site/index.qmd; echo; tail -n +"$START" README.md; } > site/index.qmd.tmp
mv site/index.qmd.tmp site/index.qmd
```

### 4. Verify

Run a quick diff to confirm the update looks correct:

```bash
# Show line count to sanity-check
wc -l site/index.qmd

# Optionally diff the body portion to confirm they match
diff <(tail -n +"$START" README.md) <(sed -n "$((END+2)),\$p" site/index.qmd)
```

### 5. Commit and push

Stage, commit, and push the change:

```bash
git add site/index.qmd
git commit -m "Sync site/index.qmd with README.md"
git push origin master
```
