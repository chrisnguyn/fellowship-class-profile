import json
import requests


from general.static import end_date, endpoints, start_date
from general.user import username, user_token


def update_commit_stats(pr_contribution_nodes, commit_stats):
    for pr_node in pr_contribution_nodes:
        pr = pr_node["pullRequest"]
        if pr["merged"]:
            repo_name = pr["repository"]["name"]
            if repo_name in commit_stats:
                commit_stats[repo_name]["commits"] += pr["commits"]["totalCount"]
                commit_stats[repo_name]["deletions"] += pr["deletions"]
                commit_stats[repo_name]["additions"] += pr["additions"]
                commit_stats[repo_name]["changed_files"] += pr["changedFiles"]
            else:
                commit_stats[repo_name] = {
                    "commits": pr["commits"]["totalCount"],
                    "deletions": pr["deletions"],
                    "additions": pr["additions"],
                    "changed_files": pr["changedFiles"]
                }


def get_commit_stats(user):
    cursor_str = ""
    commit_stats_per_repo = {}

    while True:
        query = f"""  query {{
            user(login:"{user}"){{
                contributionsCollection(from: "{start_date}", to:"{end_date}"){{
                    pullRequestContributions(first:20 {cursor_str}){{
                        pageInfo{{
                            hasNextPage
                            endCursor
                        }}
                        nodes{{
                            pullRequest {{
                                repository {{
                                    name
                                }}
                                merged
                                changedFiles
                                additions
                                deletions
                                commits(first:1){{
                                    totalCount
                                }}
                            }}
                        }}
                    }}   
                }}
            }}
        }}"""

        r = requests.post(
            endpoints["github"], headers={"Authorization": f"token {user_token}"}, json={"query": query})
        response = json.loads(r.text)
        update_commit_stats(response["data"]["user"]["contributionsCollection"]
                            ["pullRequestContributions"]["nodes"], commit_stats_per_repo)

        pageInfo = response["data"]["user"]["contributionsCollection"]["pullRequestContributions"]["pageInfo"]
        if not pageInfo["hasNextPage"]:
            break
        cursor = pageInfo["endCursor"]
        cursor_str = f", after: \"{cursor}\""
    return commit_stats_per_repo


# get commit stats for all PRs you opened (so anything you paired with someone else on won't be included)
commit_stats_per_repo = get_commit_stats(user=username)
print(commit_stats_per_repo)

#calculate total stats
num_additions = 0
num_deletions = 0
num_files_changes = 0
num_total_commits = 0
for repo_name, repo_val in commit_stats_per_repo.items():
    num_additions += repo_val["additions"]
    num_deletions += repo_val["deletions"]
    num_files_changes += repo_val["changed_files"]
    num_total_commits += repo_val["commits"]

print("Total additions: ", num_additions)
print("Total deletions: ", num_deletions)
print("Total files changed: ", num_files_changes)
print("Total commits in merged PRs: ", num_total_commits)