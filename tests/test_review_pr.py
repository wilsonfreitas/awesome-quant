import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import patch

from github import GithubException

from scripts.review_pr import (
    Finding,
    main,
    readme_has_duplicate,
    review_pr,
    url_reachable,
)


NOW = datetime(2026, 8, 10, tzinfo=timezone.utc)
ENTRY_URL = "https://github.com/example/fresh"
VALID_PATCH = """@@ -1,1 +1,2 @@
 ## Trading & Backtesting
+- [Fresh](https://github.com/example/fresh) - `Python` - Fresh project.
"""


class FakePull:
    def __init__(
        self,
        number,
        *,
        body="A useful contribution.",
        files=None,
        state="open",
        closed_at=None,
        title="Add Fresh",
        base_sha=None,
        head_sha=None,
        base_readme=None,
        head_readme=None,
        content_error=False,
    ):
        self.number = number
        self.body = body
        self.state = state
        self.closed_at = closed_at
        self.updated_at = closed_at or NOW
        self.title = title
        self.base = SimpleNamespace(
            sha=base_sha or ("base-sha" if number == 10 else f"base-{number}")
        )
        self.head = SimpleNamespace(
            sha=head_sha or ("head-sha" if number == 10 else f"head-{number}")
        )
        self._files = files if files is not None else [
            SimpleNamespace(filename="README.md", patch=VALID_PATCH)
        ]
        self.base_readme = base_readme or (
            "# awesome-quant\n\n"
            "## Trading & Backtesting\n"
        )
        added_lines = [
            line[1:]
            for changed_file in self._files
            if changed_file.filename == "README.md" and changed_file.patch
            for line in changed_file.patch.splitlines()
            if line.startswith("+- ")
        ]
        self.head_readme = head_readme or (
            self.base_readme.rstrip() + "\n" + "\n".join(added_lines) + "\n"
        )
        self.content_error = content_error

    def get_files(self):
        return list(self._files)


class FakeProjectRepository:
    def __init__(self):
        self.archived = False
        self.pushed_at = NOW
        self.has_root_readme = True
        self.has_readme = True
        self.readme_error = None

    def get_contents(self, path):
        if path != "README.md":
            raise AssertionError(f"unexpected project path: {path}")
        if not self.has_root_readme:
            raise RuntimeError("README not found")
        return SimpleNamespace(decoded_content=b"# Fresh")

    def get_readme(self):
        if self.readme_error:
            raise self.readme_error
        if not self.has_readme:
            raise GithubException(404, {"message": "Not Found"})
        return SimpleNamespace(decoded_content=b"# Fresh")


class FakeBaseRepository:
    default_branch = "main"

    def __init__(
        self,
        pull,
        *,
        other_pulls=(),
        base_readme=(
            "# awesome-quant\n\n"
            "## Trading & Backtesting\n"
        ),
        head_readme=None,
    ):
        self.pull = pull
        self.other_pulls = list(other_pulls)
        self.base_readme = base_readme
        self.head_readme = head_readme or (
            base_readme.rstrip()
            + "\n"
            + VALID_PATCH.splitlines()[-1][1:]
            + "\n"
        )
        self.pull_query_error = None
        self.content_refs = []

    def get_pull(self, number):
        if number != self.pull.number:
            raise AssertionError(f"unexpected PR number: {number}")
        return self.pull

    def get_contents(self, path, ref=None):
        if path != "README.md":
            raise AssertionError(f"unexpected base content request: {path}, {ref}")
        self.content_refs.append(ref)
        if ref in {self.default_branch, "base-sha"}:
            content = self.base_readme
        elif ref == "head-sha":
            content = self.head_readme
        else:
            matching_pull = next(
                (
                    pull
                    for pull in self.other_pulls
                    if ref in {pull.base.sha, pull.head.sha}
                ),
                None,
            )
            if matching_pull is None:
                raise AssertionError(f"unexpected README ref: {ref}")
            if matching_pull.content_error:
                raise RuntimeError("candidate README content should not be fetched")
            content = (
                matching_pull.base_readme
                if ref == matching_pull.base.sha
                else matching_pull.head_readme
            )
        return SimpleNamespace(decoded_content=content.encode())

    def get_pulls(self, **kwargs):
        if self.pull_query_error:
            raise self.pull_query_error
        state = kwargs.get("state")
        return [pull for pull in self.other_pulls if pull.state == state]


class FakeClient:
    def __init__(self, repository):
        self.repository = repository
        self.project_repository = FakeProjectRepository()
        self.requested_repositories = []

    def get_repo(self, name):
        self.requested_repositories.append(name)
        if name == "owner/list":
            return self.repository
        if name == "example/fresh":
            return self.project_repository
        raise AssertionError(f"unexpected repository: {name}")


