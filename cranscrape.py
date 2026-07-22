"""Standalone utility: scrape CRAN pages for GitHub repos of README entries.

Iterates the CRAN entries listed in README.md (via scripts.readme_entries),
fetches each package's CRAN index page, and records the first GitHub repo
link found on the page. Writes the results to cran.csv with the columns
``cran,github,repo``.

Note: this script is a standalone maintenance utility; cran.csv is NOT
consumed by the site build (parse.py / site/generate.py).
"""

import re
import sys

import pandas as pd
import requests

from scripts.readme_entries import iter_readme_entries

USER_AGENT = "awesome-quant-cranscrape (+https://github.com/wilsonfreitas/awesome-quant)"
REQUEST_TIMEOUT = 10

reu = re.compile(r"https://github.com/([\w-]+/[\w.-]+)")
# [\w.] so dotted package names like data.table resolve correctly.
re_pkg = re.compile(r"package=([\w.]+)")
re_pkg_path = re.compile(r"/packages/([\w.]+)")


def cran_index_url(url):
    """Resolve a README CRAN URL to the package's index page URL."""
    m = re_pkg.search(url) or re_pkg_path.search(url)
    if not m:
        return ""
    return f"https://cran.r-project.org/web/packages/{m.group(1)}/index.html"


def get_data(url):
    """Fetch a CRAN index page and extract the first GitHub repo link."""
    try:
        res = requests.get(
            url, timeout=REQUEST_TIMEOUT, headers={"User-Agent": USER_AGENT}
        )
        res.raise_for_status()
    except requests.RequestException as exc:
        print(f"ERROR {url}: {exc}", file=sys.stderr)
        return dict(cran=url, github="", repo="")
    m = reu.search(res.text)
    if m:
        return dict(cran=url, github=m.group(0), repo=m.group(1))
    return dict(cran=url, github="", repo="")


def main():
    all_data = []
    for entry in iter_readme_entries("README.md"):
        if "cran.r-project.org" not in entry.url:
            continue
        index_url = cran_index_url(entry.url)
        if not index_url:
            print(f"SKIP unrecognized CRAN URL: {entry.url}", file=sys.stderr)
            continue
        print(index_url)
        all_data.append(get_data(index_url))

    df = pd.DataFrame(all_data)
    df.to_csv("cran.csv", index=False)
    print(f"Wrote {len(all_data)} rows to cran.csv")


if __name__ == "__main__":
    main()
