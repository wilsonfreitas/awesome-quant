"""Recency is a review lead, not an editorial verdict."""
import io
import unittest
from contextlib import redirect_stdout
from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import patch

from scripts.review_pr import Finding, main, review_pr
from tests.test_review_pr import FakeBaseRepository, FakeClient, FakePull, NOW


class MaintenanceEvidenceTests(unittest.TestCase):
    def assess(self, commit_date, *, pushed_at=NOW, archived=False, error=None):
        client = FakeClient(FakeBaseRepository(FakePull(10)))
        project = client.project_repository
        project.default_branch = "stable"
        project.pushed_at = pushed_at
        project.archived = archived
        commit = SimpleNamespace(commit=SimpleNamespace(
            committer=SimpleNamespace(date=commit_date),
            author=SimpleNamespace(date=NOW),
        ))
        with patch.object(project, "get_commit", create=True,
                          return_value=commit, side_effect=error) as lookup:
            findings, _, _ = review_pr("owner/list", 10, client, now=NOW)
        return findings, lookup

    def test_recent_push_does_not_hide_old_default_branch_commit(self):
        findings, lookup = self.assess(NOW - timedelta(days=800))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].check, "activity")
        self.assertEqual(findings[0].severity, "review")
        self.assertIn("default-branch", findings[0].detail)
        lookup.assert_called_once_with(sha="stable")

    def test_recent_default_branch_commit_is_only_a_screening_pass(self):
        findings, _ = self.assess(NOW, pushed_at=NOW - timedelta(days=800))
        self.assertEqual(findings, [])

    def test_unavailable_commit_requires_evidence_instead_of_inactivity_claim(self):
        findings, _ = self.assess(None, error=RuntimeError("unavailable"))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "review")
        self.assertIn("unverified", findings[0].detail)

    def test_invalid_commit_dates_remain_unverified(self):
        for date in (None, NOW.replace(tzinfo=None), NOW + timedelta(days=1)):
            with self.subTest(date=date):
                findings, _ = self.assess(date)
                self.assertEqual(findings[0].severity, "review")
                self.assertIn("unverified", findings[0].detail)

    def test_archived_active_entry_still_fails(self):
        findings, _ = self.assess(NOW, archived=True)
        self.assertTrue(any(f.severity == "error" and "archived" in f.detail
                            for f in findings))

    def test_educational_publication_can_use_authoritative_non_repository_source(self):
        body = "## Reproducing Works, Training & Books\n"
        line = "- [Research notes](https://example.org/notes) - Reproduce a pricing model.\n"
        pull = FakePull(10, files=[SimpleNamespace(
            filename="README.md", patch="@@ -1 +1,2 @@\n " + body + "+" + line)])
        client = FakeClient(FakeBaseRepository(pull, base_readme=body,
                                               head_readme=body + line))
        with patch("scripts.review_pr.url_reachable", return_value=True):
            findings, _, _ = review_pr("owner/list", 10, client, now=NOW)
        self.assertEqual(findings, [])

    def run_cli(self, findings):
        output = io.StringIO()
        with patch.dict("os.environ", {"GITHUB_TOKEN": "test", "PR_NUMBER": "10",
                                       "GITHUB_REPOSITORY": "owner/list"}, clear=True), \
             patch("sys.argv", ["review_pr.py"]), \
             patch("scripts.review_pr.Github"), \
             patch("scripts.review_pr.review_pr", return_value=(findings, "Example", 1)), \
             redirect_stdout(output):
            code = main()
        return code, output.getvalue()

    def test_manual_assessment_is_visible_without_automatic_rejection(self):
        code, output = self.run_cli([Finding("activity", "Needs maintenance evidence", "review")])
        self.assertEqual(code, 0)
        self.assertIn("manual review", output)
        self.assertNotIn("activity: pass", output)
        self.assertIn("not eligibility or merge approval", output)

    def test_manual_finding_cannot_mask_structural_failure(self):
        code, output = self.run_cli([Finding("activity", "Needs evidence", "review"),
                                     Finding("format", "Malformed entry")])
        self.assertEqual(code, 1)
        self.assertIn("format: fail", output)


if __name__ == "__main__":
    unittest.main()
