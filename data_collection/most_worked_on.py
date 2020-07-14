import json
import os
import requests

from org_repo_stats import get_all_forked_repos_in_MLH

token = os.environ["GITHUB_API_TOKEN"]
user = "kbanc"

num_repos = 5
num_lang = 2


def get_repos_in_MLH_project_list(repositories):
    mlh_repo_names = [repo["name"] for repo in get_all_forked_repos_in_MLH()]
    mlh_project_repos = []
    for repo in repositories:
        if repo["repository"]["name"] in mlh_repo_names:
            mlh_project_repos.append(repo)
    return mlh_project_repos


query = f"""
  query {{
    user(login:"{user}"){{
      contributionsCollection(from: "2020-06-01T07:00:00Z", to:"2020-08-24T07:00:00Z" ) {{
        totalRepositoriesWithContributedPullRequests
        totalPullRequestContributions
        totalCommitContributions
        totalIssueContributions
        popularPullRequestContribution {{
          pullRequest {{
            title
            url
            merged
            repository{{
              name
              id
              languages(first:1){{
                nodes {{
                  name
                }}
              }}
            }}
          }}
        }}
        pullRequestContributionsByRepository(maxRepositories: {num_repos}){{
          repository {{
            name
            languages(first: {num_lang}){{
              nodes{{
                name
              }}
            }}
          }}
        }}
      }}
    }}
  }}"""

url = "https://api.github.com/graphql"
r = requests.post(
    url, headers={"Authorization": f"token {token}"}, json={"query": query})

response = json.loads(r.text)
print(f"Top {num_repos} contributed to repo:",
      response["data"]["user"]["contributionsCollection"]["pullRequestContributionsByRepository"])

print("Top repos that were part of the MLH open source projects:", get_repos_in_MLH_project_list(
    response["data"]["user"]["contributionsCollection"]["pullRequestContributionsByRepository"]))

print("Total number of PRs during Fellowship (to any repo):",
      response["data"]["user"]["contributionsCollection"]["totalPullRequestContributions"])

print("Total number of repositories contributed to during the Fellowship:",
      response["data"]["user"]["contributionsCollection"]["totalRepositoriesWithContributedPullRequests"])

print("PR with the most discussion:",
      response["data"]["user"]["contributionsCollection"]["popularPullRequestContribution"])
