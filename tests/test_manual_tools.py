import contextlib
import io
import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]


class ManualToolTests(unittest.TestCase):
    def load(self, name):
        return runpy.run_path(str(ROOT / name))

    def test_imports_have_no_network_credentials_or_output_side_effects(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.chdir(tmp):
            with patch.dict(os.environ, {}, clear=True), \
                 patch('requests.get', side_effect=AssertionError('network')), \
                 patch('github.Github', side_effect=AssertionError('GitHub')):
                for name in ('cranscrape.py', 'topic.py'):
                    with self.subTest(name=name):
                        try:
                            module = self.load(name)
                        except Exception as exc:
                            self.fail(f'import must have no side effects: {exc}')
                        self.assertTrue(callable(module['main']))
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_cran_main_writes_csv_only_on_success(self):
        module = self.load('cranscrape.py')
        response = Mock(text='<a href="https://github.com/owner/repo">source</a>')
        with tempfile.TemporaryDirectory() as tmp, contextlib.chdir(tmp):
            with patch('requests.get', return_value=response) as request:
                self.assertEqual(module['main'](), 0)
            self.assertIn('https://github.com/owner/repo', Path('cran.csv').read_text())
            self.assertTrue(all(call.kwargs['timeout'] == 10 for call in request.call_args_list))
            response.raise_for_status.assert_called()

    def test_cran_http_failure_preserves_existing_output(self):
        module = self.load('cranscrape.py')
        import requests
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError('unavailable')
        with tempfile.TemporaryDirectory() as tmp, contextlib.chdir(tmp):
            Path('cran.csv').write_text('previous output')
            with patch('requests.get', return_value=response), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(module['main'](), 1)
            self.assertEqual(Path('cran.csv').read_text(), 'previous output')

    def test_topic_missing_token_returns_failure(self):
        module = self.load('topic.py')
        with patch.dict(os.environ, {}, clear=True), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(module['main'](), 1)
