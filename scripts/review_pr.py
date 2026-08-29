#!/usr/bin/env python3
"""Automated PR reviewer for awesome-quant README contributions."""

from __future__ import annotations

import argparse
import difflib
import http.client
import ipaddress
import os
import re
import socket
import ssl
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlsplit, urlunsplit

from github import Auth, Github, GithubException

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.readme_entries import (
    ENTRY_RE,
    GITHUB_LINK_RE,
    MARKDOWN_URL_RE,
    VALID_SECTIONS,
    extract_languages,
)


NO_TAG_SECTIONS = {
    "Commercial & Proprietary Services",
    "Cross-Language Frameworks",
    "Reproducing Works, Training & Books",
    "Related Lists",
}

RECENT_CLOSED_PULL_DAYS = 365
MAX_README_ENTRIES_PER_PR = 5
CHECK_ORDER = (
    "description",
    "files",
    "entry-count",
    "content",
    "format",
    "placement",
    "tags",
    "period",
    "url",
    "github-link",
    "github",
    "activity",
    "documentation",
    "reachability",
    "duplicates",
)


@dataclass(frozen=True)
class Finding:
    check: str
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Review one awesome-quant pull request."
    )
    parser.add_argument("--pr-number", type=int, default=None)
    parser.add_argument(
        "--skip-pull-request-duplicates",
        action="store_true",
        help="skip duplicate checks against open and recently closed PRs",
    )
    return parser.parse_args()


def env(name: str) -> str | None:
    value = os.environ.get(name, "").strip()
    return value or None


def fail(message: str) -> int:
    print(f"ERROR {message}", file=sys.stderr)
    return 2


def normalize(text: str) -> str:
    return " ".join(text.casefold().split())


def canonicalize_url(url: str) -> str:
    parsed = urlsplit(url.strip())
    scheme = parsed.scheme.casefold()
    hostname = (parsed.hostname or "").casefold()
    port = parsed.port
    if port and not (
        (scheme == "https" and port == 443)
        or (scheme == "http" and port == 80)
    ):
        netloc = f"{hostname}:{port}"
    else:
        netloc = hostname
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((scheme, netloc, path, parsed.query, ""))


def parse_github_repository_url(url: str) -> tuple[str, str] | None:
    parsed = urlsplit(url.strip())
    if (
        parsed.scheme.casefold() != "https"
        or parsed.hostname != "github.com"
        or parsed.port is not None
        or parsed.query
        or parsed.fragment
    ):
        return None
    path_parts = [part for part in parsed.path.split("/") if part]
    if len(path_parts) != 2:
        return None
    return path_parts[0], path_parts[1]


def description_ends_with_period(description: str) -> bool:
    github_match = GITHUB_LINK_RE.search(description)
    text = description[: github_match.start()].rstrip() if github_match else description
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"\s*\[[^\]]+\]\([^)]+\)\s*$", "", text).rstrip()
        text = re.sub(
            r"\s*\(\[[^\]]+\]\([^)]+\)\)\s*$",
            "",
            text,
        ).rstrip()
    return bool(text) and text.endswith(".")


def parse_patch(patch: str | None) -> list[tuple[str, str]]:
    if not patch:
        return []

    result: list[tuple[str, str]] = []
    section = ""
    for raw_line in patch.splitlines():
        if raw_line.startswith("@@"):
            continue
        if raw_line.startswith("+"):
            line = raw_line[1:]
            stripped = line.strip()
            if stripped.startswith("## "):
                section = stripped[3:].strip()
            result.append((section, line))
        elif raw_line.startswith(" "):
            line = raw_line[1:]
            stripped = line.strip()
            if stripped.startswith("## "):
                section = stripped[3:].strip()
    return result


def extract_entry_line(added_lines: list[tuple[str, str]]) -> tuple[str, str] | None:
    entry_lines = [item for item in added_lines if item[1].strip().startswith("- ")]
    if len(entry_lines) != 1:
        return None
    return entry_lines[0]


def read_readme(repository: Any, ref: str) -> str:
    content = repository.get_contents("README.md", ref=ref)
    if isinstance(content, list):
        raise RuntimeError(f"README.md at {ref} did not resolve to a file")
    return content.decoded_content.decode("utf-8")


