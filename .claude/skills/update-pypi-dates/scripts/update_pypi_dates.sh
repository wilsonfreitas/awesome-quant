#!/bin/bash
# Wrapper script to check PyPI dates and update README.md

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"

cd "$PROJECT_ROOT" || exit 1

echo "🚀 Starting PyPI date update check..."
python3 "$SCRIPT_DIR/check_pypi_dates.py"
exit_code=$?

if [ $exit_code -eq 0 ]; then
    # Check if there are any changes to commit
    if git diff --quiet README.md; then
        echo "✓ No changes needed"
    else
        echo ""
        echo "📝 Changes detected, committing..."
        git add README.md
        git commit -m "Update PyPI project last updated dates"
        git push origin main
        echo "✅ Changes pushed to remote"
    fi
fi

exit $exit_code
