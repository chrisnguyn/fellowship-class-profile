import json
import os
import requests

token = os.environ["GITHUB_API_TOKEN"]
user = "kbanc"


num_original_repo_query = """
query {
    organization(login: "MLH-Fellowship"){
        repositories(isFork: false){
            totalCount
        }
    }
}
"""
num_forked_repo_query = """
query {
    organization(login: "MLH-Fellowship"){
        repositories(isFork: true){
            totalCount
        }
    }
}
"""

url = "https://api.github.com/graphql"
r = requests.post(
    url, headers={"Authorization": f"token {token}"}, json={"query": num_forked_repo_query})

num_forked_repo = json.loads(r.text)["data"]["organization"]["repositories"]["totalCount"]

r = requests.post(
    url, headers={"Authorization": f"token {token}"}, json={"query": num_original_repo_query})
num_original_repo = json.loads(r.text)["data"]["organization"]["repositories"]["totalCount"]

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
repo_info = json.loads(r.text)["data"]["organization"]["repositories"]["nodes"]
