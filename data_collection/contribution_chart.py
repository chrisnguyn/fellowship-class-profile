from general.user import username, user_token
from general.static import endpoints
import json
import requests

def get_contribution_chart(user):
    chart_query = f"""query {{
        user(login: "{user}") {{
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
        json={"query": chart_query}
    )

    return json.dumps(response.json())


if __name__ == "__main__":
    get_contribution_chart(username)
    # print(get_contribution_chart(username))
