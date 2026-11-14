
"""Manual GitHub quant-topic discovery; importing this module performs no search."""

import os
import sys
from github import Auth, Github


def main() -> int:
    token = os.environ.get('GITHUB_ACCESS_TOKEN')
    if not token:
        print('GITHUB_ACCESS_TOKEN is required', file=sys.stderr)
        return 1
    with Github(auth=Auth.Token(token)) as client:
        repos = client.search_repositories(query='topic:quant')
        for repo in repos:
            if repo.stargazers_count < 1000:
                break
            print(repo.name, repo.stargazers_count, repo.language, repo.html_url,
                  repo.description, repo.updated_at, repo.archived)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
