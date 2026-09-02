import tempfile
import threading
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from github import GithubException

from scripts.audit_readme import (
    AuditTarget,
    Candidate,
    FindingKind,
    audit_readme,
    collect_targets,
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


class AuditReadmeTests(unittest.TestCase):
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
