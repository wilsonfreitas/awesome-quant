import csv
import importlib.util
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
