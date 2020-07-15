# Get ALL issues within time frame per user
# Need to make a token for authentication, can't use the GraphQL endpoint without it

from general.static import count, end_date, endpoints, start_date
from general.user import username, user_token
import json
import requests


# {'data': {'user': {'contributionsCollection': {'issueContributions': {'totalCount'
def get_issues(user):
    issues_query = f"""query {{
        user(login: "{user}") {{
            contributionsCollection(from: "{start_date}", to: "{end_date}") {{
                issueContributions(last: {count}) {{
                    totalCount
                }}
            }}
        }}
    }}"""
    response = requests.post(
        endpoints["github"],
        headers={"Authorization": f"Bearer {user_token}"}, 
        json={"query": issues_query}
    )
    data = json.loads(response.text)
    num_issues = data['data']['user']['contributionsCollection']['issueContributions']['totalCount']
    return num_issues


print(get_issues(username))