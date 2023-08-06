import json
import requests

def createGroup(name):
    url = "https://api-gateway.staple.io/v1/groups"

    apiKey = input('Enter your API Key')
    authorization = input('Enter your accessToken')

    payload = json.dumps({
    "name": name
    })
    headers = {
    'x-api-key': apiKey,
    'Authorization': 'Bearer ' + authorization,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text