def entries_represent_same_project(old_line: str, new_line: str) -> bool:
    old_match = ENTRY_RE.match(old_line)
    new_match = ENTRY_RE.match(new_line)
    if old_match is None or new_match is None:
        return False

    if normalize(old_match.group(1)) == normalize(new_match.group(1)):
        return True

    old_urls = {
        canonicalize_url(url) for url in MARKDOWN_URL_RE.findall(old_line)
    }
    new_urls = {
        canonicalize_url(url) for url in MARKDOWN_URL_RE.findall(new_line)
    }
    return bool(old_urls & new_urls)


def analyze_readme_change(
    base_readme: str,
    head_readme: str,
) -> tuple[list[str], list[str], list[Finding]]:
    added_lines, removed_lines = readme_changed_lines(base_readme, head_readme)
    substantive_added = [line for line in added_lines if line.strip()]
    substantive_removed = [line for line in removed_lines if line.strip()]
    entry_lines = [
        line for line in substantive_added if line.strip().startswith("- ")
    ]
    removed_entry_lines = [
        line for line in substantive_removed if line.strip().startswith("- ")
    ]
    findings: list[Finding] = []
    if not 1 <= len(entry_lines) <= MAX_README_ENTRIES_PER_PR:
        findings.append(
            Finding(
                "entry-count",
                "expected between one and five added README entry lines",
            )
        )
        return [], [], findings

    unauthorized_additions = [
        line for line in substantive_added if line not in entry_lines
    ]
    unauthorized_removals = [
        line for line in substantive_removed if line not in removed_entry_lines
    ]
    unmatched_entry_lines = list(entry_lines)
    unmatched_removal = False
    for removed_entry_line in removed_entry_lines:
        matching_index = next(
            (
                index
                for index, entry_line in enumerate(unmatched_entry_lines)
                if entries_represent_same_project(removed_entry_line, entry_line)
            ),
            None,
        )
        if matching_index is None:
            unmatched_removal = True
            break
        unmatched_entry_lines.pop(matching_index)
    invalid_update = bool(substantive_removed) and (
        bool(unauthorized_removals) or unmatched_removal
    )
    if unauthorized_additions or invalid_update:
        findings.append(
            Finding(
                "content",
                "README changes must add up to five entries or update the same projects "
                "without other substantive edits",
            )
        )
    return entry_lines, removed_entry_lines, findings


def remove_entry_lines(readme_text: str, entry_lines: list[str]) -> str:
    lines = readme_text.splitlines()
    for entry_line in entry_lines:
        lines.remove(entry_line)
    return "\n".join(lines)


def readme_changed_lines(
    base_readme: str,
    head_readme: str,
) -> tuple[list[str], list[str]]:
    base_lines = base_readme.splitlines()
    head_lines = head_readme.splitlines()
    added_lines: list[str] = []
    removed_lines: list[str] = []
    matcher = difflib.SequenceMatcher(
        a=base_lines,
        b=head_lines,
        autojunk=False,
    )
    for operation, base_start, base_end, head_start, head_end in matcher.get_opcodes():
        if operation in {"replace", "delete"}:
            removed_lines.extend(base_lines[base_start:base_end])
        if operation in {"replace", "insert"}:
            added_lines.extend(head_lines[head_start:head_end])
    return added_lines, removed_lines


def find_entry_section(readme_text: str, entry_line: str) -> str:
    current_section = ""
    matches = 0
    matched_section = ""
    for line in readme_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("### "):
            current_section = stripped[3:].strip()
        if line == entry_line:
            matches += 1
            matched_section = current_section
    if matches != 1:
        raise RuntimeError(
            "added README entry could not be located uniquely in the PR head"
        )
    return matched_section


class PinnedHTTPSConnection(http.client.HTTPSConnection):
    """HTTPS connection pinned to an address that was checked as public."""

    def __init__(self, hostname: str, ip_address: str, port: int) -> None:
        context = ssl.create_default_context()
        super().__init__(
            hostname,
            port=port,
            timeout=5,
            context=context,
        )
        self.ip_address = ip_address
        self.ssl_context = context

    def connect(self) -> None:
        sock = socket.create_connection(
            (self.ip_address, self.port),
            self.timeout,
        )
        self.sock = self.ssl_context.wrap_socket(sock, server_hostname=self.host)


