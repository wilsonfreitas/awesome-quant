"""Execute the workflow's restore shell against a fake Git transport, offline."""
import os
from fnmatch import fnmatchcase
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BuildMetadataCacheTests(unittest.TestCase):
    def test_shared_metadata_changes_trigger_build_and_pr_validation(self):
        for name in ('build.yml', 'pr-validate.yml'):
            workflow = (ROOT / '.github/workflows' / name).read_text()
            paths = [line.strip()[3:-1] for line in workflow.splitlines()
                     if line.strip().startswith("- '")]
            self.assertTrue(any(fnmatchcase('scripts/metadata.py', path) for path in paths), name)

    def restore(self, scenario):
        workflow = (ROOT / '.github/workflows/build.yml').read_text()
        marker = '    - name: Restore published metadata\n      run: |\n'
        self.assertIn(marker, workflow, 'CI must restore its published observations before enrichment')
        block = workflow.split(marker, 1)[1].split('    - ', 1)[0]
        command = '\n'.join(line[8:] for line in block.splitlines())
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / 'site').mkdir()
            (directory / 'bin').mkdir()
            (directory / 'published.csv').write_text('project,stars\nEngine,42\n')
            git = directory / 'bin/git'
            git.write_text('''#!/bin/sh
case "$1" in
  ls-remote)
    [ "$SCENARIO" = unreachable ] && exit 1
    [ "$SCENARIO" = first ] || echo 'abc refs/heads/gh-pages'
    ;;
  fetch) [ "$SCENARIO" != fetch-failed ] || exit 1 ;;
  ls-tree)
    [ "$*" = 'ls-tree --name-only FETCH_HEAD -- projects.csv' ] || exit 99
    [ "$SCENARIO" != inspection-failed ] || exit 128
    [ "$SCENARIO" = no-csv ] || echo 'projects.csv'
    ;;
  show)
    [ "$SCENARIO" != show-failed ] || exit 1
    cat "$PUBLISHED_CSV"
    ;;
  *) exit 99 ;;
esac
exit 0
''')
            git.chmod(0o755)
            env = dict(os.environ, SCENARIO=scenario, PUBLISHED_CSV=str(directory / 'published.csv'),
                       RUNNER_TEMP=tmp, PATH=str(directory / 'bin') + os.pathsep + os.environ['PATH'])
            result = subprocess.run(['bash', '-e', '-o', 'pipefail', '-c', command], cwd=directory,
                                    env=env, capture_output=True, text=True)
            csv_path = directory / 'site/projects.csv'
            return result, csv_path.read_text() if csv_path.exists() else None

    def test_published_csv_is_restored_before_parser(self):
        result, content = self.restore('published')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(content, 'project,stars\nEngine,42\n')
        workflow = (ROOT / '.github/workflows/build.yml').read_text()
        self.assertLess(workflow.index('- name: Restore published metadata'), workflow.index('- name: Run parser'))

    def test_first_build_and_missing_csv_degrade_to_no_observations(self):
        for scenario in ('first', 'no-csv'):
            with self.subTest(scenario=scenario):
                result, content = self.restore(scenario)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIsNone(content)

    def test_transport_failures_stop_build_instead_of_losing_cache(self):
        for scenario in ('unreachable', 'fetch-failed', 'show-failed'):
            with self.subTest(scenario=scenario):
                result, content = self.restore(scenario)
                self.assertNotEqual(result.returncode, 0)
                self.assertIsNone(content)

    def test_tree_inspection_failure_stops_build_instead_of_losing_cache(self):
        result, content = self.restore('inspection-failed')
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNone(content)
