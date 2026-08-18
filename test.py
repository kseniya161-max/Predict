import requests

url = "https://api.football-data.org/v4/matches"

headers = {
    "X-Auth-Token": ""
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())