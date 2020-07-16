from data_collection.general.static import count, end_date, endpoints, start_date
from data_collection.general.user import username, user_token
import json
import requests


def get_members_by_teams():
    url = "https://api.github.com/orgs/MLH-Fellowship/teams"

    response = requests.get(
        url,
        headers={"Authorization": f"token {user_token}"}
    )

    data = json.loads(response.text)

    # many teams. be sure to carefully select which ones you want to access.
    team_slugs = []
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
    del team_members_master['mlh-fellows-summer-2020']
    return team_members_master


if __name__ == "__main__":
    print(get_members_by_teams())