def request_url_status(
    hostname: str,
    ip_address: str,
    port: int,
    target: str,
    method: str,
) -> int:
    connection = PinnedHTTPSConnection(hostname, ip_address, port)
    try:
        connection.request(
            method,
            target,
            headers={
                "Accept": "*/*",
                "User-Agent": "awesome-quant-pr-review",
            },
        )
        return connection.getresponse().status
    finally:
        connection.close()


def url_reachable(
    url: str,
    *,
    resolver: Callable[..., list[tuple[Any, ...]]] = socket.getaddrinfo,
    requester: Callable[[str, str, int, str, str], int] = request_url_status,
) -> bool:
    try:
        parsed = urlsplit(url)
        if (
            parsed.scheme.casefold() != "https"
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
        ):
            return False
        parsed_port = parsed.port
        if parsed_port == 0:
            return False
        port = parsed_port or 443
        addresses = {
            result[4][0]
            for result in resolver(
                parsed.hostname,
                port,
                type=socket.SOCK_STREAM,
            )
        }
        address_objects = [ipaddress.ip_address(address) for address in addresses]
        if not address_objects or any(
            not address.is_global
            or address.is_multicast
            or address.is_loopback
            or address.is_link_local
            or address.is_private
            or address.is_reserved
            or address.is_unspecified
            for address in address_objects
        ):
            return False

        target = parsed.path or "/"
        if parsed.query:
            target = f"{target}?{parsed.query}"
        for method in ("HEAD", "GET"):
            status = requester(
                parsed.hostname,
                sorted(addresses)[0],
                port,
                target,
                method,
            )
            if status not in {405, 501}:
                return 200 <= status < 400
        return False
    except (OSError, ValueError, ssl.SSLError):
        return False


def readme_has_duplicate(readme_text: str, name: str, urls: list[str]) -> bool:
    name_key = normalize(name)
    url_keys = {canonicalize_url(url) for url in urls if url}
    for line in readme_text.splitlines():
        match = ENTRY_RE.match(line)
        if match and normalize(match.group(1)) == name_key:
            return True
        if match:
            existing_urls = {
                canonicalize_url(url)
                for url in MARKDOWN_URL_RE.findall(line)
            }
            if url_keys & existing_urls:
                return True
    return False


def entry_line_has_duplicate(line: str, name: str, urls: list[str]) -> bool:
    match = ENTRY_RE.match(line)
    if not match:
        return False
    if normalize(match.group(1)) == normalize(name):
        return True
    target_urls = {canonicalize_url(url) for url in urls if url}
    entry_urls = {
        canonicalize_url(url)
        for url in MARKDOWN_URL_RE.findall(line)
    }
    return bool(target_urls & entry_urls)


def pull_request_has_duplicate(
    repository: Any,
    pull_request: Any,
    name: str,
    urls: list[str],
    *,
    readme_cache: dict[str, str] | None = None,
) -> bool:
    cache = readme_cache if readme_cache is not None else {}

    def cached_readme(ref: str) -> str:
        if ref not in cache:
            cache[ref] = read_readme(repository, ref)
        return cache[ref]

    head_readme = cached_readme(pull_request.head.sha)
    if not readme_has_duplicate(head_readme, name, urls):
        return False

    base_readme = cached_readme(pull_request.base.sha)
    added_lines, _removed_lines = readme_changed_lines(base_readme, head_readme)
    return any(
        entry_line_has_duplicate(line, name, urls)
        for line in added_lines
        if line.strip().startswith("- ")
    )


def repository_has_pull_request_duplicate(
    repository: Any,
    current_pr_number: int,
    name: str,
    urls: list[str],
    *,
    now: datetime,
    readme_cache: dict[str, str] | None = None,
) -> bool:
    cache = readme_cache if readme_cache is not None else {}
    cutoff = now - timedelta(days=RECENT_CLOSED_PULL_DAYS)
    for state in ("open", "closed"):
        pulls = repository.get_pulls(
            state=state,
            sort="updated",
            direction="desc",
        )
        for pull_request in pulls:
            if pull_request.number == current_pr_number:
                continue
            if state == "closed":
                if pull_request.updated_at < cutoff:
                    break
                closed_at = pull_request.closed_at
                if closed_at is None or closed_at < cutoff:
                    continue
            if pull_request_has_duplicate(
                repository,
                pull_request,
                name,
                urls,
                readme_cache=cache,
            ):
                return True
    return False


