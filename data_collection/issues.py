# Get ALL issues within time frame per user
# Need to make a token for authentication, can't use the GraphQL endpoint without it

from general.static import count, end_date, endpoints, start_date
from general.user import username, user_token
import json
import requests

issues_query = f"""query {{
    user(login: "{username}") {{
        contributionsCollection(from: "{start_date}", to: "{end_date}") {{
            issueContributions(last: {count}) {{
                edges {{
                    node {{
                        issue {{
                            bodyText
                            bodyHTML
                            id
                        }}
                    }}
                }}
            }}
        }}
    }}
}}"""

# {'data': {'user': {'contributionsCollection': {'issueContributions': {'edges'
def get_issues():
    response = requests.post(
        endpoints["github"],
        headers={"Authorization": f"Bearer {user_token}"}, 
        json={"query": issues_query}
    )
    data = json.loads(response.text)
    issues = data['data']['user']['contributionsCollection']['issueContributions']['edges']
    return issues


print(get_issues())