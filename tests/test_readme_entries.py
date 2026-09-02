import tempfile
import unittest
from pathlib import Path

from scripts.readme_entries import iter_readme_entries


class ReadmeEntryUrlTests(unittest.TestCase):
    def test_external_urls_extracts_all_urls_in_source_order_without_duplicates(self):
        readme = (
            "## Trading & Backtesting\n\n"
            "- [Primary](https://example.com/primary) - `Python` - "
            "Suffix [Docs](https://example.com/suffix) and "
            "<https://example.com/autolink> repeated "
            "[Again](https://example.com/suffix).\n"
        )

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text(readme, encoding="utf-8")

            entry = next(iter_readme_entries(path))

        self.assertEqual(
            entry.external_urls,
            [
                "https://example.com/primary",
                "https://example.com/suffix",
                "https://example.com/autolink",
            ],
        )

    def test_external_urls_includes_legacy_http_urls(self):
        readme = (
            "## Trading & Backtesting\n\n"
            "- [Legacy](http://example.com/primary) - `Python` - "
            "<http://example.com/autolink> entry.\n"
        )

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text(readme, encoding="utf-8")

            entry = next(iter_readme_entries(path))

        self.assertEqual(
            entry.external_urls,
            ["http://example.com/primary", "http://example.com/autolink"],
        )
