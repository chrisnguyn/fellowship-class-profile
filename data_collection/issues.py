# Get ALL issues within time frame per user
# Need to make a token for authentication, can't use the GraphQL endpoint without it

import requests
import json

# username = "YKo20010"
# TODO: need to pass username dynamically.
query = """query {
    user(login: "YKo20010") {
        contributionsCollection(from: "2020-06-01T00:00:00Z", to: "2020-08-24T23:59:59Z") {
            issueContributions(last: 20) {
                edges {
                    node {
                        issue {
                        bodyText
                        bodyHTML
                        id
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