
import os
from github import Github

# using an access token
g = Github(os.environ['GITHUB_ACCESS_TOKEN'])

u = g.get_user('kernc')
print(u)
r = u.get_repo('backtesting.py')
print(r)
print(r.html_url)
print(r.archived)
print(r.description)
print(r.updated_at)
r.language

# https://github.com/kernc/backtesting.py
# for ix, repo in enumerate(g.get_user().get_repos()):
#     print(ix+1, repo.name)
    # repo.edit(has_wiki=False)
    # to see all the available attributes and methods
    # print(dir(repo))
