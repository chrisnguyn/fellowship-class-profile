# Gets your most active day, gets your most active week.

import requests
import json

query = """query {
    viewer {
        name
        contributionsCollection(from: "2020-06-01T00:00:00Z", to: "2020-08-24T23:59:59Z") {
            contributionCalendar {
                totalContributions
                weeks {
                    contributionDays {
                        contributionCount
                        date
                    }
                }
            }
        }
    }
}"""

url = "https://api.github.com/graphql"
r = requests.post(url, headers={"Authorization": "Bearer TOKEN"}, json={"query": query})
data = json.loads(r.text)

weeks = data["data"]["viewer"]["contributionsCollection"]["contributionCalendar"]["weeks"]

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
