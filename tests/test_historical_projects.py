import importlib.util
import tempfile
import unittest
from pathlib import Path

from scripts.readme_entries import HISTORICAL_SECTION, iter_readme_entries
from scripts.validate_readme import build_duplicate_indexes, validate_entry


ROOT = Path(__file__).resolve().parents[1]


class HistoricalProjectContractTests(unittest.TestCase):
    def validate_single_entry(self, line):
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            readme.write_text(
                f"## {HISTORICAL_SECTION}\n{line}\n",
                encoding="utf-8",
            )
            entry = next(iter_readme_entries(readme))
            names, urls = build_duplicate_indexes([entry])
            return validate_entry(
                entry,
                duplicate_names=names,
                duplicate_urls=urls,
                strict_duplicates=True,
                strict_urls=True,
                strict_format=True,
            )

    def test_accepts_tagged_entry(self):
        issues = self.validate_single_entry(
            "- [Example](https://github.com/example/project) - "
            "`Python` `Historical` - Archived example retained for its early design."
        )
        self.assertEqual(issues, [])

    def test_requires_historical_tag(self):
        issues = self.validate_single_entry(
            "- [Example](https://github.com/example/project) - "
            "`Python` - Archived example retained for its early design."
        )
        self.assertIn("historical-tag", {issue.code for issue in issues})

    def test_requires_non_status_tag(self):
        issues = self.validate_single_entry(
            "- [Example](https://github.com/example/project) - "
            "`Historical` - Archived example retained for its early design."
        )
        self.assertIn("language", {issue.code for issue in issues})

    def test_readme_and_site_parser_include_historical_projects(self):
        spec = importlib.util.spec_from_file_location(
            "site_generate", ROOT / "site" / "generate.py"
        )
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)

        entries = module.parse_readme(ROOT / "README.md")
        historical = [
            entry
            for entry in entries
            if entry["category"] == "Historical & Archived Projects"
        ]

        self.assertEqual(
            {entry["project"] for entry in historical},
            {"fooltrader", "pipeline-live", "pybacktest"},
        )
        self.assertTrue(all("Historical" in entry["languages"] for entry in historical))

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "- [Historical & Archived Projects](#historical-archived-projects)",
            readme,
        )
        self.assertLess(
            readme.index("## Historical & Archived Projects"),
            readme.index("## Related Lists"),
        )
        self.assertNotIn("pythalesians", readme)
