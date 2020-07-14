# Get user current number of followers and following.

import requests
import json

query = """query {
    viewer {
        login
        following {
            totalCount
        }
        followers {
            totalCount
        }
    }
}
"""

url = "https://api.github.com/graphql"
r = requests.post(url, headers={"Authorization": "Bearer TOKEN"}, json={"query": query})

user = json.loads(r.text)["data"]["viewer"]["login"]
followers = str(json.loads(r.text)["data"]["viewer"]["followers"]["totalCount"])
following = str(json.loads(r.text)["data"]["viewer"]["following"]["totalCount"])

print(user + "'s followers count: " + followers)
print(user + "'s following count: " + following)
