import re
import unittest
from dataclasses import fields
from pathlib import Path

from scripts.review_pr import ReviewSnapshot

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

    def test_sprr_preserves_historical_exception_to_rejection(self):
        verdicts = self.sprr.split("## Verdicts", 1)[1].split("## Output Shape", 1)[0]
        self.assertIn("Historical & Archived Projects", verdicts)
        self.assertIn("CONTRIBUTING.md", verdicts)

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

    def test_review_week_allocations_fit_the_total_human_allowance(self):
        # Catch an allocation that silently spends more than the weekly allowance.
        rows = re.findall(r"^\| ([^|]+) \| (\d+) \|$", self.contributing, re.M)
        allocations = {name.strip(): int(minutes) for name, minutes in rows}
        self.assertIn("Total", allocations)
        total = allocations.pop("Total")
        self.assertEqual(total, 120)
        self.assertEqual(sum(allocations.values()), total)

    def test_reviewer_can_read_every_field_emitted_by_the_ci_snapshot(self):
        # This is the A2/A3 interface, rather than a copy of the prose around it.
        provenance = self.sprr.partition("## PR Review Provenance\n")[2].split("\n## ", 1)[0]
        documented = re.findall(r"^\| `(\w+)` \|", provenance, re.M)
        self.assertCountEqual(documented, [field.name for field in fields(ReviewSnapshot)])

    def test_decision_digest_keeps_eligibility_priority_and_readiness_separate(self):
        headers = [
            [cell.strip() for cell in line.strip("|").split("|")]
            for line in self.bprr.splitlines()
            if line.startswith("| PR |")
        ]
        self.assertEqual(len(headers), 1)
        self.assertTrue(
            {"Eligibility", "Priority", "Readiness", "Proposed action"}
            .issubset(headers[0])
        )

    def test_intake_and_skills_link_to_reachable_local_policy(self):
        paths = (
            ROOT / ".github/pull_request_template.md",
            ROOT / ".agents/skills/sprr/SKILL.md",
            ROOT / ".agents/skills/bprr/SKILL.md",
        )
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file())
                if not path.is_file():
                    continue
                prose = re.sub(r"```[\s\S]*?```|`[^`]*`", "", path.read_text())
                links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", prose)
                canonical = "https://github.com/wilsonfreitas/awesome-quant/blob/main/"
                policy_links = [link for link in links if "://" not in link or link.startswith(canonical)]
                self.assertTrue(policy_links, "Policy must be discoverable from intake/skills")
                for link in policy_links:
                    base = path.parent
                    if link.startswith(canonical):
                        base, link = ROOT, link.removeprefix(canonical)
                    filename, _, anchor = link.partition("#")
                    target = (base / filename).resolve()
                    self.assertTrue(target.is_file(), link)
                    if anchor and target.is_file():
                        headings = re.findall(r"^#+ (.+)$", target.read_text(), re.M)
                        anchors = {
                            re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
                            for heading in headings
                        }
                        self.assertIn(anchor, anchors, link)


if __name__ == "__main__":
    unittest.main()
