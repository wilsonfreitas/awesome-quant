---
name: update-pypi-dates
description: Refresh tracked PyPI last-updated dates in awesome-quant README.md. Use when the user asks to update PyPI dates, refresh PyPI metadata, or run update-pypi-dates.
---

# Update PyPI Dates

Refresh last release dates for selected PyPI packages listed in `README.md`.

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

To add packages, edit `PYPI_PROJECTS` in `scripts/check_pypi_dates.py`.
