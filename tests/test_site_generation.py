import csv
import importlib.util
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.readme_entries import iter_readme_entries

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('site_generate', ROOT / 'site/generate.py')
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)

FIXTURE = '''## Trading & Backtesting
- [Engine](https://example.org) - `Python` `Spring Boot` - Works. [Docs](https://example.org/docs) [GitHub](https://github.com/example/engine)
## Historical & Archived Projects
- [Old](https://github.com/example/old) - `Python` `Historical` - Archived foundational engine.
## Commercial & Proprietary Services
- [Service](https://example.org/service) - Useful service.
## Related Lists
- [Lists](https://example.org/lists) - Other lists.
'''


class SiteGenerationTests(unittest.TestCase):
    def test_tags_round_trip_as_complete_strings(self):
        tags = ['Python', 'Spring Boot', 'SEC EDGAR', 'Pine Script', 'C++', 'Risk & Return', 'A "quoted" tag']
        rows, buttons = [], []

        class Collector(HTMLParser):
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == 'tr' and attrs.get('class') == 'row':
                    rows.append(attrs)
                if tag == 'button' and attrs.get('data-filter-type') == 'language':
                    buttons.append(attrs['data-filter-value'])

        rendered = site.generate_html([dict(project='Example', url='https://example.org',
            description='Example.', languages=','.join(tags))])
        Collector().feed(rendered)
        self.assertIn('data-tags', rows[0])
        self.assertEqual(json.loads(rows[0]['data-tags']), tags)
        self.assertEqual(set(buttons), set(tags))
        self.assertIn('</strong> tags</span>', rendered)

    def test_current_readme_membership_matches_shared_parser(self):
        actual = site.parse_readme(ROOT / 'README.md')
        expected = list(iter_readme_entries(ROOT / 'README.md'))
        self.assertEqual([(e['project'], e['url'], e['category']) for e in actual],
                         [(e.name, e.url, e.section) for e in expected])

    def test_readme_preserves_extra_links_tags_sections_and_source_flags(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'README.md'
            path.write_text(FIXTURE)
            entries = site.parse_readme(path)
        self.assertEqual([e['project'] for e in entries], ['Engine', 'Old', 'Service', 'Lists'])
        self.assertEqual(entries[0]['languages'], 'Python,Spring Boot')
        self.assertEqual(entries[0]['repo'], 'example/engine')
        self.assertIn('[Docs](https://example.org/docs)', entries[0]['description'])
        self.assertNotIn('[GitHub]', entries[0]['description'])
        self.assertEqual(entries[1]['category'], 'Historical & Archived Projects')
        self.assertTrue(entries[2]['commercial'])
        self.assertFalse(entries[3]['github'])

    def fixture_csv(self, path):
        with path.open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=['project', 'url', 'description', 'language',
                                   'category', 'section_slug', 'repo', 'stars', 'last_commit', 'github'])
            writer.writeheader()
            writer.writerow(dict(project='CachedOnly', url='https://github.com/example/cached',
                description='Cached project.', language='R', category='Time Series Analysis',
                section_slug='time-series-analysis', repo='example/cached', stars='1234',
                last_commit='2026-01-01', github='True'))

    def test_csv_singular_language_compatibility(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'projects.csv'
            self.fixture_csv(path)
            entry = site.load_csv(path)[0]
        self.assertEqual(entry['languages'], 'R')
        self.assertEqual(entry['stars'], 1234)
        self.assertTrue(entry['github'])

    def generate(self, directory, *args):
        readme = directory / 'README.md'
        readme.write_text(FIXTURE)
        output = directory / 'index.html'
        result = subprocess.run([sys.executable, str(ROOT / 'site/generate.py'),
            '--readme', str(readme), '--csv', str(directory / 'projects.csv'),
            '--output', str(output), *args], cwd=directory, text=True, capture_output=True)
        return result, output

    def test_default_preview_ignores_stale_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.fixture_csv(directory / 'projects.csv')
            result, output = self.generate(directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.exists(), 'CLI must honor explicit output path')
            rendered = output.read_text()
            self.assertIn('Engine', rendered)
            self.assertNotIn('CachedOnly', rendered)

    def test_explicit_csv_renders_enriched_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.fixture_csv(directory / 'projects.csv')
            result, output = self.generate(directory, '--source', 'csv')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.exists(), 'CLI must honor explicit output path')
            rendered = output.read_text()
            self.assertIn('CachedOnly', rendered)
            self.assertIn('1.2k', rendered)
            self.assertIn('2026-01-01', rendered)
            self.assertNotIn('>Engine<', rendered)

    def test_missing_explicit_csv_does_not_fall_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, output = self.generate(Path(tmp), '--source', 'csv')
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())


