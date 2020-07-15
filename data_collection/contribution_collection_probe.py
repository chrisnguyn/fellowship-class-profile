from general.user import username, user_token
from general.static import end_date, endpoints, start_date
import json
import requests

query = f"""{{
        user(login: "{username}") {{
        contributionsCollection(from: "2020-06-01T19:30:46Z", to: "2020-08-24T19:30:46Z") {{
            totalCommitContributions
            totalIssueContributions
            totalPullRequestContributions
            totalPullRequestReviewContributions
            totalRepositoriesWithContributedCommits
            totalRepositoriesWithContributedIssues
            totalRepositoriesWithContributedPullRequestReviews
            totalRepositoriesWithContributedPullRequests
            totalRepositoryContributions
        }}
    }}
}}"""

response = requests.post(
    endpoints["github"],
    headers={"Authorization": f"token {user_token}"},
    json={"query": query}
)

data = json.dumps(response.json())
print(data)