class ReadmeDuplicateTests(unittest.TestCase):
    def test_rejects_exact_name_when_url_differs(self):
        readme = (
            "## Trading & Backtesting\n\n"
            "- [Example](https://github.com/example/old) - `Python` - Existing project.\n"
        )

        self.assertTrue(
            readme_has_duplicate(
                readme,
                "Example",
                ["https://github.com/example/new"],
            )
        )

    def test_does_not_match_url_prefix(self):
        readme = (
            "## Trading & Backtesting\n\n"
            "- [Other](https://github.com/example/freshness) - "
            "`Python` - Existing project.\n"
        )

        self.assertFalse(
            readme_has_duplicate(
                readme,
                "Fresh",
                ["https://github.com/example/fresh"],
            )
        )

    def test_matches_canonical_trailing_slash(self):
        readme = (
            "## Trading & Backtesting\n\n"
            "- [Fresh](https://github.com/example/fresh/) - "
            "`Python` - Existing project.\n"
        )

        self.assertTrue(
            readme_has_duplicate(
                readme,
                "Other Name",
                ["https://github.com/example/fresh"],
            )
        )



class UrlReachabilityTests(unittest.TestCase):
    @staticmethod
    def address(ip_address):
        return [(2, 1, 6, "", (ip_address, 443))]

    def test_rejects_non_https_url_without_network_request(self):
        requester = unittest.mock.Mock()

        self.assertFalse(
            url_reachable(
                "http://example.com/project",
                resolver=lambda *_args, **_kwargs: self.address("93.184.216.34"),
                requester=requester,
            )
        )
        requester.assert_not_called()

    def test_rejects_private_address_without_network_request(self):
        requester = unittest.mock.Mock()

        self.assertFalse(
            url_reachable(
                "https://localhost/project",
                resolver=lambda *_args, **_kwargs: self.address("127.0.0.1"),
                requester=requester,
            )
        )
        requester.assert_not_called()

    def test_rejects_mixed_public_and_private_dns_answers(self):
        requester = unittest.mock.Mock()

        self.assertFalse(
            url_reachable(
                "https://example.com/project",
                resolver=lambda *_args, **_kwargs: (
                    self.address("93.184.216.34") + self.address("10.0.0.1")
                ),
                requester=requester,
            )
        )
        requester.assert_not_called()

    def test_rejects_multicast_address_without_network_request(self):
        requester = unittest.mock.Mock()

        self.assertFalse(
            url_reachable(
                "https://example.com/project",
                resolver=lambda *_args, **_kwargs: self.address("224.0.0.1"),
                requester=requester,
            )
        )
        requester.assert_not_called()

    def test_rejects_port_zero_without_network_request(self):
        requester = unittest.mock.Mock()

        self.assertFalse(
            url_reachable(
                "https://example.com:0/project",
                resolver=lambda *_args, **_kwargs: self.address("93.184.216.34"),
                requester=requester,
            )
        )
        requester.assert_not_called()

    def test_accepts_public_url_without_following_redirect(self):
        requester = unittest.mock.Mock(return_value=302)

        self.assertTrue(
            url_reachable(
                "https://example.com/project?source=test",
                resolver=lambda *_args, **_kwargs: self.address("93.184.216.34"),
                requester=requester,
            )
        )
        requester.assert_called_once_with(
            "example.com",
            "93.184.216.34",
            443,
            "/project?source=test",
            "HEAD",
        )

    def test_retries_with_get_when_head_is_not_supported(self):
        requester = unittest.mock.Mock(side_effect=[405, 200])

        self.assertTrue(
            url_reachable(
                "https://example.com/project",
                resolver=lambda *_args, **_kwargs: self.address("93.184.216.34"),
                requester=requester,
            )
        )
        self.assertEqual(
            [call.args[-1] for call in requester.call_args_list],
            ["HEAD", "GET"],
        )


