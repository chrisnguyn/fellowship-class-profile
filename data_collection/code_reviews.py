
import requests

url = "https://api.github.com/"  # need to provide a commit hash

response = requests.get(url).json()

# print(response["stats"]["total"])
