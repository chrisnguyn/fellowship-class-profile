# This is an example of how you would get number of commits (default is one year)
# Found on Stack Overflow (in JavaScript) - https://stackoverflow.com/questions/18262288/finding-total-contributions-of-a-user-from-github-api

import requests
import json

query = """query { 
    viewer { 
        name
        contributionsCollection(from: "2020-06-01T00:00:00Z", to: "2020-08-24T23:59:59Z") {
            contributionCalendar {
                totalContributions
            }
        }
    }
}"""

url = "https://api.github.com/graphql"
r = requests.post(url, headers={"Authorization": "Bearer TOKEN"}, json={"query": query})
num = json.loads(r.text)["data"]["viewer"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]

print('In 12 weeks, you made ' + str(num) + ' commits!')
