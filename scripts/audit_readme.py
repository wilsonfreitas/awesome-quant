"""Deterministic README link and GitHub repository audit orchestration."""

from __future__ import annotations

import argparse
import os
import re
import string
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from itertools import islice
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import urlsplit

from github import Auth, Github, GithubException

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.readme_entries import (
    HISTORICAL_SECTION,
    ReadmeEntry,
    iter_readme_entries,
)
from scripts.url_probe import Outcome, UrlObservation, probe_url

TRACKING_TITLE = "Weekly README audit report"
TRACKING_MARKER = "<!-- awesome-quant-readme-audit -->"


class FindingKind(StrEnum):
    DEAD = "dead"
    TRANSIENT = "transient"
    RESTRICTED = "restricted"
    HTTP_ERROR = "http_error"
    PERMANENT_REDIRECT = "permanent_redirect"
    GITHUB_MOVED = "github_moved"
    GITHUB_ARCHIVED = "github_archived"
    GITHUB_DISABLED = "github_disabled"
    GITHUB_PARENT = "github_parent"
    CANDIDATES = "candidates"


FINDING_ORDER = {kind: index for index, kind in enumerate(FindingKind)}

_REPORT_SECTIONS = (
    ("Confirmed dead links", (FindingKind.DEAD,)),
    ("Repeated transient failures", (FindingKind.TRANSIENT,)),
    ("Access-restricted links", (FindingKind.RESTRICTED,)),
    ("Other HTTP failures", (FindingKind.HTTP_ERROR,)),
    ("Permanent redirects", (FindingKind.PERMANENT_REDIRECT,)),
    (
        "GitHub repository findings",
        (
            FindingKind.GITHUB_MOVED,
            FindingKind.GITHUB_ARCHIVED,
            FindingKind.GITHUB_DISABLED,
            FindingKind.GITHUB_PARENT,
        ),
    ),
    ("Candidate replacements", (FindingKind.CANDIDATES,)),
)
_REPORT_SECTION_ORDER = {
    kind: index
    for index, (_heading, kinds) in enumerate(_REPORT_SECTIONS)
    for kind in kinds
}
_MARKDOWN_CONTROLS = frozenset(string.punctuation)
_URL_RE = re.compile(r"(?<!<)https?://[^\s<>]+")


@dataclass(frozen=True)
class AuditTarget:
    entry: ReadmeEntry
    url: str
    is_primary: bool


@dataclass(frozen=True)
class Candidate:
    full_name: str
    url: str
    stars: int


@dataclass(frozen=True)
class Finding:
    kind: FindingKind
    section: str
    entry_name: str
    line_number: int
    url: str
    evidence: str
    suggestion: str
    candidates: tuple[Candidate, ...] = ()


def _candidate_sort_key(candidate: Candidate) -> tuple[Any, ...]:
    return (
        -candidate.stars,
        candidate.full_name.casefold(),
        candidate.full_name,
        candidate.url,
    )


def _sorted_candidates(finding: Finding) -> tuple[Candidate, ...]:
    return tuple(sorted(finding.candidates, key=_candidate_sort_key)[:3])


def _report_sort_key(finding: Finding) -> tuple[Any, ...]:
    return (
        _REPORT_SECTION_ORDER[finding.kind],
        finding.section,
        finding.entry_name,
        finding.line_number,
        finding.url,
        finding.evidence,
        finding.suggestion,
        tuple(_candidate_sort_key(candidate) for candidate in _sorted_candidates(finding)),
    )


def _escape_markdown(text: str) -> str:
    text = " ".join(text.splitlines())
    return "".join(
        f"\\{character}" if character in _MARKDOWN_CONTROLS else character
        for character in text
    )


def _render_text(text: str) -> str:
    text = " ".join(text.split())

    def angle_link(match: re.Match[str]) -> str:
        value = match.group(0)
        url = value.rstrip(".,;:!?")
        return f"<{url}>{value[len(url):]}"

    return _URL_RE.sub(angle_link, text)


def render_report(findings: Iterable[Finding], *, checked_at: datetime) -> str:
    """Render findings as stable Markdown suitable for the tracking issue body."""
    ordered_findings = sorted(findings, key=_report_sort_key)
    checked_at_utc = checked_at.astimezone(timezone.utc)
    lines = [
        TRACKING_MARKER,
        f"# {TRACKING_TITLE}",
        "",
        f"Checked: {checked_at_utc:%Y-%m-%d %H:%M} UTC",
        "Entries are reported for manual review; this automation did not modify README.md.",
        "",
    ]
    if not ordered_findings:
        return "\n".join((*lines, "No findings.", ""))

    findings_by_kind: dict[FindingKind, list[Finding]] = {
        kind: [] for kind in FindingKind
    }
    for finding in ordered_findings:
        findings_by_kind[finding.kind].append(finding)

    for heading, kinds in _REPORT_SECTIONS:
        section_findings = [
            finding for kind in kinds for finding in findings_by_kind[kind]
        ]
        if not section_findings:
            continue
        lines.extend((f"## {heading}", ""))
        for finding in section_findings:
            lines.append(
                f"- **Entry:** {_escape_markdown(finding.entry_name)}; "
                f"**README line:** {finding.line_number}; "
                f"**Section:** {_escape_markdown(finding.section)}; "
                f"**Checked URL:** <{finding.url}>; "
                f"**Evidence:** {_render_text(finding.evidence)}; "
                f"**Manual suggestion:** {_render_text(finding.suggestion)}"
            )
            for index, candidate in enumerate(_sorted_candidates(finding), start=1):
                lines.append(
                    f"  - **Candidate {index}:** {candidate.full_name} — "
                    f"<{candidate.url}> — {candidate.stars} stars"
                )
        lines.append("")
    return "\n".join(lines)


