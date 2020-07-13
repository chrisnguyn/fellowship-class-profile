# Example of using the GitHub API v4
# Need to make a token for authentication, can't use the GraphQL endpoint without it

import requests
import json

query = """query {
    viewer { 
        login
        name
    }
}"""

url = "https://api.github.com/graphql"
r = requests.post(url, headers={"Authorization": "Bearer TOKEN"}, json={"query": query})
print(r.text)