class PullRequestDuplicateTests(unittest.TestCase):
    def review(self, *, other_pulls=()):
        repository = FakeBaseRepository(
            FakePull(10),
            other_pulls=other_pulls,
        )
        client = FakeClient(repository)
        with patch("scripts.review_pr.url_reachable", return_value=True):
            findings, title = review_pr(
                "owner/list",
                10,
                client,
                now=NOW,
            )
        return findings, title, client

    def test_repository_name_is_an_explicit_input(self):
        findings, title, client = self.review()

        self.assertEqual(findings, [])
        self.assertEqual(title, "Add Fresh")
        self.assertEqual(client.requested_repositories[0], "owner/list")

    def test_rejects_duplicate_in_open_pull_request(self):
        duplicate = FakePull(
            9,
            body=f"Previously proposed {ENTRY_URL}",
        )

        findings, _title, _client = self.review(other_pulls=[duplicate])

        self.assertIn("duplicates", {finding.check for finding in findings})

    def test_rejects_duplicate_in_recently_closed_pull_request(self):
        duplicate = FakePull(
            8,
            body="Previously proposed Fresh",
            state="closed",
            closed_at=NOW - timedelta(days=30),
        )

        findings, _title, _client = self.review(other_pulls=[duplicate])

        self.assertIn("duplicates", {finding.check for finding in findings})

    def test_ignores_old_closed_pull_request(self):
        old_duplicate = FakePull(
            7,
            body=f"Previously proposed {ENTRY_URL}",
            state="closed",
            closed_at=NOW - timedelta(days=366),
            content_error=True,
        )

        findings, _title, _client = self.review(other_pulls=[old_duplicate])

        self.assertEqual(findings, [])

    def test_uses_full_readmes_when_candidate_patch_is_truncated(self):
        duplicate = FakePull(
            4,
            files=[
                SimpleNamespace(
                    filename="README.md",
                    patch="@@ -500,0 +501,1 @@\n context only",
                )
            ],
            head_readme=(
                "# awesome-quant\n\n"
                "## Trading & Backtesting\n"
                "- [Fresh](https://github.com/example/fresh) - "
                "`Python` - Fresh project.\n"
            ),
        )

        findings, _title, _client = self.review(other_pulls=[duplicate])

        self.assertIn("duplicates", {finding.check for finding in findings})

    def test_does_not_match_project_name_inside_unrelated_word(self):
        unrelated_patch = """@@ -1,1 +1,2 @@
 ## Trading & Backtesting
+- [Other](https://github.com/example/other) - `Python` - Other project.
"""
        unrelated = FakePull(
            6,
            title="Maintenance",
            body="Refresh metadata for the list.",
            files=[
                SimpleNamespace(
                    filename="README.md",
                    patch=unrelated_patch,
                )
            ],
        )

        findings, _title, _client = self.review(other_pulls=[unrelated])

        self.assertEqual(findings, [])

    def test_requires_matching_entry_not_matching_title(self):
        unrelated_patch = """@@ -1,1 +1,2 @@
 ## Trading & Backtesting
+- [Other](https://github.com/example/other) - `Python` - Other project.
"""
        unrelated = FakePull(
            5,
            title="Fresh ideas for the list",
            body="A maintenance proposal.",
            files=[
                SimpleNamespace(
                    filename="README.md",
                    patch=unrelated_patch,
                )
            ],
        )

        findings, _title, _client = self.review(other_pulls=[unrelated])

        self.assertEqual(findings, [])

    def test_pull_request_search_errors_fail_closed(self):
        repository = FakeBaseRepository(FakePull(10))
        repository.pull_query_error = RuntimeError("pull search failed")
        client = FakeClient(repository)

        with (
            patch("scripts.review_pr.url_reachable", return_value=True),
            self.assertRaisesRegex(RuntimeError, "pull search failed"),
        ):
            review_pr("owner/list", 10, client, now=NOW)


