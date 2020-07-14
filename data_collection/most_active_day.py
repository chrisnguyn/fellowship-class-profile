# Gets your most active day, gets your most active week.

from general.static import count, end_date, endpoints, start_date
from general.user import username, user_token
import json
import requests

most_active_day_week = f"""query {{
    user(login: "{username}") {{
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


def get_most_active_dates():
    response = requests.post(
        endpoints["github"],
        headers={"Authorization": f"Bearer {user_token}"},
        json={"query": most_active_day_week}
    )
    
    return json.loads(response.text)["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]


def calculate_max():
    weeks = get_most_active_dates()
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

    print(f'Your max day value was {max_day}. This was on {max_day_date}.')  # most number of commits pushed on one day, and what day
    print(f'Your max week value was {max_week}. This was week number {max_week_date}.')  # most number of commits made in a week, which week #


calculate_max()
