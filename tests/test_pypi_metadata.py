import contextlib
import importlib
import io
import json
from http.client import IncompleteRead
import unittest
from unittest.mock import Mock, patch


class PyPIMetadataTests(unittest.TestCase):
    def helper(self):
        try:
            return importlib.import_module('scripts.pypi_metadata')
        except ModuleNotFoundError:
            self.fail('shared PyPI metadata helper is missing')

    def test_latest_upload_uses_all_files_not_version_order(self):
        payload = {'releases': {
            '1.9': [{'upload_time_iso_8601': '2020-01-01T00:00:00Z'}],
            '1.10': [{'upload_time_iso_8601': '2021-01-01T00:00:00Z'},
                     {'upload_time_iso_8601': '2026-01-01T00:00:00Z'}],
        }}
        self.assertEqual(self.helper().latest_upload_date(payload), '2026-01-01')
        payload['releases'] = dict(reversed(list(payload['releases'].items())))
        self.assertEqual(self.helper().latest_upload_date(payload), '2026-01-01')

    def test_offsets_prereleases_and_yanked_files_use_upload_time(self):
        payload = {'releases': {
            '2.0rc1': [{'upload_time_iso_8601': '2026-01-02T00:30:00+02:00', 'yanked': True}],
            '1.0': [{'upload_time_iso_8601': '2026-01-01T23:30:00-02:00'}],
        }}
        self.assertEqual(self.helper().latest_upload_date(payload), '2026-01-02')

    def test_empty_malformed_and_missing_dates_are_ignored(self):
        for payload in ({}, {'releases': {}}, {'releases': None},
                        {'releases': {'1': [], '2': [None, {}, {'upload_time_iso_8601': 'bad'}]}},
                        {'releases': {'1': 'not a file list'}}):
            with self.subTest(payload=payload):
                self.assertIsNone(self.helper().latest_upload_date(payload))

    def test_fetch_uses_timeout_and_returns_selected_date(self):
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.read.return_value = json.dumps({'releases': {'1': [
            {'upload_time_iso_8601': '2026-02-03T00:00:00Z'}]}}).encode()
        helper = self.helper()
        with patch.object(helper, 'urlopen', return_value=response) as fetch:
            self.assertEqual(helper.get_pypi_last_updated('example'), '2026-02-03')
        fetch.assert_called_once_with('https://pypi.org/pypi/example/json', timeout=10)

    def test_fetch_failure_returns_none(self):
        helper = self.helper()
        with patch.object(helper, 'urlopen', side_effect=OSError('offline')), contextlib.redirect_stderr(io.StringIO()):
            self.assertIsNone(helper.get_pypi_last_updated('example'))

    def test_truncated_response_returns_none(self):
        helper = self.helper()
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.read.side_effect = IncompleteRead(b'{"releases":', 100)
        with patch.object(helper, 'urlopen', return_value=response), contextlib.redirect_stderr(io.StringIO()):
            self.assertIsNone(helper.get_pypi_last_updated('example'))
