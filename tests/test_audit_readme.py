import tempfile
import threading
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from github import GithubException

from scripts.audit_readme import (
    AuditTarget,
    Candidate,
    Finding,
    FindingKind,
    TRACKING_MARKER,
    TRACKING_TITLE,
    audit_readme,
    collect_targets,
    render_report,
    sync_tracking_issue,
)
from scripts.readme_entries import ReadmeEntry
from scripts.url_probe import Outcome, UrlObservation


def entry(line_number, section, name, url, *, raw_line=None):
    return ReadmeEntry(
        line_number=line_number,
        raw_line=raw_line or f"- [{name}]({url}) - `Python` - Entry.",
        section=section,
        name=name,
        url=url,
        tail="`Python` - Entry.",
        languages=["Python"],
        description="Entry.",
    )


def observation(url, outcome=Outcome.OK, *, status=200, attempts=1, final_url=None, error=""):
    return UrlObservation(
        requested_url=url,
        final_url=final_url or url,
        status=status,
        outcome=outcome,
        attempts=attempts,
        error=error,
    )


class FakeRepository:
    def __init__(
        self,
        full_name,
        *,
        name=None,
        stars=0,
        archived=False,
        disabled=False,
        fork=False,
        parent=None,
    ):
        self.full_name = full_name
        self.name = name or full_name.rsplit("/", 1)[-1]
        self.html_url = f"https://github.com/{full_name}"
        self.stargazers_count = stars
        self.archived = archived
        self.disabled = disabled
        self.fork = fork
        self.parent = parent


class FakeGithubClient:
    def __init__(self, repos=None, searches=None):
        self.repos = repos or {}
        self.searches = searches or {}
        self.repo_calls = []
        self.search_calls = []

    def get_repo(self, full_name):
        self.repo_calls.append(full_name)
        result = self.repos[full_name]
        if isinstance(result, BaseException):
            raise result
        return result

    def search_repositories(self, **kwargs):
        self.search_calls.append(kwargs)
        return iter(self.searches.get(kwargs["query"], ()))


class FakeIssue:
    def __init__(self, title, body, state):
        self.title = title
        self.body = body
        self.state = state
        self.edits = []

    def edit(self, **kwargs):
        self.edits.append(kwargs)
        if "body" in kwargs:
            self.body = kwargs["body"]
        if "state" in kwargs:
            self.state = kwargs["state"]


class FakeTrackingRepository:
    def __init__(self, issues=()):
        self.issues = list(issues)
        self.get_issues_calls = []
        self.create_issue_calls = []

    def get_issues(self, **kwargs):
        self.get_issues_calls.append(kwargs)
        return iter(self.issues)

    def create_issue(self, **kwargs):
        self.create_issue_calls.append(kwargs)
        issue = FakeIssue(kwargs["title"], kwargs["body"], "open")
        self.issues.append(issue)
        return issue


