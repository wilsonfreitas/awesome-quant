import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "pr-review.yml"
EXPECTED_WORKFLOW = """name: PR Review

on:
    pull_request_target:
        branches: [main]
        types: [opened, synchronize, reopened, edited]

permissions:
    contents: read
    pull-requests: read

concurrency:
    group: ${{ github.workflow }}-${{ github.event.pull_request.number }}
    cancel-in-progress: true

jobs:
    validate:
        runs-on: ubuntu-latest
        timeout-minutes: 10
        steps:
            - uses: actions/checkout@v4
              with:
                  ref: ${{ github.event.pull_request.base.sha }}
                  fetch-depth: 1
                  persist-credentials: false
            - uses: astral-sh/setup-uv@v6
            - uses: actions/setup-python@v5
              with:
                  python-version: "3.11"
            - name: Install dependencies
              run: uv sync --frozen --no-install-project
            - name: Review pull request
              env:
                  GITHUB_TOKEN: ${{ github.token }}
                  GITHUB_REPOSITORY: ${{ github.repository }}
                  PR_NUMBER: ${{ github.event.pull_request.number }}
              run: uv run python scripts/review_pr.py
"""


class PullRequestReviewWorkflowContractTests(unittest.TestCase):
    def test_matches_the_complete_read_only_security_contract(self):
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertEqual(workflow, EXPECTED_WORKFLOW)


if __name__ == "__main__":
    unittest.main()
