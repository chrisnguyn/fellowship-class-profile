import json
import requests

from general.static import end_date, endpoints, start_date
from general.user import username, user_token
from typing import Dict
from org_repo_stats import get_all_forked_repos_in_MLH


def get_repos_in_MLH_project_list(repositories):
    mlh_repo_names = [repo["name"] for repo in get_all_forked_repos_in_MLH()]
    mlh_project_repos = []
    for repo in repositories:
        if repo["repository"]["name"] in mlh_repo_names:
            mlh_project_repos.append(repo)
    return mlh_project_repos


def get_most_worked_on(user: str) -> Dict:
    num_repos = 5
    query = f"""
    query {{
      user(login:"{user}"){{
        contributionsCollection(from: "{start_date}", to:"{end_date}" ) {{
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
				primaryLanguage {{
					name
				}}
            }}
          }}
        }}
      }}
    }}"""
    r = requests.post(
        endpoints["github"], headers={"Authorization": f"token {user_token}"}, json={"query": query})

    print(json.loads(r.text))

    return json.loads(r.text)


response = get_most_worked_on(user="kbanc")
print(f"Top contributed to repos:",
      response["data"]["user"]["contributionsCollection"]["pullRequestContributionsByRepository"])

print("Top repos that were part of the MLH open source projects:", get_repos_in_MLH_project_list(
    response["data"]["user"]["contributionsCollection"]["pullRequestContributionsByRepository"]))

print("Total number of PRs during Fellowship (to any repo):",
      response["data"]["user"]["contributionsCollection"]["totalPullRequestContributions"])

print("Total number of repositories contributed to during the Fellowship:",
      response["data"]["user"]["contributionsCollection"]["totalRepositoriesWithContributedPullRequests"])

print("PR with the most discussion:",
      response["data"]["user"]["contributionsCollection"]["popularPullRequestContribution"])
