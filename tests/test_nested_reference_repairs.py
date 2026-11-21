import difflib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from github import GithubException

from scripts.readme_entries import iter_readme_entries, nested_reference_repairs
from scripts.validate_readme import validate_malformed_added_lines
from tests import test_review_pr as fixtures

OLD = (
    '  - Library - Python [package](https://pypi.org/project/demo/) '
    'and [C++](https://github.com/example/old)'
)
NEW = OLD.replace('/old)', '/new)')
PARENT = '- [Parent](https://github.com/example/parent) - `Python` - Toolkit.\n'
BASE = '## Trading & Backtesting\n' + PARENT + OLD + '\n'


class NestedReferenceRepairTests(unittest.TestCase):
    def review(self, head, *, base=BASE, identity=123):
        original = fixtures.FakeClient.get_repo
        def lookup(client, name):
            if identity is None and name == 'example/old':
                raise GithubException(404, {'message': 'Not Found'})
            repo = original(client, name)
            if name.startswith('example/'):
                repo.id = 123 if name.endswith('/old') else identity
            return repo
        patch_text = ''.join(difflib.unified_diff(
            base.splitlines(keepends=True), head.splitlines(keepends=True)
        ))
        with patch.object(fixtures.FakeClient, 'get_repo', lookup):
            return fixtures.ValidationPipelineTests().review(
                patch_text=patch_text, base_readme=base, head_readme=head
            )

    def test_existing_reference_only_repair(self):
        self.assertEqual(self.review(BASE.replace(OLD, NEW)), set())

    def test_repair_mixed_with_entry_update(self):
        base = BASE + PARENT.replace('[Parent]', '[Other]').replace('/parent)', '/other)')
        head = base.replace(OLD, NEW).replace('[Other]', '[Renamed]')
        self.assertEqual(self.review(head, base=base), set())

    def test_new_changed_moved_or_duplicated_references_rejected(self):
        cases = [
            BASE + NEW + '\n',
            BASE.replace(OLD, NEW + '\n' + NEW),
            BASE.replace(OLD, NEW.replace('Library -', 'Different -')),
            BASE.replace(OLD, NEW.replace('  -', '   -')),
            BASE.replace(OLD, NEW.lstrip()),
            BASE.replace(OLD, NEW.replace('[C++]', '[New label]')),
            BASE.replace(OLD, NEW.replace('/project/demo/', '/project/other/')),
            (BASE.replace(OLD, '') + '## Market Data & Data Sources\n'
             + PARENT.replace('[Parent]', '[Moved]') + NEW + '\n'),
            BASE.replace(OLD, '') + PARENT.replace('[Parent]', '[Other]') + NEW + '\n',
            BASE.replace(OLD + '\n', ''),
        ]
        for head in cases:
            with self.subTest(head=head):
                self.assertTrue(self.review(head))

    def test_reference_cannot_move_between_identical_parent_occurrences(self):
        base = BASE + PARENT
        head = BASE.replace(OLD + '\n', '') + PARENT + NEW + '\n'
        self.assertEqual(nested_reference_repairs(base, head), [])

    def test_reference_cannot_reorder_within_parent(self):
        other = OLD.replace('Library -', 'Other -')
        base = BASE + other + '\n'
        head = BASE.replace(OLD, other) + NEW + '\n'
        self.assertEqual(nested_reference_repairs(base, head), [])

    def test_replacement_or_unverified_repository_rejected(self):
        for identity in (456, None):
            with self.subTest(identity=identity):
                self.assertTrue(self.review(BASE.replace(OLD, NEW), identity=identity))

    def test_non_repository_destinations_rejected(self):
        for url in ('http://github.com/example/new', 'https://user@github.com/example/new',
                    'https://other.example/example/new', 'https://github.com/example/new?q=x',
                    'https://github.com/example/new#x', 'https://github.com/example/new/tree/main'):
            with self.subTest(url=url):
                self.assertTrue(self.review(BASE.replace('https://github.com/example/old', url)))

    def test_offline_validation_preserves_entry_count(self):
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / 'README.md'
            readme.write_text(BASE.replace(OLD, NEW))
            self.assertEqual(len(list(iter_readme_entries(readme))), 1)
            self.assertEqual(validate_malformed_added_lines(readme, {3}, base_readme=BASE), [])
            self.assertTrue(validate_malformed_added_lines(
                readme, {3}, base_readme=BASE.replace(OLD, '')
            ))

    def test_offline_cli_uses_merge_base_for_existing_reference(self):
        script = Path(__file__).resolve().parents[1] / 'scripts' / 'validate_readme.py'
        with tempfile.TemporaryDirectory() as directory:
            def git(*args):
                return subprocess.run(['git', *args], cwd=directory, check=True,
                                      capture_output=True, text=True).stdout.strip()
            git('init', '-q')
            git('config', 'user.email', 'test@example.com')
            git('config', 'user.name', 'Test')
            readme = Path(directory) / 'README.md'
            readme.write_text(BASE)
            git('add', 'README.md')
            git('commit', '-qm', 'Base')
            base = git('rev-parse', 'HEAD')
            readme.write_text(BASE.replace(OLD, NEW))
            git('commit', '-qam', 'Repair')
            result = subprocess.run(
                [sys.executable, str(script), '--diff-from', base], cwd=directory,
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('Validated 0 entries', result.stdout)
            readme.write_text(BASE.replace(OLD, NEW) + NEW + '\n')
            git('commit', '-qam', 'Extra reference')
            result = subprocess.run(
                [sys.executable, str(script), '--diff-from', base], cwd=directory,
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn('added README bullet does not match entry regex', result.stdout)
