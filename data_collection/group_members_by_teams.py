from general.static import count, end_date, endpoints, start_date
from general.user import username, user_token
import json
import requests

url = "https://api.github.com/orgs/MLH-Fellowship/teams"

response = requests.get(
    url,
    headers={"Authorization": f"token {user_token}"}
)

data = json.loads(response.text)

team_slugs = []  # many teams. be sure to carefully select which ones you want to access.
team_members_master = {}

for dictionary in data:
    team_slugs.append(dictionary["slug"])

for team in team_slugs:
    team_members = []
    url = f"https://api.github.com/orgs/MLH-Fellowship/teams/{team}/members"

    response = requests.get(
        url,
        headers={"Authorization": f"token {user_token}"}
    )

    data = json.loads(response.text)

    for member in data:
        team_members.append(member["login"])
    
    team_members_master[team] = team_members

print(json.dumps(team_members_master))
