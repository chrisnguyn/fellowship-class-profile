# Get ALL code reviews within time frame per user
# Need to make a token for authentication, can't use the GraphQL endpoint without it

from data_collection.general.static import count, end_date, endpoints, start_date
from data_collection.general.user import username, user_token
import json
import requests


# 'data': {'user': {'contributionsCollection': {'user': {'issueComments': {'edges'
def get_num_issue_comments(user):
    # Issue comments.
    issue_comment_query = f"""query {{
        user(login: "{user}") {{
            contributionsCollection(from: "{start_date}", to: "{end_date}") {{
                user {{
                    issueComments(last: {count}) {{
                        totalCount
                    }}
                }}
            }}
        }}
    }}"""

    response = requests.post(
        endpoints["github"], 
        headers={"Authorization": f"Bearer {user_token}"}, 
        json={"query": issue_comment_query}
    )
    data = json.loads(response.text)
    num_issue_comments = data['data']['user']['contributionsCollection']['user']['issueComments']['totalCount']
    return num_issue_comments


# 'data': {'user': {'contributionsCollection': {'pullRequestReviewContributions': {'edges'
def get_num_pr_reviews(user):
    # Pull request reviews.
    pr_review_query = f"""query {{
        user(login: "{user}") {{
            contributionsCollection(from: "{start_date}", to: "{end_date}") {{
                pullRequestReviewContributions(last: {count}) {{
                    totalCount
                }}
            }}
        }}
    }}"""
    response = requests.post(
        endpoints["github"], 
        headers={"Authorization": f"Bearer {user_token}"}, 
        json={"query": pr_review_query}
    )
    data = json.loads(response.text)
    pr_reviews = data['data']['user']['contributionsCollection']['pullRequestReviewContributions']['totalCount']
    return pr_reviews

if __name__ == "__main__":
    print(get_num_issue_comments(user=username))
    print('')
    print(get_num_pr_reviews(user=username))