class ValidationPipelineTests(unittest.TestCase):
    def review(
        self,
        *,
        patch_text=VALID_PATCH,
        body="A useful contribution.",
        files=None,
        base_readme=(
            "# awesome-quant\n\n"
            "## Trading & Backtesting\n"
        ),
        head_readme=None,
        reachable=True,
        configure_project=None,
    ):
        changed_files = files or [
            SimpleNamespace(filename="README.md", patch=patch_text)
        ]
        if head_readme is None:
            section = "Trading & Backtesting"
            added_lines = []
            for raw_line in patch_text.splitlines():
                if raw_line.startswith(" ## "):
                    section = raw_line[4:]
                elif raw_line.startswith("+- "):
                    added_lines.append(raw_line[1:])
            heading = (
                ""
                if f"## {section}" in base_readme
                else f"\n## {section}\n"
            )
            head_readme = (
                base_readme.rstrip()
                + heading
                + "\n"
                + "\n".join(added_lines)
                + "\n"
            )
        repository = FakeBaseRepository(
            FakePull(10, body=body, files=changed_files),
            base_readme=base_readme,
            head_readme=head_readme,
        )
        client = FakeClient(repository)
        if configure_project:
            configure_project(client.project_repository)
        with patch(
            "scripts.review_pr.url_reachable",
            return_value=reachable,
        ):
            findings, _title = review_pr(
                "owner/list",
                10,
                client,
                now=NOW,
            )
        return {finding.check for finding in findings}

    def test_uses_pinned_base_and_head_readmes(self):
        repository = FakeBaseRepository(FakePull(10))
        client = FakeClient(repository)

        with patch("scripts.review_pr.url_reachable", return_value=True):
            review_pr("owner/list", 10, client, now=NOW)

        self.assertIn("base-sha", repository.content_refs)
        self.assertIn("head-sha", repository.content_refs)
        self.assertNotIn("main", repository.content_refs)

    def test_accepts_entry_when_heading_is_outside_patch_context(self):
        patch_text = """@@ -20,0 +21,1 @@
+- [Fresh](https://github.com/example/fresh) - `Python` - Fresh project.
"""
        head_readme = (
            "# awesome-quant\n\n"
            "## Trading & Backtesting\n\n"
            "- [Existing](https://github.com/example/existing) - "
            "`Python` - Existing project.\n"
            "- [Fresh](https://github.com/example/fresh) - "
            "`Python` - Fresh project.\n"
        )
        base_readme = head_readme.replace(
            "- [Fresh](https://github.com/example/fresh) - "
            "`Python` - Fresh project.\n",
            "",
        )

        self.assertNotIn(
            "placement",
            self.review(
                patch_text=patch_text,
                base_readme=base_readme,
                head_readme=head_readme,
            ),
        )

    def test_rejects_deleting_an_existing_entry(self):
        base_readme = (
            "# awesome-quant\n\n"
            "## Trading & Backtesting\n\n"
            "- [Existing](https://github.com/example/existing) - "
            "`Python` - Existing project.\n"
        )
        head_readme = (
            "# awesome-quant\n\n"
            "## Trading & Backtesting\n\n"
            "- [Fresh](https://github.com/example/fresh) - "
            "`Python` - Fresh project.\n"
        )

        self.assertIn(
            "content",
            self.review(
                base_readme=base_readme,
                head_readme=head_readme,
            ),
        )

    def test_accepts_valid_entry(self):
        self.assertEqual(self.review(), set())

    def test_rejects_empty_pr_description(self):
        self.assertIn("description", self.review(body=" "))

    def test_rejects_changes_outside_readme(self):
        files = [
            SimpleNamespace(filename="README.md", patch=VALID_PATCH),
            SimpleNamespace(filename="code.py", patch="+print(1)"),
        ]
        self.assertIn("files", self.review(files=files))

    def test_rejects_multiple_entries(self):
        patch_text = VALID_PATCH + (
            "+- [Other](https://github.com/example/other) - "
            "`Python` - Other project.\n"
        )
        self.assertIn("entry-count", self.review(patch_text=patch_text))

    def test_rejects_malformed_entry(self):
        patch_text = """@@ -1,1 +1,2 @@
 ## Trading & Backtesting
+- Fresh project without Markdown links
"""
        self.assertIn("format", self.review(patch_text=patch_text))

    def test_rejects_unknown_section(self):
        self.assertIn(
            "placement",
            self.review(
                patch_text=VALID_PATCH.replace(
                    "Trading & Backtesting",
                    "Unknown Section",
                )
            ),
        )

    def test_rejects_missing_tags(self):
        self.assertIn(
            "tags",
            self.review(
                patch_text=VALID_PATCH.replace(
                    "`Python` - ",
                    "",
                )
            ),
        )

    def test_rejects_tags_without_required_separator(self):
        self.assertIn(
            "tags",
            self.review(
                patch_text=VALID_PATCH.replace(
                    "`Python` - Fresh",
                    "`Python` Fresh",
                )
            ),
        )

    def test_rejects_description_without_period(self):
        self.assertIn(
            "period",
            self.review(
                patch_text=VALID_PATCH.replace(
                    "Fresh project.",
                    "Fresh project",
                )
            ),
        )

    def test_rejects_insecure_primary_url(self):
        self.assertIn(
            "url",
            self.review(
                patch_text=VALID_PATCH.replace(
                    "https://github.com/example/fresh",
                    "http://github.com/example/fresh",
                )
            ),
        )

    def test_rejects_insecure_trailing_url(self):
        patch_text = VALID_PATCH.replace(
            "Fresh project.",
            "Fresh project. [Website](http://example.com)",
        )
        self.assertIn("url", self.review(patch_text=patch_text))

    def test_rejects_malformed_github_suffix(self):
        patch_text = VALID_PATCH.replace(
            "Fresh project.",
            "Fresh project. [GitHub](http://github.com/example/fresh)",
        )
        self.assertIn("github-link", self.review(patch_text=patch_text))

    def test_rejects_github_link_that_is_not_the_suffix(self):
        patch_text = VALID_PATCH.replace(
            "Fresh project.",
            (
                "Fresh project. "
                "[GitHub](https://github.com/example/fresh) trailing text"
            ),
        )
        self.assertIn("github-link", self.review(patch_text=patch_text))

    def test_rejects_entry_without_github_repository(self):
        patch_text = VALID_PATCH.replace(
            "https://github.com/example/fresh",
            "https://example.com/fresh",
        )
        self.assertIn("github", self.review(patch_text=patch_text))

    def test_rejects_non_repository_github_path(self):
        patch_text = VALID_PATCH.replace(
            "https://github.com/example/fresh",
            "https://github.com/example/fresh/issues",
        )
        self.assertIn("github", self.review(patch_text=patch_text))

    def test_rejects_archived_repository(self):
        def archive(repository):
            repository.archived = True

        self.assertIn(
            "activity",
            self.review(configure_project=archive),
        )

    def test_rejects_stale_repository(self):
        def make_stale(repository):
            repository.pushed_at = NOW - timedelta(days=366)

        self.assertIn(
            "activity",
            self.review(configure_project=make_stale),
        )

    def test_rejects_repository_without_readme(self):
        def remove_readme(repository):
            repository.has_root_readme = False
            repository.has_readme = False

        self.assertIn(
            "documentation",
            self.review(configure_project=remove_readme),
        )

    def test_accepts_alternate_readme_name(self):
        def use_alternate_readme(repository):
            repository.has_root_readme = False
            repository.has_readme = True

        self.assertNotIn(
            "documentation",
            self.review(configure_project=use_alternate_readme),
        )

    def test_readme_api_error_fails_closed(self):
        def fail_readme_lookup(repository):
            repository.readme_error = GithubException(
                500,
                {"message": "Server Error"},
            )

        with self.assertRaises(GithubException):
            self.review(configure_project=fail_readme_lookup)

    def test_rejects_unreachable_primary_url(self):
        self.assertIn("reachability", self.review(reachable=False))

    def test_rejects_duplicate_in_base_readme(self):
        base_readme = (
            "## Trading & Backtesting\n"
            "- [Fresh](https://github.com/example/old) - "
            "`Python` - Existing project.\n"
        )
        self.assertIn(
            "duplicates",
            self.review(base_readme=base_readme),
        )


