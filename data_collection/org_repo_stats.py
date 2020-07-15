import json
import requests

from general.static import end_date, endpoints, start_date
from general.user import username, user_token
from typing import Dict


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
        endpoints["github"], headers={"Authorization": f"token {user_token}"}, json={"query": num_repo_query})
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
        endpoints["github"], headers={"Authorization": f"token {user_token}"}, json={"query": repo_info_query})
    return json.loads(r.text)["data"]["organization"]["repositories"]["nodes"]

if __name__ == "__main__":
    num_original_repo = get_number_repos_in_MLH(isFork="false")
    num_forked_repo = get_number_repos_in_MLH(isFork="true")
    all_repos = get_all_forked_repos_in_MLH()
