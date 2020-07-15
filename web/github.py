import os

import requests


class GitHubExtension:
    API_URL = 'https://api.github.com'
    ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')

    def __init__(self):
        self.user_info = None

    def get_basic_user_info(self, access_token):
        url = self.API_URL + '/user'
        params = {'access_token': access_token}

        user = requests.get(url, params=params).json()
        self.user_info = user

        return user

    def get_access_token_with_auth_code(self, auth_code):
        return requests.post(
            self.ACCESS_TOKEN_URL,
            params={
                'client_id': self.GITHUB_CLIENT_ID,
                'client_secret': self.GITHUB_CLIENT_SECRET,
                'code': auth_code
            }, headers={'Accept': 'application/json'})

    def get_user_repos(self, access_token):
        params = {'access_token': access_token}
        username = self.get_basic_user_info(access_token)['login']

        url = self.API_URL + '/users/' + username + '/repos'
        repos = requests.get(url, params=params).json()
        return repos

    def invite_user_to_repo(self, repo, access_token, user_to_add):
        params = {'access_token': access_token }

        url = self.API_URL + f"/repos/{repo.git_user}/{repo.repo_name}/collaborators/{user_to_add}"
        print(url)
        result = requests.put(url, params=params).json()

        return result
