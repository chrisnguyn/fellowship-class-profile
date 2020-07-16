from data_collection.general.user import username, user_token
from data_collection.general.static import endpoints, start_date, end_date
import json
import requests


def get_contribution_chart(user):
    chart_query = f"""query {{
        user(login: "{user}") {{
            contributionsCollection(from: "{start_date}", to: "{end_date}") {{
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

    data = json.loads(response.text)
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


if __name__ == "__main__":
    # get_contribution_chart(username)
    print(get_contribution_chart(username))