def review_entry(
    repository: Any,
    client: Github,
    pr_number: int,
    line: str,
    *,
    current_time: datetime,
    head_readme: str,
    duplicate_base_readme: str,
    other_entry_lines: list[str],
    check_pull_request_duplicates: bool,
    readme_cache: dict[str, str],
) -> list[Finding]:
    findings: list[Finding] = []
    match = ENTRY_RE.match(line)
    if not match:
        findings.append(
            Finding("format", "added README bullet does not match the entry regex")
        )
        return findings

    section = find_entry_section(head_readme, line)
    name = match.group(1).strip()
    url = match.group(2).strip()
    tail = match.group(3).strip()
    tags, clean_description = extract_languages(tail)

    if section not in VALID_SECTIONS:
        findings.append(
            Finding("placement", f"entry is under unknown section {section!r}")
        )

    if section not in NO_TAG_SECTIONS and not tags:
        findings.append(Finding("tags", "missing required backtick tag prefix"))

    github_label_count = clean_description.count("[GitHub](")
    github_marker = clean_description.rfind("[GitHub](")
    github_suffix = (
        clean_description[github_marker:]
        if github_marker >= 0
        else ""
    )
    if github_label_count and (
        github_label_count != 1
        or GITHUB_LINK_RE.fullmatch(github_suffix) is None
    ):
        findings.append(
            Finding(
                "github-link",
                "optional GitHub link must use "
                "[GitHub](https://github.com/owner/repo)",
            )
        )

    if not description_ends_with_period(clean_description):
        findings.append(
            Finding(
                "period",
                "description must end with a period before the optional GitHub link",
            )
        )

    for markdown_url in MARKDOWN_URL_RE.findall(line):
        if not markdown_url.startswith("https://"):
            findings.append(
                Finding("url", f"URL must use https://: {markdown_url}")
            )

    github_urls: list[str] = []
    primary_github = parse_github_repository_url(url)
    if primary_github:
        github_urls.append(url)
    elif (urlsplit(url).hostname or "").casefold() == "github.com":
        findings.append(
            Finding("github", f"invalid GitHub repository URL: {url}")
        )
    github_urls.extend(GITHUB_LINK_RE.findall(line))
    github_urls = list(dict.fromkeys(github_urls))
    if not github_urls:
        if section != "Commercial & Proprietary Services":
            findings.append(
                Finding(
                    "github",
                    "no GitHub repository URL found; cannot verify activity",
                )
            )
    else:
        repository_parts = parse_github_repository_url(github_urls[0])
        if not repository_parts:
            findings.append(
                Finding(
                    "github", f"unable to parse GitHub repository URL: {github_urls[0]}"
                )
            )
        else:
            owner, repo_name = repository_parts
            github_repo = client.get_repo(f"{owner}/{repo_name}")
            if github_repo.archived:
                findings.append(Finding("activity", "repository is archived"))
            pushed_at = github_repo.pushed_at
            if (
                pushed_at is None
                or pushed_at < current_time - timedelta(days=365)
            ):
                findings.append(
                    Finding(
                        "activity",
                        "repository has not been updated within the last 365 days",
                    )
                )
            try:
                github_repo.get_readme()
            except GithubException as exc:
                if exc.status != 404:
                    raise
                findings.append(
                    Finding(
                        "documentation",
                        "repository does not have a README",
                    )
                )

    if not primary_github and not url_reachable(url):
        findings.append(Finding("reachability", f"primary URL is not reachable: {url}"))

    entry_urls = [url, *github_urls]
    if readme_has_duplicate(duplicate_base_readme, name, entry_urls):
        findings.append(
            Finding("duplicates", "project name or URL already exists in README.md")
        )
    elif any(
        entry_line_has_duplicate(other_line, name, entry_urls)
        for other_line in other_entry_lines
    ):
        findings.append(
            Finding("duplicates", "project name or URL is duplicated within this PR")
        )
    elif check_pull_request_duplicates and repository_has_pull_request_duplicate(
        repository,
        pr_number,
        name,
        entry_urls,
        now=current_time,
        readme_cache=readme_cache,
    ):
        findings.append(
            Finding(
                "duplicates",
                "project name or URL already exists in an open or recently closed PR",
            )
        )

    return findings


