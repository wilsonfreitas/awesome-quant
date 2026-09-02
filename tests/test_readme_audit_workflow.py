import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).parents[1] / ".github/workflows/readme-audit.yml"


class ReadmeAuditWorkflowTests(unittest.TestCase):
    def test_workflow_matches_the_scheduled_audit_contract(self):
        expected = """name: README Audit

on:
    schedule:
        - cron: "0 9 * * 1"
    workflow_dispatch:

permissions:
    contents: read
    issues: write

concurrency:
    group: readme-audit
    cancel-in-progress: false

jobs:
    audit:
        runs-on: ubuntu-latest
        timeout-minutes: 30
        steps:
            - uses: actions/checkout@v4
              with:
                  fetch-depth: 1
                  persist-credentials: false
            - uses: astral-sh/setup-uv@v6
            - uses: actions/setup-python@v5
              with:
                  python-version: "3.11"
            - name: Install dependencies
              run: uv sync --frozen --no-install-project
            - name: Audit README links and repositories
              env:
                  GITHUB_TOKEN: ${{ github.token }}
                  GITHUB_REPOSITORY: ${{ github.repository }}
              run: uv run python scripts/audit_readme.py --readme README.md
"""

        self.assertEqual(WORKFLOW_PATH.read_text(encoding="utf-8"), expected)


if __name__ == "__main__":
    unittest.main()
