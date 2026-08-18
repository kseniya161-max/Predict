import requests

url = "https://api.football-data.org/v4/matches"

headers = {
    "X-Auth-Token": "a5d744d4d7a04811806a614ab9802eb8"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())