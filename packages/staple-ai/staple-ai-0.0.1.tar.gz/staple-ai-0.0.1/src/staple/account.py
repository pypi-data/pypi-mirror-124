import requests
import getpass
import json


def login():
    url = "https://api-gateway.staple.io/v1/users/login"

    email = input('Enter your email assoiated with staple:')
    password = getpass.getpass('Enter your password:')

    payload = json.dumps({
    "credential": {
        "email": email,
        "password": password
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text



