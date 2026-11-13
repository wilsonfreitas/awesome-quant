from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestWorkflowContractTests(unittest.TestCase):
    def test_offline_suite_runs_without_write_credentials(self):
        path = ROOT / '.github/workflows/tests.yml'
        self.assertTrue(path.exists(), 'offline suite workflow is missing')
        workflow = path.read_text()
        for required in ('pull_request:', 'push:', 'branches: [main]', 'workflow_dispatch:',
                         'contents: read', 'persist-credentials: false', 'python-version: "3.11"',
                         'uv sync --frozen --no-install-project',
                         'uv run python -m unittest discover -s tests -q'):
            self.assertIn(required, workflow)
        for forbidden in ('pull_request_target', 'write', 'secrets.', 'github.token',
                          'GITHUB_TOKEN', 'paths:', 'paths-ignore:'):
            self.assertNotIn(forbidden, workflow)

    def test_production_tracks_helper_and_dependency_changes(self):
        workflow = (ROOT / '.github/workflows/build.yml').read_text()
        for path in ('scripts/readme_entries.py', 'scripts/pypi_metadata.py', 'pyproject.toml',
                     'uv.lock', '.github/workflows/build.yml'):
            self.assertIn(f"- '{path}'", workflow)
        self.assertIn('uv run python site/generate.py --source csv', workflow)
        self.assertLess(workflow.index('uv run python parse.py'), workflow.index('uv run python site/generate.py'))
        self.assertIn('publish_dir: site', workflow)

    def test_pr_preview_tracks_code_and_explicit_readme_input(self):
        workflow = (ROOT / '.github/workflows/pr-validate.yml').read_text()
        for path in ('parse.py', 'tests/**', '.agents/**', 'pyproject.toml', 'uv.lock'):
            self.assertIn(f"- '{path}'", workflow)
        self.assertIn('uv run python site/generate.py --source readme', workflow)
