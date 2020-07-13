# This is an example of how you would get number of commits (default is one year)
# Found on Stack Overflow (in JavaScript) - https://stackoverflow.com/questions/18262288/finding-total-contributions-of-a-user-from-github-api

import requests
import json

query = """query { 
    viewer { 
        name
        contributionsCollection {
            contributionCalendar {
                totalContributions
                    weeks {
                        contributionDays {
                            contributionCount
                            date
                            weekday
                        }
                    firstDay
                }
            }
        }
    }
}"""

url = "https://api.github.com/graphql"
r = requests.post(url, headers={"Authorization": "Bearer TOKEN"}, json={"query": query})
print(r.text)
