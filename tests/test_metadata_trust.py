"""Offline contracts for successful observations, identity, and CI persistence."""
import contextlib
import csv
from datetime import datetime, timezone
import io
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import Mock, patch

import parse

NOW = '2026-11-14T12:00:00+00:00'
LATER = '2026-11-15T12:00:00+00:00'


def project(url='https://pypi.org/project/engine/', suffix=' [GitHub](https://github.com/example/engine)',
            prior=None, checked_at=NOW, name='Engine'):
    match = parse.ENTRY_RE.match(f'- [{name}]({url}) - `Python` - Engine.{suffix}')
    entry = parse.Project(match, 'Python', 'Trading & Backtesting', 'Trading & Backtesting',
                          prior=prior, checked_at=checked_at)
    entry.run()
    return entry.regs


class MetadataTrustTests(unittest.TestCase):
    def observe(self, github=('2026-01-02', 42), pypi='2026-02-03', **kwargs):
        with patch.object(parse, 'get_repo_info', return_value=github), \
             patch.object(parse, 'get_pypi_last_updated', return_value=pypi), \
             contextlib.redirect_stdout(io.StringIO()):
            return project(**kwargs)

    def test_success_keeps_repository_and_upload_dates_separate(self):
        row = self.observe()
        self.assertEqual(row['last_commit'], '2026-01-02')
        self.assertEqual(row['pypi_upload'], '2026-02-03')
        for field, source in [('last_commit', 'github_commit'), ('stars', 'github'),
                              ('pypi_upload', 'pypi_upload')]:
            self.assertEqual(row[field + '_source'], source)
            self.assertEqual(row[field + '_checked_at'], NOW)
            self.assertEqual(row[field + '_status'], 'fresh')

    def test_partial_success_never_refreshes_failed_fields(self):
        old = self.observe()
        row = self.observe(github=('', None), pypi='2026-11-01', prior=old, checked_at=LATER)
        self.assertEqual(row['pypi_upload_checked_at'], LATER)
        self.assertEqual(row['pypi_upload_status'], 'fresh')
        self.assertEqual(row['last_commit'], '2026-01-02')
        self.assertEqual(row['stars'], 42)
        for field in ('last_commit', 'stars'):
            self.assertEqual(row[field + '_checked_at'], NOW)
            self.assertEqual(row[field + '_status'], 'stale')
        row = self.observe(github=('', 84), prior=old, checked_at=LATER)
        self.assertEqual(row['stars_checked_at'], LATER)
        self.assertEqual(row['last_commit_checked_at'], NOW)
        row = self.observe(github=('2026-11-01', None), prior=old, checked_at=LATER)
        self.assertEqual(row['last_commit_checked_at'], LATER)
        self.assertEqual(row['stars_checked_at'], NOW)

    def test_total_failure_retains_last_success_through_csv_in_clean_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            first, clean = Path(tmp) / 'first', Path(tmp) / 'clean'
            for directory in (first, clean):
                (directory / 'site').mkdir(parents=True)
                (directory / 'README.md').write_text('## Trading & Backtesting\n'
                    '- [Engine](https://pypi.org/project/engine/) - `Python` - Engine. '
                    '[GitHub](https://github.com/example/engine)\n')
            with patch.object(parse, 'get_repo_info', return_value=('2026-01-02', 42)), \
                 patch.object(parse, 'get_pypi_last_updated', return_value='2026-02-03'), \
                 contextlib.redirect_stdout(io.StringIO()):
                parse.main(first / 'README.md', first / 'site/projects.csv')
            with (first / 'site/projects.csv').open() as handle:
                successful = next(csv.DictReader(handle))
            # CI restores only the previously published CSV, into a clean checkout.
            (clean / 'site/projects.csv').write_bytes((first / 'site/projects.csv').read_bytes())
            with patch.object(parse, 'get_repo_info', return_value=('', None)), \
                 patch.object(parse, 'get_pypi_last_updated', return_value=''), \
                 contextlib.redirect_stdout(io.StringIO()):
                parse.main(clean / 'README.md', clean / 'site/projects.csv')
                parse.main(clean / 'README.md', clean / 'site/projects.csv')
            with (clean / 'site/projects.csv').open() as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row['stars'], '42')
            self.assertEqual(row['last_commit'], '2026-01-02')
            self.assertEqual(row['pypi_upload'], '2026-02-03')
            self.assertEqual(row['last_commit_status'], 'stale')
            self.assertEqual(row['pypi_upload_status'], 'stale')
            for field in ('last_commit', 'stars', 'pypi_upload'):
                self.assertEqual(row[field + '_checked_at'], successful[field + '_checked_at'])

    def test_first_failure_is_unknown_and_upload_is_never_a_commit(self):
        row = self.observe(github=('', None))
        self.assertEqual(row['last_commit'], '')
        self.assertIsNone(row['stars'])
        self.assertEqual(row['last_commit_status'], 'unknown')
        self.assertEqual(row['last_commit_checked_at'], '')
        self.assertEqual(row['pypi_upload'], '2026-02-03')
        row = self.observe(github=('', None), pypi='')
        self.assertEqual(row['pypi_upload_status'], 'unknown')
        self.assertEqual(row['pypi_upload_checked_at'], '')

    def test_changed_project_url_or_repository_invalidates_prior(self):
        old = self.observe()
        for change in ({'name': 'Replacement'}, {'url': 'https://pypi.org/project/replacement/'},
                       {'suffix': ' [GitHub](https://github.com/example/replacement)'}, {'suffix': ''}):
            with self.subTest(change=change):
                row = self.observe(github=('', None), pypi='', prior=old, **change)
                self.assertEqual(row['last_commit'], '')
                self.assertIsNone(row['stars'])
                self.assertEqual(row['pypi_upload'], '')

    def test_trailing_slash_repository_is_enriched_without_inheriting_another_repository(self):
        old = self.observe(url='https://github.com/example/engine/', suffix='')
        self.assertEqual(old['repo'], 'example/engine')
        self.assertTrue(old['github'])
        row = self.observe(url='https://github.com/example/replacement/', suffix='',
                           github=('', None), prior=old, checked_at=LATER)
        self.assertEqual(row['repo'], 'example/replacement')
        self.assertTrue(row['github'])
        self.assertEqual(row['last_commit'], '')
        self.assertIsNone(row['stars'])
        self.assertEqual(row['last_commit_status'], 'unknown')
        self.assertNotEqual(row['metadata_identity'], old['metadata_identity'])

    def test_repository_normalization_does_not_accept_other_hosts_or_subpaths(self):
        for url in ('https://githubXcom/example/engine/',
                    'https://github.com/example/engine/issues/',
                    'https://github.com/example/engine/?next=other',
                    'https://github.com/example/engine/#other'):
            with self.subTest(url=url):
                self.assertEqual(parse.extract_repo(url), '')

    def test_legacy_cache_and_malformed_observations_are_not_trusted(self):
        legacy = dict(project='Engine', url='https://pypi.org/project/engine/',
                      repo='example/engine', last_commit='2020-01-01', stars=0)
        row = self.observe(github=('2026-02-30', -1), pypi='not-a-date', prior=legacy)
        self.assertEqual(row['last_commit_status'], 'unknown')
        self.assertEqual(row['pypi_upload_status'], 'unknown')
        self.assertIsNone(row['stars'])
        old = self.observe()
        old['last_commit_checked_at'] = 'not-a-timestamp'
        old['stars'] = 'NaN'
        row = self.observe(github=('', None), pypi='', prior=old)
        self.assertEqual(row['last_commit'], '')
        self.assertIsNone(row['stars'])

    def test_zero_stars_is_a_successful_observation(self):
        row = self.observe(github=('2026-01-02', 0))
        self.assertEqual(row['stars'], 0)
        self.assertEqual(row['stars_status'], 'fresh')

    def test_cran_publication_and_discovered_repository_survive_scrape_failure(self):
        with patch.object(parse, 'get_cran_info', return_value=('2026-03-04', 'https://github.com/example/r')), \
             patch.object(parse, 'get_repo_info', return_value=('2026-01-02', 3)), \
             contextlib.redirect_stdout(io.StringIO()):
            old = project(url='https://cran.r-project.org/package=engine', suffix='')
        self.assertEqual(old['cran_published'], '2026-03-04')
        self.assertEqual(old['cran_published_source'], 'cran_publication')
        with patch.object(parse, 'get_cran_info', return_value=None), \
             patch.object(parse, 'get_repo_info', return_value=('', None)), \
             contextlib.redirect_stdout(io.StringIO()):
            row = project(url='https://cran.r-project.org/package=engine', suffix='', prior=old, checked_at=LATER)
        self.assertEqual(row['repo'], 'example/r')
        self.assertEqual(row['cran_published_checked_at'], NOW)
        self.assertEqual(row['cran_published_status'], 'stale')
        with patch.object(parse, 'get_cran_info', return_value=('2026-11-01', 'https://github.com/example/new')), \
             patch.object(parse, 'get_repo_info', return_value=('', None)), \
             contextlib.redirect_stdout(io.StringIO()):
            row = project(url='https://cran.r-project.org/package=engine', suffix='', prior=old)
        self.assertIsNone(row['stars'])
        self.assertEqual(row['last_commit'], '')

    def repository(self, commit_date):
        repo = Mock(stargazers_count=42, default_branch='trunk')
        commit = SimpleNamespace(commit=SimpleNamespace(
            author=SimpleNamespace(date=datetime(1999, 1, 1, tzinfo=timezone.utc)),
            committer=SimpleNamespace(date=commit_date)))
        repo.get_commits.return_value = [commit]
        return repo

    def test_github_uses_default_branch_committer_time_in_utc(self):
        repo = self.repository(datetime.fromisoformat('2026-01-03T00:30:00+02:00'))
        with patch.object(parse, 'get_github_client') as client:
            client.return_value.get_repo.return_value = repo
            date, stars = parse.get_repo_info('example/engine')
        self.assertEqual(date, '2026-01-02')
        self.assertEqual(stars, 42)
        repo.get_commits.assert_called_once_with(sha='trunk')

    def test_github_commit_timeout_keeps_successful_stars(self):
        repo = self.repository(None)
        repo.get_commits.side_effect = TimeoutError('offline')
        with patch.object(parse, 'get_github_client') as client, contextlib.redirect_stdout(io.StringIO()):
            client.return_value.get_repo.return_value = repo
            self.assertEqual(parse.get_repo_info('example/engine'), ('', 42))
            client.return_value.get_repo.side_effect = TimeoutError('offline')
            self.assertEqual(parse.get_repo_info('example/engine'), ('', None))

    def test_github_malformed_committer_date_keeps_successful_stars(self):
        with patch.object(parse, 'get_github_client') as client, contextlib.redirect_stdout(io.StringIO()):
            client.return_value.get_repo.return_value = self.repository('not-a-date')
            self.assertEqual(parse.get_repo_info('example/engine'), ('', 42))

    def test_github_client_has_bounded_timeout(self):
        with patch.object(parse, '_github_client', None), patch.dict('os.environ', {'GITHUB_ACCESS_TOKEN': 'fixture'}), \
             patch.object(parse, 'Github') as client:
            parse.get_github_client()
        self.assertEqual(client.call_args.kwargs['timeout'], 10)

    def test_registry_timeout_degrades_without_losing_prior(self):
        old = self.observe()
        with patch.object(parse.pypi_metadata, 'get_pypi_last_updated', side_effect=TimeoutError('offline')), \
             patch.object(parse, 'get_repo_info', return_value=('', None)), \
             contextlib.redirect_stdout(io.StringIO()):
            row = project(prior=old)
        self.assertEqual(row['pypi_upload'], '2026-02-03')
        self.assertEqual(row['pypi_upload_status'], 'stale')
        with patch.object(parse, 'urlopen', side_effect=TimeoutError('offline')), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(parse.get_cran_info('https://cran.r-project.org/package=engine'))

    def test_successful_cran_page_removing_repository_invalidates_history(self):
        with patch.object(parse, 'get_cran_info', return_value=('2026-03-04', 'https://github.com/example/r')), \
             patch.object(parse, 'get_repo_info', return_value=('2026-01-02', 3)), \
             contextlib.redirect_stdout(io.StringIO()):
            old = project(url='https://cran.r-project.org/package=engine', suffix='')
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.read.return_value = b'<html><body><table><tr><td>Published:</td><td>2026-11-01</td></tr></table></body></html>'
        with patch.object(parse, 'urlopen', return_value=response), \
             patch.object(parse, 'get_github_client', side_effect=TimeoutError('offline')), \
             contextlib.redirect_stdout(io.StringIO()):
            row = project(url='https://cran.r-project.org/package=engine', suffix='', prior=old, checked_at=LATER)
        self.assertEqual(row['repo'], '')
        self.assertEqual(row['last_commit'], '')
        self.assertIsNone(row['stars'])
        self.assertEqual(row['cran_published'], '2026-11-01')
        self.assertEqual(row['cran_published_status'], 'fresh')

    def test_non_utf8_cache_degrades_to_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            readme, output = directory / 'README.md', directory / 'projects.csv'
            readme.write_text('## Trading & Backtesting\n'
                '- [Engine](https://github.com/example/engine) - `Python` - Engine.\n')
            output.write_bytes(b'project,stars\nEngine,\xff\n')
            with patch.object(parse, 'get_repo_info', return_value=('', None)), \
                 contextlib.redirect_stdout(io.StringIO()):
                parse.main(readme, output)
            with output.open() as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row['stars'], '')
            self.assertEqual(row['last_commit_status'], 'unknown')

    def test_incomplete_or_invalid_cran_publication_preserves_cached_observations(self):
        with patch.object(parse, 'get_cran_info', return_value=('2026-03-04', 'https://github.com/example/r')), \
             patch.object(parse, 'get_repo_info', return_value=('2026-01-02', 3)), \
             contextlib.redirect_stdout(io.StringIO()):
            old = project(url='https://cran.r-project.org/package=engine', suffix='')
        for page in (b'<td>Published:</td>',
                     b'<td>Published:</td><td></td>',
                     b'<td>Published:</td><td>2026-02-30</td>',
                     b'<td>Published:</td><td>2026-11-01',
                     b'<td>Published:</td><td>unknown</td><td>2026-11-01</td>'):
            with self.subTest(page=page):
                response = Mock()
                response.__enter__ = Mock(return_value=response)
                response.__exit__ = Mock(return_value=False)
                response.read.return_value = b'<html><body>' + page + b'</body></html>'
                with patch.object(parse, 'urlopen', return_value=response), \
                     patch.object(parse, 'get_repo_info', return_value=('', None)), \
                     contextlib.redirect_stdout(io.StringIO()):
                    row = project(url='https://cran.r-project.org/package=engine', suffix='',
                                  prior=old, checked_at=LATER)
                self.assertEqual(row['repo'], 'example/r')
                for field, value in (('last_commit', '2026-01-02'), ('stars', 3), ('cran_published', '2026-03-04')):
                    self.assertEqual(row[field], value)
                    self.assertEqual(row[field + '_checked_at'], NOW)
                    self.assertEqual(row[field + '_status'], 'stale')

    def test_cran_truncated_after_closed_publication_cell_preserves_all_observations(self):
        url = 'https://cran.r-project.org/package=quantmod'
        github = 'https://github.com/joshuaulrich/quantmod'
        with patch.object(parse, 'get_cran_info', return_value=('2026-03-04', github)), \
             patch.object(parse, 'get_repo_info', return_value=('2026-01-02', 3)), \
             contextlib.redirect_stdout(io.StringIO()):
            old = project(url=url, suffix='')
        prefix = b'<html><body><table><tr><td>Published:</td><td>2026-11-01</td>'
        full_page = prefix + (f'</tr><tr><td>URL:</td><td><a href="{github}">Source</a>'
                              '</td></tr></table></body></html>').encode()
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        with patch.object(parse, 'urlopen', return_value=response), \
             patch.object(parse, 'get_repo_info', return_value=('', None)), \
             contextlib.redirect_stdout(io.StringIO()):
            response.read.return_value = full_page
            self.assertEqual(parse.get_cran_info(url), ('2026-11-01', github))
            for ending in (b'', b'</body>', b'</html>', b'<!-- </body></html> -->', b'</html></body>'):
                with self.subTest(ending=ending):
                    response.read.return_value = prefix + ending
                    self.assertIsNone(parse.get_cran_info(url))
                    row = project(url=url, suffix='', prior=old, checked_at=LATER)
                    self.assertEqual(row['repo'], 'joshuaulrich/quantmod')
                    for field in ('last_commit', 'stars', 'cran_published'):
                        self.assertEqual(row[field], old[field])
                        self.assertEqual(row[field + '_source'], old[field + '_source'])
                        self.assertEqual(row[field + '_checked_at'], NOW)
                        self.assertEqual(row[field + '_status'], 'stale')
