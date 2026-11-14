import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
from html.parser import HTMLParser
from threading import Thread
from urllib.request import urlopen

from github import Auth, Github
from scripts import pypi_metadata
from scripts.metadata import FIELDS, checked_at_value, date_value, stars_value

from scripts.readme_entries import (
    BADGE_RE,
    ENTRY_RE,
    HEADING_RE,
    extract_languages,
    slugify,
)

_github_client = None


def get_github_client():
    """Create the GitHub client lazily so importing this module is token-free."""
    global _github_client
    if _github_client is None:
        auth = Auth.Token(os.environ["GITHUB_ACCESS_TOKEN"])
        _github_client = Github(auth=auth, timeout=10, retry=0)
    return _github_client


def extract_repo(url):
    reu = re.compile(r"^https://github.com/([\w-]+/[-\w\.]+)$")
    m = reu.match(url)
    if m:
        return m.group(1)
    else:
        return ""


def extract_github_url(description):
    """Extract GitHub URL from description if present."""
    github_pattern = re.compile(r"\[GitHub\]\((https://github\.com/[\w-]+/[-\w\.]+)\)")
    m = github_pattern.search(description)
    if m:
        return m.group(1)
    return ""


def get_cran_info(url):
    """Fetch Published date and GitHub URL from a CRAN package page.

    Return (published_date, github_url) for a package page, or None on failure.
    A successful page without a repository link is an observed removal.
    """
    try:
        m = re.search(r"package=([\w.]+)", url) or re.search(
            r"/packages/([\w.]+)", url
        )
        if not m:
            return None
        pkg = m.group(1)
        page_url = f"https://cran.r-project.org/web/packages/{pkg}/index.html"
        with urlopen(page_url, timeout=10) as resp:
            page_html = resp.read().decode("utf-8", errors="replace")

        class CranParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self._in_td = False
                self._found_published = False
                self.date = ""
                self.github_url = ""

            def handle_starttag(self, tag, attrs):
                if tag == "td":
                    self._in_td = True
                # Also check <a href> for github.com links
                if tag == "a" and not self.github_url:
                    href = dict(attrs).get("href", "")
                    if "github.com" in href and "/issues" not in href:
                        self.github_url = href

            def handle_endtag(self, tag):
                if tag == "td":
                    self._in_td = False

            def handle_data(self, data):
                if self._in_td:
                    if data.strip() == "Published:":
                        self._found_published = True
                    elif self._found_published and not self.date:
                        d = data.strip()
                        if re.match(r"\d{4}-\d{2}-\d{2}", d):
                            self.date = d

        parser = CranParser()
        parser.feed(page_html)
        if not parser._found_published:
            return None
        # Clean trailing slashes or .git from GitHub URL
        gh = parser.github_url.rstrip("/")
        if gh.endswith(".git"):
            gh = gh[:-4]
        return date_value(parser.date), gh
    except Exception as e:
        print(f"CRAN ERROR {url}: {e}")
        return None


def get_pypi_last_updated(url):
    """Adapt a supported package URL to the shared latest-upload lookup."""
    match = re.search(r"pypi\.org/project/([\w.-]+)", url) or re.search(
        r"pypi\.python\.org/pypi/([\w.-]+)", url
    )
    try:
        return (pypi_metadata.get_pypi_last_updated(match.group(1)) or "") if match else ""
    except (OSError, ValueError) as exc:
        print(f"PyPI ERROR {url}: {type(exc).__name__}")
        return ""


def get_repo_info(repo):
    """Observe stars and the default branch head's committer date independently."""
    if not repo:
        return "", None
    try:
        r = get_github_client().get_repo(repo)
    except Exception:
        print("ERROR " + repo)
        return "", None
    stars, last_commit = None, ""
    try:
        stars = stars_value(r.stargazers_count)
    except Exception:
        print("STARS ERROR " + repo)
    try:
        cs = r.get_commits(sha=r.default_branch)
        last_commit = date_value(cs[0].commit.committer.date)
    except Exception:
        print("COMMIT ERROR " + repo)
    return last_commit, stars


