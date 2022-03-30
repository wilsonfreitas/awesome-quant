
import os
from github import Github

# using an access token
g = Github(os.environ['GITHUB_ACCESS_TOKEN'])

# ts = g.search_topics('trading')

# for t in ts:
#     print(t)

# t = ts[0]
# print(t)
# print(t.name)
# print(t.updated_at)
# print(t.score)

topic = 'quant'
repos = g.search_repositories(query=f'topic:{topic}')
for repo in repos:
    if repo.stargazers_count < 1000:
        break
    print(repo.name, repo.stargazers_count, repo.language, repo.html_url,
          repo.description, repo.updated_at, repo.archived)