class AuditReadmeTests(unittest.TestCase):
    def test_render_report_is_a_complete_deterministic_markdown_document(self):
        findings = [
            Finding(
                FindingKind.CANDIDATES,
                "Zeta [Section]",
                "Replacement *Tool*",
                80,
                "https://dead.example/tool",
                "The original primary URL returned confirmed HTTP 404.",
                "Manual verification of these candidate repositories is required.",
                (
                    Candidate("zeta/tool", "https://github.com/zeta/tool", 2),
                    Candidate("beta/tool", "https://github.com/beta/tool", 9),
                    Candidate("alpha/tool", "https://github.com/alpha/tool", 9),
                ),
            ),
            Finding(
                FindingKind.PERMANENT_REDIRECT,
                "Redirects",
                "Moved",
                50,
                "https://old.example/path",
                "The link permanently redirects to https://new.example/path.",
                "Update the link to https://new.example/path.",
            ),
            Finding(
                FindingKind.HTTP_ERROR,
                "HTTP",
                "Broken",
                40,
                "https://error.example",
                "HTTP probe failed; last error unsafe URL.",
                "Perform manual diagnosis before changing the link.",
            ),
            Finding(
                FindingKind.DEAD,
                "Alpha & Beta",
                "A_B [tool]",
                10,
                "https://dead.example/a",
                "Confirmed HTTP 404 response.",
                "Manually verify, then remove or replace this link.",
            ),
            Finding(
                FindingKind.GITHUB_ARCHIVED,
                "Repositories",
                "Archive",
                60,
                "https://github.com/owner/archive",
                "GitHub marks the repository as archived.",
                "Manually verify whether to replace it or move it to the historical section.",
            ),
            Finding(
                FindingKind.RESTRICTED,
                "Access",
                "Restricted",
                30,
                "https://restricted.example",
                "Automated access was restricted by HTTP 403.",
                "Perform manual browser verification before changing the link.",
            ),
            Finding(
                FindingKind.TRANSIENT,
                "Transient",
                "Retry",
                20,
                "https://retry.example",
                "Transient failure after 3 attempts; last status 503.",
                "Retry this link on the next audit run.",
            ),
            Finding(
                FindingKind.DEAD,
                "Alpha & Beta",
                "Zed",
                11,
                "https://dead.example/z",
                "Confirmed HTTP 410 response.",
                "Manually verify, then remove or replace this link.",
            ),
        ]
        checked_at = datetime(
            2026, 9, 2, 9, 45, tzinfo=timezone(timedelta(hours=-3))
        )
        expected = r"""<!-- awesome-quant-readme-audit -->
# Weekly README audit report

Checked: 2026-09-02 12:45 UTC
Entries are reported for manual review; this automation did not modify README.md.

## Confirmed dead links

- **Entry:** A\_B \[tool\]; **README line:** 10; **Section:** Alpha & Beta; **Checked URL:** <https://dead.example/a>; **Evidence:** Confirmed HTTP 404 response.; **Manual suggestion:** Manually verify, then remove or replace this link.
- **Entry:** Zed; **README line:** 11; **Section:** Alpha & Beta; **Checked URL:** <https://dead.example/z>; **Evidence:** Confirmed HTTP 410 response.; **Manual suggestion:** Manually verify, then remove or replace this link.

## Repeated transient failures

- **Entry:** Retry; **README line:** 20; **Section:** Transient; **Checked URL:** <https://retry.example>; **Evidence:** Transient failure after 3 attempts; last status 503.; **Manual suggestion:** Retry this link on the next audit run.

## Access-restricted links

- **Entry:** Restricted; **README line:** 30; **Section:** Access; **Checked URL:** <https://restricted.example>; **Evidence:** Automated access was restricted by HTTP 403.; **Manual suggestion:** Perform manual browser verification before changing the link.

## Other HTTP failures

- **Entry:** Broken; **README line:** 40; **Section:** HTTP; **Checked URL:** <https://error.example>; **Evidence:** HTTP probe failed; last error unsafe URL.; **Manual suggestion:** Perform manual diagnosis before changing the link.

## Permanent redirects

- **Entry:** Moved; **README line:** 50; **Section:** Redirects; **Checked URL:** <https://old.example/path>; **Evidence:** The link permanently redirects to <https://new.example/path>.; **Manual suggestion:** Update the link to <https://new.example/path>.

## GitHub repository findings

- **Entry:** Archive; **README line:** 60; **Section:** Repositories; **Checked URL:** <https://github.com/owner/archive>; **Evidence:** GitHub marks the repository as archived.; **Manual suggestion:** Manually verify whether to replace it or move it to the historical section.

## Candidate replacements

- **Entry:** Replacement \*Tool\*; **README line:** 80; **Section:** Zeta \[Section\]; **Checked URL:** <https://dead.example/tool>; **Evidence:** The original primary URL returned confirmed HTTP 404.; **Manual suggestion:** Manual verification of these candidate repositories is required.
  - **Candidate 1:** alpha/tool — <https://github.com/alpha/tool> — 9 stars
  - **Candidate 2:** beta/tool — <https://github.com/beta/tool> — 9 stars
  - **Candidate 3:** zeta/tool — <https://github.com/zeta/tool> — 2 stars
"""

        self.assertEqual(render_report(findings, checked_at=checked_at), expected)
        self.assertEqual(
            render_report(reversed(findings), checked_at=checked_at),
            expected,
        )

    def test_render_report_clean_body_has_no_finding_headings(self):
        report = render_report(
            [],
            checked_at=datetime(2026, 9, 2, 12, 45, tzinfo=timezone.utc),
        )

        self.assertEqual(
            report,
            """<!-- awesome-quant-readme-audit -->
# Weekly README audit report

Checked: 2026-09-02 12:45 UTC
Entries are reported for manual review; this automation did not modify README.md.

No findings.
""",
        )

    def test_sync_tracking_issue_follows_the_full_lifecycle_matrix(self):
        findings = [SimpleNamespace()]
        new_body = f"{TRACKING_MARKER}\nnew report"
        old_body = f"{TRACKING_MARKER}\nold report"
        cases = (
            ("none with findings", (), findings, "created", None),
            (
                "open with findings",
                (FakeIssue(TRACKING_TITLE, old_body, "open"),),
                findings,
                "updated",
                {"body": new_body},
            ),
            (
                "closed with findings",
                (FakeIssue(TRACKING_TITLE, old_body, "closed"),),
                findings,
                "reopened",
                {"body": new_body, "state": "open"},
            ),
            (
                "open clean",
                (FakeIssue(TRACKING_TITLE, old_body, "open"),),
                [],
                "closed",
                {"body": new_body, "state": "closed"},
            ),
            (
                "closed clean",
                (FakeIssue(TRACKING_TITLE, old_body, "closed"),),
                [],
                "updated",
                {"body": new_body},
            ),
            ("none clean", (), [], "clean", None),
        )

        for name, issues, case_findings, expected, edit in cases:
            with self.subTest(name=name):
                repository = FakeTrackingRepository(issues)

                result = sync_tracking_issue(repository, case_findings, new_body)

                self.assertEqual(result, expected)
                self.assertEqual(repository.get_issues_calls, [{"state": "all"}])
                if issues:
                    self.assertEqual(issues[0].edits, [edit] if edit else [])
                    self.assertEqual(repository.create_issue_calls, [])
                elif case_findings:
                    self.assertEqual(
                        repository.create_issue_calls,
                        [{"title": TRACKING_TITLE, "body": new_body}],
                    )
                else:
                    self.assertEqual(repository.create_issue_calls, [])

    def test_sync_tracking_issue_does_nothing_when_body_and_state_are_current(self):
        body = f"{TRACKING_MARKER}\ncurrent report"
        for findings, state in (([SimpleNamespace()], "open"), ([], "closed")):
            with self.subTest(state=state):
                issue = FakeIssue(TRACKING_TITLE, body, state)
                repository = FakeTrackingRepository((issue,))

                result = sync_tracking_issue(repository, findings, body)

                self.assertEqual(result, "unchanged")
                self.assertEqual(issue.edits, [])
                self.assertEqual(repository.create_issue_calls, [])

    def test_sync_tracking_issue_ignores_unmarked_issues_and_rejects_duplicates(self):
        body = f"{TRACKING_MARKER}\nreport"
        unmarked = FakeIssue(TRACKING_TITLE, "human issue", "open")
        wrong_title = FakeIssue("Another report", body, "open")
        repository = FakeTrackingRepository((unmarked, wrong_title))

        self.assertEqual(
            sync_tracking_issue(repository, [SimpleNamespace()], body),
            "created",
        )

        duplicate_repository = FakeTrackingRepository(
            (
                FakeIssue(TRACKING_TITLE, body, "open"),
                FakeIssue(TRACKING_TITLE, f"prefix\n{body}", "closed"),
            )
        )
        with self.assertRaisesRegex(RuntimeError, "multiple tracking issues"):
            sync_tracking_issue(duplicate_repository, [], body)

    def test_collect_targets_uses_one_parser_pass_and_preserves_entry_and_url_order(self):
        first = entry(
            3,
            "Trading & Backtesting",
            "First",
            "https://first.example",
            raw_line=(
                "- [First](https://first.example) - `Python` - "
                "[Docs](https://docs.example)."
            ),
        )
        second = entry(4, "Trading & Backtesting", "Second", "http://second.example")

        with patch(
            "scripts.audit_readme.iter_readme_entries",
            return_value=iter((first, second)),
        ) as parser:
            targets = collect_targets("README.fixture.md")

        parser.assert_called_once_with("README.fixture.md")
        self.assertEqual(
            targets,
            [
                AuditTarget(first, "https://first.example", True),
                AuditTarget(first, "https://docs.example", False),
                AuditTarget(second, "http://second.example", True),
            ],
        )

    def test_historical_entries_keep_link_and_move_findings_but_suppress_status_and_parent(self):
        url = "https://github.com/old/project.git"
        parent = FakeRepository("upstream/project")
        repository = FakeRepository(
            "new/project",
            archived=True,
            disabled=True,
            fork=True,
            parent=parent,
        )
        client = FakeGithubClient({"old/project": repository})

        findings = self.audit(
            f"## Historical & Archived Projects\n- [Project]({url}) - `Historical` - Entry.\n",
            client,
            {url: observation(url, Outcome.DEAD, status=404)},
        )

        self.assertEqual(
            [finding.kind for finding in findings],
            [FindingKind.DEAD, FindingKind.GITHUB_MOVED],
        )
        self.assertIn("https://github.com/new/project", findings[1].suggestion)
        self.assertEqual(client.repo_calls, ["old/project"])

    def test_moved_repository_is_reported_for_each_reference_but_looked_up_once(self):
        first_url = "http://github.com/Owner/Old.git"
        second_url = "https://github.com/owner/old"
        client = FakeGithubClient(
            {"Owner/Old": FakeRepository("Canonical/New")}
        )
        readme = (
            "## Trading & Backtesting\n"
            f"- [First]({first_url}) - `Python` - Entry.\n"
            f"- [Second]({second_url}) - `Python` - Entry.\n"
        )

        findings = self.audit(
            readme,
            client,
            {
                first_url: observation(first_url),
                second_url: observation(second_url),
            },
        )

        self.assertEqual(
            [finding.kind for finding in findings],
            [FindingKind.GITHUB_MOVED, FindingKind.GITHUB_MOVED],
        )
        self.assertEqual(client.repo_calls, ["Owner/Old"])
        self.assertTrue(
            all("https://github.com/Canonical/New" in finding.suggestion for finding in findings)
        )

    def test_active_fork_promotes_a_different_active_parent(self):
        url = "https://github.com/fork/project"
        parent = FakeRepository("upstream/project")
        client = FakeGithubClient(
            {"fork/project": FakeRepository("fork/project", fork=True, parent=parent)}
        )

        findings = self.audit(
            f"## Trading & Backtesting\n- [Project]({url}) - `Python` - Entry.\n",
            client,
            {url: observation(url)},
        )

        self.assertEqual([finding.kind for finding in findings], [FindingKind.GITHUB_PARENT])
        self.assertIn(parent.html_url, findings[0].suggestion)

    def test_active_non_fork_has_no_github_metadata_finding(self):
        url = "https://github.com/owner/project/"
        client = FakeGithubClient(
            {"owner/project": FakeRepository("OWNER/PROJECT", parent=FakeRepository("other/project"))}
        )

        findings = self.audit(
            f"## Trading & Backtesting\n- [Project]({url}) - `Python` - Entry.\n",
            client,
            {url: observation(url)},
        )

        self.assertEqual(findings, [])

    def test_empty_query_and_fragment_delimiters_are_not_github_repository_urls(self):
        urls = [
            "https://github.com/owner/query?",
            "https://github.com/owner/fragment#",
            "https://github.com/owner/slash-query/?",
            "https://github.com/owner/slash-fragment/#",
        ]
        readme = "## Trading & Backtesting\n" + "".join(
            f"- [Project {index}]({url}) - `Python` - Entry.\n"
            for index, url in enumerate(urls)
        )
        client = FakeGithubClient(
            {
                "owner/query": FakeRepository("owner/query"),
                "owner/fragment": FakeRepository("owner/fragment"),
                "owner/slash-query": FakeRepository("owner/slash-query"),
                "owner/slash-fragment": FakeRepository("owner/slash-fragment"),
            }
        )

        findings = self.audit(
            readme,
            client,
            {url: observation(url) for url in urls},
        )

        self.assertEqual(findings, [])
        self.assertEqual(client.repo_calls, [])

    def test_github_404_adds_no_metadata_finding_and_other_api_errors_escape(self):
        missing_url = "https://github.com/owner/missing"
        broken_url = "https://github.com/owner/broken"
        missing = GithubException(404, {"message": "Not Found"})
        broken = GithubException(500, {"message": "Unavailable"})

        findings = self.audit(
            f"## Trading & Backtesting\n- [Missing]({missing_url}) - `Python` - Entry.\n",
            FakeGithubClient({"owner/missing": missing}),
            {missing_url: observation(missing_url, Outcome.DEAD, status=404)},
        )
        self.assertEqual([finding.kind for finding in findings], [FindingKind.DEAD])

        with self.assertRaises(GithubException):
            self.audit(
                f"## Trading & Backtesting\n- [Broken]({broken_url}) - `Python` - Entry.\n",
                FakeGithubClient({"owner/broken": broken}),
                {broken_url: observation(broken_url)},
            )

    def test_candidates_are_bounded_filtered_deduplicated_ranked_and_strictly_eligible(self):
        eligible_url = "https://dead.example/tool"
        suffix_url = "https://dead.example/docs"
        github_url = "https://github.com/owner/dead-tool"
        linked_url = "https://dead.example/linked"
        historical_url = "https://dead.example/historical"
        readme = (
            "## Trading & Backtesting\n"
            f"- [Dead Tool]({eligible_url}) - `Python` - Entry.\n"
            f"- [Suffix Owner](https://ok.example) - `Python` - [Docs]({suffix_url}).\n"
            f"- [Dead Tool]({github_url}) - `Python` - Entry.\n"
            f"- [Linked Tool]({linked_url}) - `Python` - Entry. [GitHub](https://github.com/linked/tool)\n"
            "## Historical & Archived Projects\n"
            f"- [Historical Tool]({historical_url}) - `Historical` - Entry.\n"
        )
        exact = [
            FakeRepository("zeta/dead-tool", name="dead_tool", stars=10),
            FakeRepository("beta/DeadTool", name="DeadTool", stars=80),
            FakeRepository("BETA/deadtool", name="dead-tool", stars=70),
            FakeRepository("alpha/dead-tool", name="DEAD TOOL", stars=80),
            FakeRepository("gamma/dead-tool", name="dead.tool", stars=30),
            FakeRepository("archived/dead-tool", name="dead-tool", stars=500, archived=True),
            FakeRepository("disabled/dead-tool", name="dead-tool", stars=400, disabled=True),
            FakeRepository("wrong/something", name="something", stars=900),
        ]
        padding = [FakeRepository(f"wrong/pad-{index}", name=f"pad-{index}") for index in range(12)]
        beyond_cap = FakeRepository("beyond/dead-tool", name="dead-tool", stars=1000)
        client = FakeGithubClient(
            repos={
                "owner/dead-tool": FakeRepository("owner/dead-tool"),
                "linked/tool": FakeRepository("linked/tool"),
            },
            searches={"Dead Tool in:name": [*exact, *padding, beyond_cap]},
        )
        outcomes = {
            url: observation(
                url,
                Outcome.DEAD if url != "https://ok.example" else Outcome.OK,
                status=410 if url != "https://ok.example" else 200,
            )
            for url in (
                eligible_url,
                "https://ok.example",
                suffix_url,
                github_url,
                linked_url,
                "https://github.com/linked/tool",
                historical_url,
            )
        }

        findings = self.audit(readme, client, outcomes)
        candidate_findings = [finding for finding in findings if finding.kind == FindingKind.CANDIDATES]

        self.assertEqual(len(candidate_findings), 1)
        self.assertEqual(
            candidate_findings[0].candidates,
            (
                Candidate("alpha/dead-tool", "https://github.com/alpha/dead-tool", 80),
                Candidate("beta/DeadTool", "https://github.com/beta/DeadTool", 80),
                Candidate("gamma/dead-tool", "https://github.com/gamma/dead-tool", 30),
            ),
        )
        self.assertIn("410", candidate_findings[0].evidence)
        self.assertIn("manual verification", candidate_findings[0].suggestion.casefold())
        self.assertEqual(
            client.search_calls,
            [{"query": "Dead Tool in:name", "sort": "stars", "order": "desc"}],
        )

    def test_equal_star_case_variant_candidates_are_independent_of_api_order(self):
        url = "https://dead.example/tool"
        readme = (
            "## Trading & Backtesting\n"
            f"- [Dead Tool]({url}) - `Python` - Entry.\n"
        )
        upper = FakeRepository("OWNER/Dead-Tool", name="dead-tool", stars=40)
        lower = FakeRepository("owner/dead-tool", name="dead-tool", stars=40)

        selections = []
        for repositories in ((lower, upper), (upper, lower)):
            client = FakeGithubClient(
                searches={"Dead Tool in:name": repositories}
            )
            findings = self.audit(
                readme,
                client,
                {url: observation(url, Outcome.DEAD, status=404)},
            )
            selections.append(
                next(
                    finding.candidates
                    for finding in findings
                    if finding.kind == FindingKind.CANDIDATES
                )
            )

        expected = (
            Candidate("OWNER/Dead-Tool", "https://github.com/OWNER/Dead-Tool", 40),
        )
        self.assertEqual(selections, [expected, expected])

    def test_all_finding_kinds_are_mapped_and_sorted_deterministically(self):
        urls = {
            "dead": "https://dead.example",
            "transient": "https://transient.example",
            "restricted": "https://restricted.example",
            "error": "https://error.example",
            "redirect": "https://redirect.example",
            "moved": "https://github.com/old/moved",
            "archived": "https://github.com/owner/archived",
            "disabled": "https://github.com/owner/disabled",
            "parent": "https://github.com/fork/project",
        }
        readme = "## Trading & Backtesting\n" + "".join(
            f"- [{name.title()}]({url}) - `Python` - Entry.\n"
            for name, url in reversed(list(urls.items()))
        )
        client = FakeGithubClient(
            repos={
                "old/moved": FakeRepository("new/moved"),
                "owner/archived": FakeRepository("owner/archived", archived=True),
                "owner/disabled": FakeRepository("owner/disabled", disabled=True),
                "fork/project": FakeRepository(
                    "fork/project", fork=True, parent=FakeRepository("upstream/project")
                ),
            },
            searches={"Dead in:name": [FakeRepository("candidate/dead", name="dead", stars=4)]},
        )
        outcomes = {
            urls["dead"]: observation(urls["dead"], Outcome.DEAD, status=404),
            urls["transient"]: observation(
                urls["transient"], Outcome.TRANSIENT, status=503, attempts=3,
                error="retry limit exceeded: HTTP 503",
            ),
            urls["restricted"]: observation(urls["restricted"], Outcome.RESTRICTED, status=403),
            urls["error"]: observation(
                urls["error"], Outcome.HTTP_ERROR, status=None, error="unsafe URL"
            ),
            urls["redirect"]: observation(
                urls["redirect"], Outcome.PERMANENT_REDIRECT, status=200,
                final_url="https://redirect.example/new",
            ),
            urls["moved"]: observation(urls["moved"]),
            urls["archived"]: observation(urls["archived"]),
            urls["disabled"]: observation(urls["disabled"]),
            urls["parent"]: observation(urls["parent"]),
        }

        findings = self.audit(readme, client, outcomes)

        self.assertEqual([finding.kind for finding in findings], list(FindingKind))
        self.assertIn("3 attempts", findings[1].evidence)
        self.assertIn("503", findings[1].evidence)
        self.assertIn("next audit run", findings[1].suggestion)
        self.assertIn("manual browser", findings[2].suggestion)
        self.assertIn("manual diagnosis", findings[3].suggestion)
        self.assertIn("https://redirect.example/new", findings[4].evidence)
        self.assertIn("update", findings[4].suggestion.casefold())

    def test_eight_worker_out_of_order_probes_have_stable_results(self):
        urls = [f"https://project-{index}.example" for index in range(8)]
        readme = "## Trading & Backtesting\n" + "".join(
            f"- [Project {index}]({url}) - `Python` - Entry.\n"
            for index, url in enumerate(urls)
        )

        def run_with_delays(reverse):
            barrier = threading.Barrier(8)

            def delayed_probe(url):
                index = urls.index(url)
                barrier.wait(timeout=2)
                delay_index = index if reverse else 7 - index
                time.sleep(delay_index / 1000)
                return observation(url, Outcome.DEAD, status=404)

            return self.audit(readme, FakeGithubClient(), delayed_probe)

        forward = run_with_delays(False)
        reverse = run_with_delays(True)

        self.assertEqual(forward, reverse)
        self.assertEqual([finding.entry_name for finding in forward], [f"Project {i}" for i in range(8)])

    def audit(self, readme, client, observations):
        if callable(observations):
            prober = observations
        else:
            prober = observations.__getitem__
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text(readme, encoding="utf-8")
            return audit_readme(path, client, prober=prober)


if __name__ == "__main__":
    unittest.main()
