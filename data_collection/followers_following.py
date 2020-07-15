# Get user current number of followers and following.

from data_collection.general.static import count, end_date, endpoints, start_date
from data_collection.general.user import username, user_token
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

    data = json.loads(response.text)
    followers = str(data["data"]["user"]["followers"]["totalCount"])
    following = str(data["data"]["user"]["following"]["totalCount"])

    return followers, following

if __name__ == "__main__":
    followers, following = get_followers_following(username)

    print(username + "'s followers count: " + followers)
    print(username + "'s following count: " + following)
