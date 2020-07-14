# This is an example of how you would get the number of line changes in a commit.
# https://api.github.com/repos/:owner/:repo/commits


import requests

url = "https://api.github.com/repos/chrisngyn/rosie/commits/36bacfea66defdaa18fe030317d2182684b69a06"  # need to provide a commit hash

response = requests.get(url).json()

print(response["stats"]["total"])  # number of lines changes
print(len(response["files"]))  # number of files changes in a commit
