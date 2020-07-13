import os
import requests
import pandas as pd

token = os.environ['GITHUB_API_TOKEN']

page_num = 1
per_page = 30
repos = []

while True:
    url = f'https://api.github.com/orgs/MLH-Fellowship/repos?page={page_num}&per_page={per_page}'
    response = requests.get(url, headers={'Authorization': f'token {token}'}).json()
    repos += response
    if len(response) < per_page:
        break
    page_num += 1


print("Number of repos fellowship wide", len(repos))

repos_df = pd.DataFrame(repos)
num_forked_repos = len(repos_df.query('fork == True'))

#forked repos can be considered the projects we're contributing to
print("Number of forked repos", num_forked_repos) 
print("Number of orginal repos", len(repos)-num_forked_repos)

