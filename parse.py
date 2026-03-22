import os
import re
import pandas as pd
from threading import Thread

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
    # Look for [GitHub](https://github.com/...) pattern
    github_pattern = re.compile(r"\[GitHub\]\((https://github\.com/[\w-]+/[-\w\.]+)\)")
    m = github_pattern.search(description)
    if m:
        return m.group(1)
    return ""


def get_last_commit(repo):
    try:
        if repo:
            r = g.get_repo(repo)
            cs = r.get_commits()
            return cs[0].commit.author.date.strftime("%Y-%m-%d")
        else:
            return ""
    except:
        print("ERROR " + repo)
        return "error"


class Project(Thread):
    def __init__(self, match, section):
        super().__init__()
        self._match = match
        self.regs = None
        self._section = section

    def run(self):
        m = self._match
        primary_url = m.group(2)
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
        repo = extract_repo(github_url)
        print(repo)
        last_commit = get_last_commit(repo)
        self.regs = dict(
            project=m.group(1),
            section=self._section,
            last_commit=last_commit,
            url=primary_url,
            description=description,
            github=is_github or bool(github_url),
            cran=is_cran,
            repo=repo,
        )


projects = []

with open("README.md", "r", encoding="utf8") as f:
    ret = re.compile(r"^(#+) (.*)$")
    rex = re.compile(r"^\s*- \[(.*)\]\((.*)\) - (.*)$")
    m_titles = []
    last_head_level = 0
    for line in f:
        m = rex.match(line)
        if m:
            p = Project(m, " > ".join(m_titles[1:]))
            p.start()
            projects.append(p)
        else:
            m = ret.match(line)
            if m:
                hrs = m.group(1)
                if len(hrs) > last_head_level:
                    m_titles.append(m.group(2))
                else:
                    for n in range(last_head_level - len(hrs) + 1):
                        m_titles.pop()
                    m_titles.append(m.group(2))
                last_head_level = len(hrs)

while True:
    checks = [not p.is_alive() for p in projects]
    if all(checks):
        break

projects = [p.regs for p in projects]
df = pd.DataFrame(projects)
df.to_csv("site/projects.csv", index=False)
# df.to_markdown('projects.md', index=False)
