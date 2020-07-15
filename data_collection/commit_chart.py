from general.user import username, user_token
from general.static import end_date, endpoints, start_date
import json
import requests

query = f"""query {{
  user(login: "chrisngyn") {{
    contributionsCollection(from: "2020-06-01T00:00:00Z", to: "2020-08-24T19:30:46Z") {{
      contributionCalendar {{
        totalContributions
        weeks {{
          contributionDays {{
            contributionCount
            date
            weekday
          }}
        }}
      }}
    }}
  }}
}}"""

response = requests.post(
    endpoints["github"],
    headers={"Authorization": f"token {user_token}"},
    json={"query": query}
)

print(json.dumps(response.json()))