class Project(Thread):
    def __init__(self, match, language, category, section_path, *, prior=None, checked_at=None):
        super().__init__()
        self._match = match
        self.regs = None
        self._language = language
        self._category = category
        self._section_path = section_path
        self.languages = []
        self.clean_description = ""
        self._prior = prior or {}
        self._checked_at = checked_at or datetime.now(timezone.utc).isoformat(timespec="seconds")

    def run(self):
        m = self._match
        primary_url = m.group(2)
        # Use clean_description if it was set by the parser, otherwise extract from match
        if self.clean_description:
            description = self.clean_description
        else:
            description = m.group(3)

        # Check if primary URL is GitHub
        is_github = bool(extract_repo(primary_url))

        # If not GitHub, check if there's a GitHub link in the description
        github_url = ""
        if not is_github:
            github_url = extract_github_url(description)
        else:
            github_url = primary_url

        is_cran = "cran.r-project.org" in primary_url
        is_pypi = "pypi.org" in primary_url or "pypi.python.org" in primary_url
        is_commercial = self._category == "Commercial & Proprietary Services"
        declared_repo = extract_repo(github_url)
        entry_identity = [m.group(1), primary_url, declared_repo]
        prior = self._prior
        try:
            prior_identity = json.loads(prior.get("metadata_identity", ""))
        except (ValueError, TypeError):
            prior_identity = []
        if not isinstance(prior_identity, list) or len(prior_identity) != 4 or prior_identity[:3] != entry_identity:
            prior = {}

        # For CRAN projects, scrape the CRAN page for GitHub URL and published date
        cran_date = ""
        if is_cran:
            cran_info = get_cran_info(primary_url)
            if cran_info is not None:
                cran_date, cran_github = cran_info
                if not github_url:
                    github_url = cran_github
            elif not github_url and prior:
                # A failed discovery must not discard the previously discovered repository.
                github_url = "https://github.com/" + prior.get("repo", "")

        repo = extract_repo(github_url)
        identity = json.dumps(entry_identity + [repo], separators=(",", ":"))
        if prior and prior_identity != entry_identity + [repo]:
            prior = {}
        print(repo or primary_url)
        last_commit, stars = get_repo_info(repo)

        observations = {
            "last_commit": date_value(last_commit),
            "stars": stars_value(stars),
            "cran_published": date_value(cran_date),
            "pypi_upload": date_value(get_pypi_last_updated(primary_url)) if is_pypi else "",
        }

        # Build section slug from category or language
        section_slug = slugify(self._category or self._language)

        self.regs = dict(
            project=m.group(1),
            language=self._language,
            languages=",".join(self.languages),
            category=self._category,
            section=self._section_path,
            section_slug=section_slug,
            url=primary_url,
            description=description,
            github=bool(repo),
            cran=is_cran,
            pypi=is_pypi,
            commercial=is_commercial,
            repo=repo,
            metadata_identity=identity,
            metadata_attempted_at=self._checked_at,
        )
        for field, (source, _) in FIELDS.items():
            value = observations[field]
            observed = value is not None if field == "stars" else bool(value)
            checked_at, status = (self._checked_at, "fresh") if observed else ("", "unknown")
            if not observed and prior.get(field + "_source") == source:
                previous = stars_value(prior.get(field)) if field == "stars" else date_value(prior.get(field))
                previous_check = checked_at_value(prior.get(field + "_checked_at"))
                if previous_check and (previous is not None if field == "stars" else bool(previous)):
                    value, checked_at, status = previous, previous_check, "stale"
            self.regs.update({field: value, field + "_source": source if checked_at else "",
                              field + "_checked_at": checked_at, field + "_status": status})


def main(readme_path="README.md", csv_path="site/projects.csv"):
    projects = []
    prior = {}
    try:
        with open(csv_path, encoding="utf-8", newline="") as handle:
            prior = {(row.get("project"), row.get("url")): row for row in csv.DictReader(handle)}
    except (OSError, ValueError, csv.Error) as exc:
        print(f"Prior metadata unavailable: {type(exc).__name__}")

    with open(readme_path, "r", encoding="utf8") as f:
        ret = HEADING_RE
        rex = ENTRY_RE
        re_badge = BADGE_RE
        current_category = ""
        for line in f:
            line = re_badge.sub(" ", line)
            m = rex.match(line)
            if m:
                raw_desc = m.group(3).strip()

                # Extract language tags from description
                languages, clean_description = extract_languages(raw_desc)
                primary_language = languages[0] if languages else ""

                p = Project(
                    m,
                    primary_language,
                    current_category,
                    current_category,
                    prior=prior.get((m.group(1), m.group(2))),
                )
                p.languages = languages
                p.clean_description = clean_description
                p.start()
                projects.append(p)
            else:
                m = ret.match(line)
                if m:
                    hrs = m.group(1)
                    title = m.group(2).strip()
                    if len(hrs) == 2 and title != "Contents":
                        current_category = title

    for p in projects:
        p.join()

    projects = [p.regs for p in projects]
    # Replace atomically so an interrupted build cannot truncate its last good cache.
    destination = Path(csv_path)
    temporary = destination.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(projects[0]) if projects else ["project", "url"])
        writer.writeheader()
        writer.writerows(projects)
    temporary.replace(destination)


if __name__ == "__main__":
    main()
