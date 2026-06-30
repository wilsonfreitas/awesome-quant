#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "$script_dir/../../../.." && pwd)"

cd "$project_root"
uv run python "$script_dir/check_pypi_dates.py"
uv run python scripts/validate_readme.py
