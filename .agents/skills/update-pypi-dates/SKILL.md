---
name: update-pypi-dates
description: Refresh tracked PyPI last-updated dates in awesome-quant README.md. Use when the user asks to update PyPI dates, refresh PyPI metadata, or run update-pypi-dates.
---

# Update PyPI Dates

Refresh latest distribution-upload dates for selected PyPI packages in `README.md`.
The shared `scripts/pypi_metadata.py` helper selects the latest valid upload in
UTC across every release file, including prerelease and yanked files. This is
upload recency, not latest stable-version selection. Unavailable dates preserve
existing README notes.

## Workflow

1. Run the checker:

```bash
uv run python .agents/skills/update-pypi-dates/scripts/check_pypi_dates.py
```

2. Show the user which packages changed.
3. Run README validation:

```bash
uv run python scripts/validate_readme.py
```

4. If the user asked for a commit, stage only the relevant files and commit.
5. Do not push unless the user explicitly asks.

## Tracked Packages

The script currently tracks:

- `qfrm`
- `chinesestockapi`
- `tushare`
- `metatrader5` / `MetaTrader5`

To add packages, edit `PYPI_PROJECTS` in
`.agents/skills/update-pypi-dates/scripts/check_pypi_dates.py` (relative to the repo).
