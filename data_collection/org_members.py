# This is an example of how you would grab all the members of a GitHub organization.
# https://api.github.com/orgs/:org/members


import requests

page_num = 1
url = 'https://api.github.com/orgs/MLH-Fellowship/members?page={}'.format(page_num)

while True:
    response = requests.get(url).json()

    if response['message']:
        print('You were rate limited! Please authenticate yourself for more requests.')
        return

    for user in response:
        print(user['login'])

    if (len(response) == 30):  # requests only returns 30 at one time, so if we get 30, there might be another page of users
        page_num += 1
        url = 'https://api.github.com/orgs/MLH-Fellowship/members?page={}'.format(page_num)  # restructure the URL
    else:
        break