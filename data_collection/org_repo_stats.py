import json
import os
import requests
from typing import Dict

token = os.environ["GITHUB_API_TOKEN"]
url = "https://api.github.com/graphql"


def get_number_repos_in_MLH(isFork: str = "true") -> int:
    num_repo_query = f"""
    query {{
        organization(login: "MLH-Fellowship"){{
            repositories(isFork: {isFork}){{
                totalCount
            }}
        }}
    }}
    """
    r = requests.post(
        url, headers={"Authorization": f"token {token}"}, json={"query": num_repo_query})
    return json.loads(r.text)["data"]["organization"]["repositories"]["totalCount"]


def get_all_forked_repos_in_MLH() -> Dict:
    num_forked_repo = get_number_repos_in_MLH(isFork="true")
    repo_info_query = f"""
    query {{ 
        organization(login: "MLH-Fellowship"){{
            repositories(first: {num_forked_repo}, isFork: true) {{
                totalCount
                nodes {{
                    name
                    parent{{
                        nameWithOwner
                    }}
                    primaryLanguage{{
                        name
                    }}
                    homepageUrl
                    url
                }}
            }}
        }}
    }}"""

    r = requests.post(
        url, headers={"Authorization": f"token {token}"}, json={"query": repo_info_query})
    return json.loads(r.text)["data"]["organization"]["repositories"]["nodes"]


num_original_repo = get_number_repos_in_MLH(isFork="false")
num_forked_repo = get_number_repos_in_MLH(isFork="true")
num_repos = get_all_forked_repos_in_MLH()
