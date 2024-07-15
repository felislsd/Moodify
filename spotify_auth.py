#!/usr/bin/python3
import requests
import base64
import json
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_spotify_token(client_id, client_secret):
    encoded_credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    auth_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code == 200:
        token_info = response.json()
        # Save token to a file
        with open('token.json', 'w') as token_file:
            json.dump(token_info, token_file)
        return token_info['access_token']
    else:
        raise Exception(f"Failed to get token. Status code: {response.status_code}\n{response.text}")

def read_saved_token():
    try:
        with open('token.json', 'r') as token_file:
            token_info = json.load(token_file)
        return token_info['access_token']
    except FileNotFoundError:
        return None