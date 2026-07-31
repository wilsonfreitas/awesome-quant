import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from urllib.request import Request, urlopen

import pandas as pd
from github import Auth, Github

from scripts.readme_entries import (
    BADGE_RE,
    ENTRY_RE,
    HEADING_RE,
    extract_languages,
    slugify,
)

USER_AGENT = "awesome-quant-parser (+https://github.com/wilsonfreitas/awesome-quant)"
REQUEST_TIMEOUT = 10
# MAX_WORKERS bounds concurrency and doubles as a modest rate limit: at most
# 8 lookups are in flight at any time (against GitHub, CRAN, and PyPI).
MAX_WORKERS = 8
# Entries whose last commit is older than this are flagged as stale in the CSV.
STALE_AFTER = timedelta(days=730)  # 24 months

_github_client = None


def get_github_client():
    """Create the GitHub client lazily so importing this module is token-free."""
    global _github_client
    if _github_client is None:
        auth = Auth.Token(os.environ["GITHUB_ACCESS_TOKEN"])
        _github_client = Github(auth=auth)
    return _github_client


def _fetch_url(url):
    """urlopen with a User-Agent header and timeout; returns decoded body."""
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=REQUEST_TIMEOUT) as resp:
        return resp.read().decode("utf-8", errors="replace")


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

    Returns (published_date, github_url) — either may be empty string.
    """
    try:
        # [\w.] so dotted package names like data.table resolve correctly.
        m = re.search(r"package=([\w.]+)", url) or re.search(
            r"/packages/([\w.]+)", url
        )
        if not m:
            return "", ""
        pkg = m.group(1)
        page_url = f"https://cran.r-project.org/web/packages/{pkg}/index.html"
        page_html = _fetch_url(page_url)

        class CranParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self._in_td = False
                self._found_published = False
                self._in_github_span = False
                self.date = ""
                self.github_url = ""

            def handle_starttag(self, tag, attrs):
                if tag == "td":
                    self._in_td = True
                # GitHub links are wrapped in <span class="GitHub">
                if tag == "span":
                    classes = dict(attrs).get("class", "")
                    if "GitHub" in classes:
                        self._in_github_span = True
                # Also check <a href> for github.com links
                if tag == "a" and not self.github_url:
                    href = dict(attrs).get("href", "")
                    if "github.com" in href and "/issues" not in href:
                        self.github_url = href

            def handle_endtag(self, tag):
                if tag == "td":
                    self._in_td = False
                if tag == "span":
                    self._in_github_span = False

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
        # Clean trailing slashes or .git from GitHub URL
        gh = parser.github_url.rstrip("/")
        if gh.endswith(".git"):
            gh = gh[:-4]
        return parser.date, gh
    except Exception as e:
        print(f"CRAN ERROR {url}: {e}", file=sys.stderr)
        return "", ""


def get_pypi_last_updated(url):
    """Fetch the last release date from PyPI JSON API."""
    try:
        # Extract package name from URL like https://pypi.org/project/tushare/
        m = re.search(r"pypi\.org/project/([\w.-]+)", url) or re.search(
            r"pypi\.python\.org/pypi/([\w.-]+)", url
        )
        if not m:
            return ""
        pkg = m.group(1).rstrip("/")
        api_url = f"https://pypi.org/pypi/{pkg}/json"
        data = json.loads(_fetch_url(api_url))

        releases = data.get("releases", {})
        if not releases:
            return ""

        # Find the latest release with an upload time
        for version in sorted(releases.keys(), reverse=True):
            release_data = releases[version]
            if release_data:
                upload_time = release_data[0].get("upload_time_iso_8601")
                if upload_time:
                    return upload_time.split("T")[0]
        return ""
    except Exception as e:
        print(f"PYPI ERROR {url}: {e}", file=sys.stderr)
        return ""


def get_repo_info(repo):
    """Fetch last commit date and star count from GitHub.

    Returns (last_commit, stars). last_commit is None when the lookup failed
    (as opposed to "", which means there was no repo to look up).
    """
    if not repo:
        return "", 0
    try:
        r = get_github_client().get_repo(repo)
        cs = r.get_commits()
        last_commit = cs[0].commit.author.date.strftime("%Y-%m-%d")
        stars = r.stargazers_count
        return last_commit, stars
    except Exception as e:
        print(f"ERROR {repo}: {e!r}", file=sys.stderr)
        return None, 0


def is_stale(last_commit, now=None):
    """True when last_commit (YYYY-MM-DD) is older than STALE_AFTER."""
    if not last_commit:
        return False
    try:
        commit_date = datetime.strptime(last_commit, "%Y-%m-%d").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        return False
    now = now or datetime.now(timezone.utc)
    return now - commit_date > STALE_AFTER


def fetch_project(match, language, languages, clean_description, category):
    """Enrich one README entry with GitHub/CRAN/PyPI metadata.

    Returns (record, attempted, failed): record is the CSV row dict,
    attempted is True when a metadata lookup was possible for the entry,
    failed is True when a lookup was attempted but no date was obtained.
    """
    m = match
    primary_url = m.group(2)
    description = clean_description if clean_description else m.group(3)

    # Check if primary URL is GitHub
    is_github = "github.com" in primary_url

    # If not GitHub, check if there's a GitHub link in the description
    if is_github:
        github_url = primary_url
    else:
        github_url = extract_github_url(description)

    is_cran = "cran.r-project.org" in primary_url
    is_pypi = "pypi.org" in primary_url or "pypi.python.org" in primary_url
    is_commercial = category == "Commercial & Proprietary Services"

    # For CRAN projects, scrape the CRAN page for GitHub URL and published date
    cran_date = ""
    if is_cran:
        cran_date, cran_github = get_cran_info(primary_url)
        if cran_github and not github_url:
            github_url = cran_github

    repo = extract_repo(github_url)
    print(repo or primary_url)
    last_commit, stars = get_repo_info(repo)
    if last_commit is None:
        # Lookup failed: emit an empty value rather than a fake date.
        last_commit = ""

    # Fallback: use CRAN/PyPI dates when no GitHub data
    if not last_commit:
        if is_cran and cran_date:
            last_commit = cran_date
        elif is_pypi:
            pypi_date = get_pypi_last_updated(primary_url)
            if pypi_date:
                last_commit = pypi_date

    attempted = bool(repo) or is_cran or is_pypi
    failed = attempted and not last_commit

    # Build section slug from category or language
    section_slug = slugify(category or language)

    record = dict(
        project=m.group(1),
        language=language,
        languages=",".join(languages),
        category=category,
        section=category,
        section_slug=section_slug,
        last_commit=last_commit,
        stars=stars,
        url=primary_url,
        description=description,
        github=is_github or bool(github_url),
        cran=is_cran,
        pypi=is_pypi,
        commercial=is_commercial,
        repo=repo,
        stale=is_stale(last_commit),
    )
    return record, attempted, failed


def main():
    tasks = []

    with open("README.md", "r", encoding="utf8") as f:
        current_category = ""
        for line in f:
            line = BADGE_RE.sub(" ", line)
            m = ENTRY_RE.match(line)
            if m:
                raw_desc = m.group(3).strip()

                # Extract language tags from description
                languages, clean_description = extract_languages(raw_desc)
                primary_language = languages[0] if languages else ""

                tasks.append(
                    (m, primary_language, languages, clean_description, current_category)
                )
            else:
                m = HEADING_RE.match(line)
                if m:
                    hrs = m.group(1)
                    title = m.group(2).strip()
                    if len(hrs) == 2 and title != "Contents":
                        current_category = title

    # Bounded thread pool instead of one unbounded thread per entry. Futures
    # are collected in submission order so the CSV keeps the README order.
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(fetch_project, *task) for task in tasks]
        results = [future.result() for future in futures]

    records = [record for record, _, _ in results]
    attempted = sum(1 for _, was_attempted, _ in results if was_attempted)
    failures = sum(1 for _, _, failed in results if failed)

    df = pd.DataFrame(records)
    df.to_csv("site/projects.csv", index=False)

    total = len(records)
    print(f"{failures}/{attempted} lookups failed ({total} entries)")
    if total and failures > 0.10 * total:
        print(
            f"ERROR: more than 10% of entries failed metadata lookup "
            f"({failures}/{total})",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