def sync_tracking_issue(
    repository: Any,
    findings: Iterable[Finding],
    body: str,
) -> str:
    """Create or transition the single marked README audit tracking issue."""
    has_findings = bool(tuple(findings))
    matches = [
        issue
        for issue in repository.get_issues(state="all")
        if issue.title == TRACKING_TITLE and TRACKING_MARKER in (issue.body or "")
    ]
    if len(matches) > 1:
        raise RuntimeError("multiple tracking issues found")
    if not matches:
        if not has_findings:
            return "clean"
        repository.create_issue(title=TRACKING_TITLE, body=body)
        return "created"

    issue = matches[0]
    desired_state = "open" if has_findings else "closed"
    changes = {}
    if issue.body != body:
        changes["body"] = body
    if issue.state != desired_state:
        changes["state"] = desired_state
    if not changes:
        return "unchanged"

    state_changed = "state" in changes
    issue.edit(**changes)
    if state_changed:
        return "reopened" if has_findings else "closed"
    return "updated"


def collect_targets(readme_path: str | Path) -> list[AuditTarget]:
    """Collect every entry URL in README source order with its entry context."""
    return [
        AuditTarget(entry, url, url == entry.url)
        for entry in iter_readme_entries(readme_path)
        for url in entry.external_urls
    ]


def _parse_github_repository_url(url: str) -> str | None:
    if "?" in url or "#" in url:
        return None
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError:
        return None
    if (
        parsed.scheme.casefold() not in {"http", "https"}
        or parsed.netloc.casefold() != "github.com"
        or parsed.username is not None
        or parsed.password is not None
        or port is not None
        or parsed.query
        or parsed.fragment
    ):
        return None

    path = parsed.path[:-1] if parsed.path.endswith("/") else parsed.path
    parts = path.split("/")
    if len(parts) != 3 or parts[0] or not parts[1] or not parts[2]:
        return None
    repository = parts[2][:-4] if parts[2].casefold().endswith(".git") else parts[2]
    if not repository:
        return None
    return f"{parts[1]}/{repository}"


def _finding(
    kind: FindingKind,
    target: AuditTarget,
    evidence: str,
    suggestion: str,
    candidates: tuple[Candidate, ...] = (),
) -> Finding:
    return Finding(
        kind=kind,
        section=target.entry.section,
        entry_name=target.entry.name,
        line_number=target.entry.line_number,
        url=target.url,
        evidence=evidence,
        suggestion=suggestion,
        candidates=candidates,
    )


def _last_result(observation: UrlObservation) -> str:
    details = []
    if observation.status is not None:
        details.append(f"status {observation.status}")
    if observation.error:
        details.append(f"error {observation.error}")
    return "; last " + "; ".join(details) if details else ""


def _link_finding(target: AuditTarget, observation: UrlObservation) -> Finding | None:
    if observation.outcome == Outcome.OK:
        return None
    if observation.outcome == Outcome.DEAD:
        return _finding(
            FindingKind.DEAD,
            target,
            f"Confirmed HTTP {observation.status} response.",
            "Manually verify, then remove or replace this link.",
        )
    if observation.outcome == Outcome.TRANSIENT:
        return _finding(
            FindingKind.TRANSIENT,
            target,
            f"Transient failure after {observation.attempts} attempts{_last_result(observation)}.",
            "Retry this link on the next audit run.",
        )
    if observation.outcome == Outcome.RESTRICTED:
        return _finding(
            FindingKind.RESTRICTED,
            target,
            f"Automated access was restricted by HTTP {observation.status}.",
            "Perform manual browser verification before changing the link.",
        )
    if observation.outcome == Outcome.HTTP_ERROR:
        return _finding(
            FindingKind.HTTP_ERROR,
            target,
            f"HTTP probe failed{_last_result(observation)}.",
            "Perform manual diagnosis before changing the link.",
        )
    if observation.outcome == Outcome.PERMANENT_REDIRECT:
        return _finding(
            FindingKind.PERMANENT_REDIRECT,
            target,
            f"The link permanently redirects to {observation.final_url}.",
            f"Update the link to {observation.final_url}.",
        )
    raise AssertionError(f"unhandled URL outcome: {observation.outcome}")