class MetadataDisplayTests(unittest.TestCase):
    def entry(self, **values):
        return dict(project='Engine', url='https://example.org', description='Engine.', **values)

    def text(self, rendered):
        chunks = []

        class Collector(HTMLParser):
            def handle_data(self, data):
                chunks.append(data)

        Collector().feed(rendered)
        return ' '.join(chunks)

    def test_source_labels_checks_and_stale_status_are_visible(self):
        rendered = site.generate_html([self.entry(last_commit='2026-01-01',
            last_commit_source='github_commit', last_commit_checked_at='2026-11-13T12:00:00+00:00',
            last_commit_status='stale', stars=42, stars_source='github', stars_status='stale',
            stars_checked_at='2026-11-12T12:00:00+00:00',
            pypi_upload='2026-02-03', pypi_upload_source='pypi_upload', pypi_upload_status='fresh',
            pypi_upload_checked_at='2026-11-14T12:00:00+00:00',
            cran_published='2026-03-04', cran_published_source='cran_publication',
            cran_published_status='fresh', cran_published_checked_at='2026-11-14T12:00:00+00:00')])
        text = self.text(rendered)
        for label in ('GitHub commit', 'PyPI upload', 'CRAN publication', 'Checked',
                      '2026-11-13', '2026-11-12', 'stale', 'reused'):
            self.assertIn(label, text)
        self.assertIn('data-update="2026-01-01"', rendered)

    def test_registry_fallback_is_labelled_upload_not_commit(self):
        rendered = site.generate_html([self.entry(last_commit='', pypi_upload='2026-02-03',
            pypi_upload_source='pypi_upload', pypi_upload_status='fresh',
            pypi_upload_checked_at='2026-11-14T12:00:00+00:00')])
        text = self.text(rendered)
        self.assertIn('PyPI upload', text)
        self.assertNotIn('Last commit: 2026-02-03', rendered)
        self.assertIn('data-update="2026-02-03"', rendered)

    def test_unknown_and_zero_stars_are_distinct_and_legacy_is_unattributed(self):
        rendered = site.generate_html([self.entry(stars=None, last_commit='2020-01-01')])
        text = self.text(rendered)
        self.assertIn('Unknown', text)
        self.assertIn('source unknown', text)
        self.assertNotIn('Last commit:', rendered)
        rendered = site.generate_html([self.entry(stars=0, stars_source='github',
            stars_status='fresh', stars_checked_at='2026-11-14T12:00:00+00:00')])
        self.assertIn('0 stars', rendered)

    def test_metadata_escaping(self):
        hostile = '\"><script>alert(1)</script>'
        rendered = site.generate_html([self.entry(last_commit=hostile, last_commit_source=hostile,
            last_commit_checked_at=hostile, last_commit_status=hostile,
            metadata_attempted_at=hostile, stars=1, stars_checked_at=hostile)])
        self.assertNotIn('<script>alert(1)</script>', rendered)
        self.assertNotIn('title="Last commit:', rendered)

    def test_empty_and_malformed_csv_metadata_remains_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'projects.csv'
            with path.open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=['project', 'url', 'description',
                    'stars', 'last_commit', 'last_commit_source', 'last_commit_checked_at'])
                writer.writeheader()
                for stars in ('', 'NaN', 'inf', '-2', 'bad'):
                    writer.writerow(dict(project='Engine', url='https://example.org', description='Engine.',
                        stars=stars, last_commit='2026-02-30', last_commit_source='github_commit',
                        last_commit_checked_at='bad'))
            entries = site.load_csv(path)
        for entry in entries:
            self.assertIsNone(entry['stars'])
        self.assertNotIn('2026-02-30', self.text(site.generate_html(entries)))

    def test_preview_is_token_free_and_has_no_observed_stars(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'README.md'
            path.write_text(FIXTURE)
            entries = site.parse_readme(path)
        self.assertTrue(all(e['stars'] is None for e in entries))
        self.assertIn('Unknown', self.text(site.generate_html(entries)))

    def test_guide_navigation_uses_main_branch(self):
        rendered = site.generate_html([])
        self.assertIn('href="https://github.com/wilsonfreitas/awesome-quant/blob/main/docs/choosing-backtesting.md"', rendered)
        self.assertIn('>Choosing a backtester</a>', rendered)
        self.assertIn('blob/main/CONTRIBUTING.md', rendered)
        self.assertNotIn('blob/master/CONTRIBUTING.md', rendered)

    def test_details_include_only_applicable_sources_and_actual_legacy_values(self):
        rendered = site.build_metadata_details(self.entry(github=True, stars=None, last_commit=''))
        text = self.text(rendered)
        self.assertIn('GitHub commit', text)
        self.assertIn('GitHub stars', text)
        self.assertNotIn('PyPI', text)
        self.assertNotIn('CRAN', text)
        self.assertNotIn('Date (', text)
        rendered = site.build_metadata_details(self.entry(pypi=True))
        text = self.text(rendered)
        self.assertIn('PyPI upload', text)
        self.assertNotIn('GitHub', text)
        self.assertNotIn('CRAN', text)
        self.assertEqual(site.build_metadata_details(self.entry()), '')
        text = self.text(site.build_metadata_details(self.entry(last_commit='2020-01-01', stars=42)))
        self.assertIn('Date (source unknown)', text)
        self.assertIn('2020-01-01', text)
        self.assertIn('42', text)
        self.assertNotIn('commit', text)
