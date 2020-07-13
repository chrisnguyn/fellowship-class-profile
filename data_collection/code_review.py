# Get ALL code reviews within time frame per user
# Need to make a token for authentication, can't use the GraphQL endpoint without it

import requests
import json

# username = "YKo20010"
# TODO: need to pass username through dynamically.
# WIP: looks like issueComments doesn't encompass all code review.
query = """query {
    user(login: "YKo20010") {
        contributionsCollection {
            user {
                issueComments(first: 10) {
                    edges {
                        node {
                        id
                        bodyText
                        }
                    }
                }
            }
        }
    }
}"""

url = "https://api.github.com/graphql"
r = requests.post(url, headers={"Authorization": "Bearer TOKEN"}, json={"query": query})
print(r.text)