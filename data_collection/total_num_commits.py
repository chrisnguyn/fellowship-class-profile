from data_collection.general.user import username, user_token
from data_collection.general.static import endpoints
import json
import requests

query = f"""query {{
    user(login:"{username}") {{
        contributionsCollection(from: "2020-06-01T00:00:00Z", to: "2020-08-24T23:59:59Z") {{
            contributionCalendar {{
                totalContributions
            }}
        }}
    }}
}}"""

response = requests.post(
    endpoints["github"],
    headers={"Authorization": f"token {user_token}"},
    json={"query": query}
)

data = json.loads(response.text)
print(json.dumps({'Total contributions': data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]}))
