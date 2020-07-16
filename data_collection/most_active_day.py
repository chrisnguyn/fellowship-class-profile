# Gets your most active day, gets your most active week.

from data_collection.general.static import end_date, endpoints, start_date
from data_collection.general.user import username, user_token

import json
import requests


def get_most_active_dates(user):
    most_active_day_week = f"""query {{
        user(login: "{user}") {{
            name
            contributionsCollection(from: "{start_date}", to: "{end_date}") {{
                contributionCalendar {{
                    totalContributions
                    weeks {{
                        contributionDays {{
                            contributionCount
                            date
                        }}
                    }}
                }}
            }}
        }}
    }}"""
    response = requests.post(
        endpoints["github"],
        headers={"Authorization": f"Bearer {user_token}"},
        json={"query": most_active_day_week}
    )

    return json.loads(response.text)["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]


def calculate_max(user):
    weeks = get_most_active_dates(user)
    max_day = 0
    max_day_date = ''
    max_week = 0
    max_week_date = 0
    counter = 0

    for week in weeks:
        current_week = 0
        for day in week["contributionDays"]:
            current_day = day["contributionCount"]

            if current_day > max_day:
                max_day = current_day
                max_day_date = day["date"]

            current_week += current_day

        if current_week > max_week:
            max_week = current_week
            max_week_date = counter

        counter += 1
    
    return {"max_day": {
                "date": max_day_date,
                "contributions": max_day
                },
            "max_week": {
                "week_number": max_week_date,
                "contributions": max_week
                }
            }

if __name__ == "__main__":
    max_stats = calculate_max(user=username)
    # most number of commits pushed on one day, and what day
    print(f'Your max day value was {max_stats["max_day"]["contributions"]}. This was on {max_stats["max_day"]["date"]}.')
    # most number of commits made in a week, which week #
    print(
        f'Your max week value was {max_stats["max_week"]["contributions"]}. This was week number {max_stats["max_week"]["week_number"]}.')

