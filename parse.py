import json
import os
import re
from html.parser import HTMLParser
from threading import Thread
from urllib.request import urlopen

import pandas as pd
from github import Auth, Github

# using an access token
auth = Auth.Token(os.environ["GITHUB_ACCESS_TOKEN"])
g = Github(auth=auth)


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
        m = re.search(r"package=(\w+)", url) or re.search(
            r"/packages/(\w+)", url
        )
        if not m:
            return "", ""
        pkg = m.group(1)
        page_url = f"https://cran.r-project.org/web/packages/{pkg}/index.html"
        with urlopen(page_url, timeout=10) as resp:
            page_html = resp.read().decode("utf-8", errors="replace")

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
        print(f"CRAN ERROR {url}: {e}")
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
        with urlopen(api_url, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

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
        print(f"PYPI ERROR {url}: {e}")
        return ""


def slugify(text):
    """Convert text to lowercase hyphen-separated slug."""
    text = text.lower().strip()
    text = re.sub(r"[&/]+", "-", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


re_langs = re.compile(r'^((?:`[^`]+`\s*)+)-\s*(.*)$')


def extract_languages(description: str) -> tuple[list[str], str]:
    """Extract inline language tags from description.

    Returns (languages, clean_description).
    E.g. "`Python` `Rust` - High-performance..." -> (["Python", "Rust"], "High-performance...")
    """
    m = re_langs.match(description)
    if m:
        lang_str = m.group(1)
        clean_desc = m.group(2)
        langs = re.findall(r'`([^`]+)`', lang_str)
        return langs, clean_desc
    return [], description


def get_repo_info(repo):
    """Fetch last commit date and star count from GitHub."""
    try:
        if repo:
            r = g.get_repo(repo)
            cs = r.get_commits()
            last_commit = cs[0].commit.author.date.strftime("%Y-%m-%d")
            stars = r.stargazers_count
            return last_commit, stars
        else:
            return "", 0
    except Exception:
        print("ERROR " + repo)
        return "error", 0


class Project(Thread):
    def __init__(self, match, language, category, section_path):
        super().__init__()
        self._match = match
        self.regs = None
        self._language = language
        self._category = category
        self._section_path = section_path
        self.languages = []
        self.clean_description = ""

    def run(self):
        m = self._match
        primary_url = m.group(2)
        # Use clean_description if it was set by the parser, otherwise extract from match
        if self.clean_description:
            description = self.clean_description
        else:
            description = m.group(3)

        # Check if primary URL is GitHub
        is_github = "github.com" in primary_url

        # If not GitHub, check if there's a GitHub link in the description
        github_url = ""
        if not is_github:
            github_url = extract_github_url(description)
        else:
            github_url = primary_url

        is_cran = "cran.r-project.org" in primary_url
        is_pypi = "pypi.org" in primary_url or "pypi.python.org" in primary_url
        is_commercial = self._language == "Commercial & Proprietary Services"

        # For CRAN projects, scrape the CRAN page for GitHub URL and published date
        cran_date = ""
        if is_cran:
            cran_date, cran_github = get_cran_info(primary_url)
            if cran_github and not github_url:
                github_url = cran_github

        repo = extract_repo(github_url)
        print(repo or primary_url)
        last_commit, stars = get_repo_info(repo)

        # Fallback: use CRAN/PyPI dates when no GitHub data
        if not last_commit or last_commit == "error":
            if is_cran and cran_date:
                last_commit = cran_date
            elif is_pypi:
                pypi_date = get_pypi_last_updated(primary_url)
                if pypi_date:
                    last_commit = pypi_date

        # Build section slug from category or language
        section_slug = slugify(self._category or self._language)

        self.regs = dict(
            project=m.group(1),
            language=self._language,
            languages=",".join(self.languages),
            category=self._category,
            section=self._section_path,
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
        )


projects = []

with open("README.md", "r", encoding="utf8") as f:
    ret = re.compile(r"^(#+) (.*)$")
    rex = re.compile(r"^\s*- \[(.*)\]\((.*)\) - (.*)$")
    re_badge = re.compile(r"\s*!\[[^\]]*\]\([^)]*\)\s*")
    m_titles = []
    last_head_level = 0
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

while True:
    checks = [not p.is_alive() for p in projects]
    if all(checks):
        break

projects = [p.regs for p in projects]
df = pd.DataFrame(projects)
df.to_csv("site/projects.csv", index=False)