def review_pr(
    repository_name: str,
    pr_number: int,
    client: Github,
    *,
    now: datetime | None = None,
    check_pull_request_duplicates: bool = True,
) -> tuple[list[Finding], str, int]:
    current_time = now or datetime.now(timezone.utc)

    repository = client.get_repo(repository_name)
    pull_request = repository.get_pull(pr_number)
    findings: list[Finding] = []

    if not (pull_request.body or "").strip():
        findings.append(Finding("description", "PR body is empty"))

    files = list(pull_request.get_files())
    if len(files) != 1 or files[0].filename != "README.md":
        changed = ", ".join(file.filename for file in files) or "none"
        findings.append(
            Finding("files", f"only README.md may change, found: {changed}")
        )
        return findings, pull_request.title, 0

    base_readme = read_readme(repository, pull_request.base.sha)
    head_readme = read_readme(repository, pull_request.head.sha)
    entry_lines, removed_entry_lines, change_findings = analyze_readme_change(
        base_readme,
        head_readme,
    )
    findings.extend(change_findings)
    if not entry_lines:
        return findings, pull_request.title, 0

    duplicate_base_readme = remove_entry_lines(base_readme, removed_entry_lines)
    readme_cache = {
        pull_request.base.sha: base_readme,
        pull_request.head.sha: head_readme,
    }
    for index, entry_line in enumerate(entry_lines):
        findings.extend(
            review_entry(
                repository,
                client,
                pr_number,
                entry_line,
                current_time=current_time,
                head_readme=head_readme,
                duplicate_base_readme=duplicate_base_readme,
                other_entry_lines=entry_lines[:index] + entry_lines[index + 1 :],
                check_pull_request_duplicates=check_pull_request_duplicates,
                readme_cache=readme_cache,
            )
        )

    return findings, pull_request.title, len(entry_lines)


def main() -> int:
    args = parse_args()
    if args.pr_number is not None:
        pr_number = args.pr_number
    else:
        raw_pr_number = env("PR_NUMBER")
        if raw_pr_number is None:
            return fail("PR number is required via --pr-number or PR_NUMBER")
        try:
            pr_number = int(raw_pr_number)
        except ValueError:
            return fail("PR_NUMBER must be an integer")
    if pr_number <= 0:
        return fail("PR number is required via --pr-number or PR_NUMBER")

    token = env("GITHUB_TOKEN") or env("GITHUB_ACCESS_TOKEN")
    if not token:
        return fail("GITHUB_TOKEN or GITHUB_ACCESS_TOKEN is required")

    try:
        repository_name = env("GITHUB_REPOSITORY")
        if not repository_name:
            return fail("GITHUB_REPOSITORY is required")
        client = Github(auth=Auth.Token(token))
        findings, title, entries_reviewed = review_pr(
            repository_name,
            pr_number,
            client,
            check_pull_request_duplicates=not args.skip_pull_request_duplicates,
        )
    except Exception as exc:
        return fail(str(exc))

    print(f"PR #{pr_number}: {title}")
    print(f"Entries reviewed: {entries_reviewed}")
    if args.skip_pull_request_duplicates:
        print("Cross-PR duplicate check: skipped")
    if not findings:
        for check in CHECK_ORDER:
            if check == "duplicates" and args.skip_pull_request_duplicates:
                print("- duplicates: pass (existing README only)")
            else:
                print(f"- {check}: pass")
        print("Verdict: APPROVE")
        print("Recommended action: merge")
        return 0

    print("Findings:")
    for finding in findings:
        print(f"- {finding.check}: fail - {finding.detail}")
    print("Verdict: NEEDS CHANGES")
    print("Recommended action: no action")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
