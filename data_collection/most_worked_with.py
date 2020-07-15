import json
import requests

from general.static import count, end_date, endpoints, start_date
from general.user import username, user_token
from typing import Dict, List


def update_ppl_worked_with(user: str, pull_request_contributions_nodes: List, ppl_worked_with: Dict):
    for pull_request in pull_request_contributions_nodes:
        for participant in pull_request["pullRequest"]["participants"]["nodes"]:
            if participant["login"] != user:
                if participant["login"] in ppl_worked_with:
                    ppl_worked_with[participant["login"]] += 1
                else:
                    ppl_worked_with[participant["login"]] = 1


def customize_query(user: str, cursor_str: str, num_users: int) -> str:
    return f"""
            query {{
            user(login:"{user}"){{
                contributionsCollection(from: "2020-06-01T07:00:00Z", to:"2020-08-24T07:00:00Z"){{
                    pullRequestContributions(first:5 {cursor_str}){{
                    pageInfo{{
                        endCursor
                        hasNextPage
                    }}
                    nodes{{
                    pullRequest{{
                        baseRepository{{
                        nameWithOwner
                        }}
                        participants(first:{num_users}){{
                        totalCount
                        nodes{{
                            login
                        }}
                        pageInfo{{
                            endCursor
                            hasNextPage
                        }}
                        }}
                    }}
                    }}
                }}
            }}
            }}
        }}"""


def get_people_worked_with(user: str) -> Dict:
    ppl_worked_with = {}
    cursor = None
    cursor_str = ""
    num_users = 1
    while True:
        r = requests.post(
            endpoints["github"], headers={"Authorization": f"token {user_token}"}, json={"query": customize_query(user, cursor_str, num_users)})

        response = json.loads(r.text)
        prs = response["data"]["user"]["contributionsCollection"]["pullRequestContributions"]["nodes"]

        new_total = num_users
        for pr in prs:
            if pr["pullRequest"]["participants"]["pageInfo"]["hasNextPage"]:
                if pr["pullRequest"]["participants"]["totalCount"] > new_total:
                    new_total = pr["pullRequest"]["participants"]["totalCount"]+1
        if new_total > num_users:
            num_users = new_total
            r = requests.post(endpoints["github"], headers={"Authorization": f"token {user_token}"}, json={
                              "query": customize_query(user, cursor_str, num_users)})
            response = json.loads(r.text)

        update_ppl_worked_with(user, response["data"]["user"]["contributionsCollection"]
                               ["pullRequestContributions"]["nodes"], ppl_worked_with)

        pageInfo = response["data"]["user"]["contributionsCollection"]["pullRequestContributions"]["pageInfo"]
        if not pageInfo["hasNextPage"]:
            break
        cursor = pageInfo["endCursor"]
        cursor_str = f", after: \"{cursor}\""
    return ppl_worked_with


if __name__ == "__main__":
    people = get_people_worked_with(username)
    print("People worked with (desc order):", {k: v for k, v in sorted(
        people.items(), key=lambda item: item[1], reverse=True)})