class MainTests(unittest.TestCase):
    def run_main(self, review_result):
        stdout = io.StringIO()
        stderr = io.StringIO()
        environment = {
            "GITHUB_TOKEN": "token",
            "GITHUB_REPOSITORY": "owner/list",
            "PR_NUMBER": "10",
        }
        with (
            patch.dict("os.environ", environment, clear=True),
            patch("sys.argv", ["review_pr.py"]),
            patch("scripts.review_pr.Github"),
            patch("scripts.review_pr.review_pr", return_value=review_result),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            result = main()
        return result, stdout.getvalue(), stderr.getvalue()

    def test_success_reports_passed_checks(self):
        result, stdout, _stderr = self.run_main(([], "Add Fresh"))

        self.assertEqual(result, 0)
        self.assertIn("description: pass", stdout)
        self.assertIn("duplicates: pass", stdout)

    def test_failure_reports_failed_check_and_nonzero_status(self):
        finding = Finding("description", "PR body is empty")

        result, stdout, _stderr = self.run_main(([finding], "Add Fresh"))

        self.assertEqual(result, 1)
        self.assertIn("description: fail - PR body is empty", stdout)

    def test_api_error_fails_closed(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        environment = {
            "GITHUB_TOKEN": "token",
            "GITHUB_REPOSITORY": "owner/list",
            "PR_NUMBER": "10",
        }
        with (
            patch.dict("os.environ", environment, clear=True),
            patch("sys.argv", ["review_pr.py"]),
            patch("scripts.review_pr.Github"),
            patch(
                "scripts.review_pr.review_pr",
                side_effect=RuntimeError("API failed"),
            ),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            result = main()

        self.assertEqual(result, 2)
        self.assertIn("ERROR API failed", stderr.getvalue())

    def test_invalid_pr_number_fails_closed(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        environment = {
            "GITHUB_TOKEN": "token",
            "GITHUB_REPOSITORY": "owner/list",
            "PR_NUMBER": "not-a-number",
        }
        with (
            patch.dict("os.environ", environment, clear=True),
            patch("sys.argv", ["review_pr.py"]),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            result = main()

        self.assertEqual(result, 2)
        self.assertIn("ERROR PR_NUMBER must be an integer", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
