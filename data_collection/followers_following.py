# Get user current number of followers and following.

from general.static import count, end_date, endpoints, start_date
from general.user import username, user_token
import json
import requests


def get_followers_following(user):
    follower_following_query = f"""query {{
        user(login: "{user}") {{
            login
            following {{
                totalCount
            }}
            followers {{
                totalCount
            }}
        }}
    }}"""
    response = requests.post(
        endpoints["github"],
        headers={"Authorization": f"Bearer {user_token}"},
        json={"query": follower_following_query}
    )

    return json.loads(response.text)


data = get_followers_following(user=username)
login = data["data"]["user"]["login"]
followers = str(data["data"]["user"]["followers"]["totalCount"])
following = str(data["data"]["user"]["following"]["totalCount"])

print(login + "'s followers count: " + followers)
print(login + "'s following count: " + following)