def _github_findings(target: AuditTarget, requested_name: str, repository: Any) -> list[Finding]:
    findings: list[Finding] = []
    full_name = repository.full_name
    canonical_url = f"https://github.com/{full_name}"
    if full_name.casefold() != requested_name.casefold():
        findings.append(
            _finding(
                FindingKind.GITHUB_MOVED,
                target,
                f"GitHub resolves {requested_name} as {full_name}.",
                f"Update the link to the canonical repository {canonical_url}.",
            )
        )

    if target.entry.section == HISTORICAL_SECTION:
        return findings
    if repository.archived:
        findings.append(
            _finding(
                FindingKind.GITHUB_ARCHIVED,
                target,
                "GitHub marks the repository as archived.",
                "Manually verify whether to replace it or move it to the historical section.",
            )
        )
    if repository.disabled:
        findings.append(
            _finding(
                FindingKind.GITHUB_DISABLED,
                target,
                "GitHub marks the repository as disabled.",
                "Manually verify whether the repository should be replaced or removed.",
            )
        )

    parent = repository.parent if repository.fork else None
    if (
        parent is not None
        and parent.full_name.casefold() != full_name.casefold()
        and not parent.archived
        and not parent.disabled
    ):
        parent_url = f"https://github.com/{parent.full_name}"
        findings.append(
            _finding(
                FindingKind.GITHUB_PARENT,
                target,
                f"This fork has the active parent repository {parent.full_name}.",
                f"Manually verify replacing the link with {parent_url}.",
            )
        )
    return findings


def _normalized_name(name: str) -> str:
    return "".join(character for character in name.casefold() if character.isalnum())


def _candidate_repositories(entry: ReadmeEntry, github_client: Any) -> tuple[Candidate, ...]:
    repositories = github_client.search_repositories(
        query=f"{entry.name} in:name",
        sort="stars",
        order="desc",
    )
    normalized_entry_name = _normalized_name(entry.name)
    matches = []
    for repository in islice(repositories, 20):
        if (
            _normalized_name(repository.name) == normalized_entry_name
            and not repository.archived
            and not repository.disabled
        ):
            matches.append(
                Candidate(
                    full_name=repository.full_name,
                    url=repository.html_url,
                    stars=repository.stargazers_count,
                )
            )

    matches.sort(
        key=lambda candidate: (
            -candidate.stars,
            candidate.full_name.casefold(),
            candidate.full_name,
            candidate.url,
        )
    )
    unique = []
    seen = set()
    for candidate in matches:
        key = candidate.full_name.casefold()
        if key not in seen:
            seen.add(key)
            unique.append(candidate)
    return tuple(unique[:3])


def audit_readme(
    readme_path: str | Path,
    github_client: Any,
    *,
    prober: Callable[[str], UrlObservation] = probe_url,
) -> list[Finding]:
    """Audit README URLs and GitHub metadata without modifying repository files."""
    targets = collect_targets(readme_path)
    unique_urls = list(dict.fromkeys(target.url for target in targets))
    with ThreadPoolExecutor(max_workers=8) as executor:
        observations = dict(zip(unique_urls, executor.map(prober, unique_urls)))

    findings = []
    repository_cache: dict[str, Any | None] = {}
    for target in targets:
        observation = observations[target.url]
        if link_finding := _link_finding(target, observation):
            findings.append(link_finding)

        requested_name = _parse_github_repository_url(target.url)
        if requested_name is not None:
            cache_key = requested_name.casefold()
            if cache_key not in repository_cache:
                try:
                    repository_cache[cache_key] = github_client.get_repo(requested_name)
                except GithubException as error:
                    if error.status != 404:
                        raise
                    repository_cache[cache_key] = None
            repository = repository_cache[cache_key]
            if repository is not None:
                findings.extend(_github_findings(target, requested_name, repository))

        if (
            observation.outcome == Outcome.DEAD
            and target.is_primary
            and requested_name is None
            and not target.entry.github_url
            and target.entry.section != HISTORICAL_SECTION
        ):
            candidates = _candidate_repositories(target.entry, github_client)
            if candidates:
                findings.append(
                    _finding(
                        FindingKind.CANDIDATES,
                        target,
                        f"The original primary URL returned confirmed HTTP {observation.status}.",
                        "Manual verification of these candidate repositories is required.",
                        candidates,
                    )
                )

    findings.sort(
        key=lambda finding: (
            FINDING_ORDER[finding.kind],
            finding.section,
            finding.entry_name,
            finding.line_number,
            finding.url,
        )
    )
    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit awesome-quant README links and repositories."
    )
    parser.add_argument("--readme", default="README.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required")
    repository_name = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if not repository_name:
        raise RuntimeError("GITHUB_REPOSITORY is required")

    github_client = Github(auth=Auth.Token(token))
    repository = github_client.get_repo(repository_name)
    findings = audit_readme(args.readme, github_client)
    body = render_report(findings, checked_at=datetime.now(timezone.utc))
    action = sync_tracking_issue(repository, findings, body)
    print(f"README audit: {len(findings)} finding(s); issue action: {action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
