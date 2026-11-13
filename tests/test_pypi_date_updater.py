import contextlib
import importlib.util
import io
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

import parse

ROOT = Path(__file__).resolve().parents[1]
UPDATER = ROOT / '.agents/skills/update-pypi-dates/scripts/check_pypi_dates.py'


class PyPIDateUpdaterTests(unittest.TestCase):
    def load(self):
        spec = importlib.util.spec_from_file_location('date_updater', UPDATER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_parser_preserves_url_shapes_and_empty_fallback(self):
        with patch('scripts.pypi_metadata.get_pypi_last_updated', return_value='2026-01-01') as lookup:
            for url in ('https://pypi.org/project/example/', 'https://pypi.python.org/pypi/example'):
                self.assertEqual(parse.get_pypi_last_updated(url), '2026-01-01')
            self.assertEqual(lookup.call_count, 2)
        with patch('scripts.pypi_metadata.get_pypi_last_updated', return_value=None):
            self.assertEqual(parse.get_pypi_last_updated('https://pypi.org/project/example/'), '')
        self.assertEqual(parse.get_pypi_last_updated('https://example.org'), '')

    def test_failed_fetch_preserves_readme_and_updates_are_idempotent(self):
        module = self.load()
        original = '- [qfrm](https://pypi.org/project/qfrm/) - `Python` - Pricing (Last updated: 2020-01-01).\n'
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            target = Path(tmp) / 'README.md'
            target.write_text(original)
            module.README_PATH = target
            with patch('scripts.pypi_metadata.urlopen', side_effect=OSError('offline')):
                self.assertEqual(module.main(), 0)
            self.assertEqual(target.read_text(), original)
            with patch.object(module, 'get_pypi_last_updated', return_value='2026-01-01'):
                self.assertEqual(module.main(), 0)
                updated = target.read_text()
                self.assertIn('Last updated: 2026-01-01', updated)
                self.assertEqual(module.main(), 0)
                self.assertEqual(target.read_text(), updated)

    def test_script_import_from_arbitrary_cwd_resolves_repo(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.chdir(tmp), patch('sys.path', []):
            module = runpy.run_path(str(UPDATER))
            self.assertEqual(module['README_PATH'], ROOT / 'README.md')
            self.assertEqual(module['get_pypi_last_updated'].__module__, 'scripts.pypi_metadata')
