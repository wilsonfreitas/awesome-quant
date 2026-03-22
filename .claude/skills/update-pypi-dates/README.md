# Update PyPI Dates Skill

Automatically check PyPI projects for their latest update dates and keep README.md entries current.

## Overview

This skill monitors Python packages listed in awesome-quant and updates their entries with the latest release dates from PyPI. This ensures that outdated project information is easily identifiable.

## Features

- ✅ Checks 4 PyPI projects: qfrm, chinesestockapi, tushare, metatrader5
- ✅ Fetches latest release dates from PyPI API
- ✅ Updates README.md entries with `(Last updated: YYYY-MM-DD)` format
- ✅ Commits changes automatically when updates found
- ✅ No dependencies beyond Python standard library

## Usage

### Invoke from Claude Code

```bash
/update-pypi-dates
```

Or call the script directly:

```bash
./.claude/skills/update-pypi-dates/scripts/check_pypi_dates.py
```

### Manual Python Execution

```bash
python3 .claude/skills/update-pypi-dates/scripts/check_pypi_dates.py
```

### Bash Wrapper

```bash
./.claude/skills/update-pypi-dates/scripts/update_pypi_dates.sh
```

## How It Works

1. **Queries PyPI API** for each tracked package
2. **Extracts last release date** from the releases data
3. **Updates README.md** entries with format: `(Last updated: 2024-08-27)`
4. **Commits changes** if any updates were found

## Adding New Packages

To track additional PyPI packages, edit the `PYPI_PROJECTS` dictionary in `scripts/check_pypi_dates.py`:

```python
PYPI_PROJECTS = {
    "display_name": "pypi_package_name",
    # Add new entries here
}
```

Then update the skill description if needed.

## Output Examples

### No Changes
```
📦 Checking PyPI projects for last updated dates...

Checking qfrm...
  ✓ 2015-12-12 (no change)

✓ All packages up to date!
```

### With Updates
```
📦 Checking PyPI projects for last updated dates...

Checking tushare...
  ✓ 2024-08-27 (no change)
Checking metatrader5...
  ✅ Updated to 2026-02-20

📝 Found 1 update(s):
  - metatrader5: 2026-02-20

✅ Updated README.md
```

## Configuration

### Periodic Execution

Set up a cron job to run weekly:

```bash
# Add to crontab (runs Monday at 2 AM)
0 2 * * 1 cd /path/to/awesome-quant && ./.claude/skills/update-pypi-dates/scripts/update_pypi_dates.sh
```

Or use Claude Code's scheduling:

```bash
/loop 1w /update-pypi-dates
```

## Files

- `SKILL.md` - Skill definition and documentation
- `scripts/check_pypi_dates.py` - Main Python script
- `scripts/update_pypi_dates.sh` - Bash wrapper with git integration
- `README.md` - This file

## Requirements

- Python 3.6+
- Network access to PyPI API
- Git (for automatic commits)

## Error Handling

- Network timeouts: Gracefully skipped with warning
- Package not found: Skipped with message
- API errors: Logged and continued with other packages

## Future Enhancements

- [ ] Support for more PyPI packages
- [ ] GitHub Actions workflow integration
- [ ] Email notifications on updates
- [ ] Comparison with published versions in README
- [ ] Support for other package registries (npm, Ruby Gems, etc.)
