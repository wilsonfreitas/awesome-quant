import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReviewDocumentationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        cls.sprr = (ROOT / ".agents/skills/sprr/SKILL.md").read_text(
            encoding="utf-8"
        )
        cls.bprr = (ROOT / ".agents/skills/bprr/SKILL.md").read_text(
            encoding="utf-8"
        )

    def test_contributing_requires_both_workflows_on_latest_revision(self):
        self.assertIn("## Required Pull Request Workflows", self.contributing)
        self.assertIn("`Validate PR`", self.contributing)
        self.assertIn("`PR Review`", self.contributing)
        self.assertIn(
            "Both workflows must pass on the latest pull request revision",
            self.contributing,
        )

    def test_sprr_treats_both_workflows_as_approval_gates(self):
        self.assertIn(
            "Both `Validate PR` and `PR Review` must pass before returning "
            "`APPROVE`",
            self.sprr,
        )

    def test_bprr_uses_sprr_as_the_canonical_per_pr_policy(self):
        self.assertIn("**REQUIRED SUB-SKILL:** Use `sprr`", self.bprr)
        self.assertIn("Apply `sprr` independently to every PR", self.bprr)
        for duplicated_section in (
            "## CI Evidence Rules",
            "## Validation Checklist",
            "## Verdicts",
        ):
            self.assertNotIn(duplicated_section, self.bprr)

    def test_bulk_summary_reports_both_required_workflows(self):
        self.assertIn("| Validate PR | PR Review |", self.bprr)


if __name__ == "__main__":
    unittest.main()
