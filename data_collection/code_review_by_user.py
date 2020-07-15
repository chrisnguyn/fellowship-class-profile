# Get ALL code reviews within time frame per user
# Need to make a token for authentication, can't use the GraphQL endpoint without it

from general.static import count, end_date, endpoints, start_date
from general.user import username, user_token
import json
import requests


# 'data': {'user': {'contributionsCollection': {'user': {'issueComments': {'edges'
def get_issue_comments(user):
    # Issue comments.
    issue_comment_query = f"""query {{
        user(login: "{user}") {{
            contributionsCollection(from: "{start_date}", to: "{end_date}") {{
                user {{
                    issueComments(last: {count}) {{
                        edges {{
                            node {{
                                id
                                bodyHTML
                                bodyText
                                url
                            }}
                        }}
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
    issue_comments = data['data']['user']['contributionsCollection']['user']['issueComments']['edges']
    return issue_comments


# 'data': {'user': {'contributionsCollection': {'pullRequestReviewContributions': {'edges'
def get_pr_reviews(user):
    # Pull request reviews.
    pr_review_query = f"""query {{
        user(login: "{user}") {{
            contributionsCollection(from: "{start_date}", to: "{end_date}") {{
                pullRequestReviewContributions(last: {count}) {{
                    edges {{
                        node {{
                            pullRequestReview {{
                                id
                                bodyHTML
                                bodyText
                                url
                                comments(last: {count}) {{
                                    edges {{
                                        node {{
                                            id
                                            bodyHTML
                                            bodyText
                                            url
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
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
    pr_reviews = data['data']['user']['contributionsCollection']['pullRequestReviewContributions']['edges']
    return pr_reviews


print(get_issue_comments(user=username))
print('')
print(get_pr_reviews(user=username))