# Found on Stack Overflow (in JavaScript) - https://stackoverflow.com/questions/18262288/finding-total-contributions-of-a-user-from-github-api
# Example of using the GitHub API v4

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