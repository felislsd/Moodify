#!/usr/bin/python3

import requests
import json
from dotenv import load_dotenv
import os
import base64

# Load environment variables from .env file
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
        return token_info['access_token']
    else:
        raise Exception(f"Failed to get token. Status code: {response.status_code}\n{response.text}")

def get_available_genres(token):
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('genres', [])
    else:
        print(f"Failed to get available genres. Status code: {response.status_code}\n{response.text}")
        return []

if __name__ == "__main__":
    access_token = get_spotify_token(client_id, client_secret)
    available_genres = get_available_genres(access_token)
    
    with open('available_genres.json', 'w') as f:
        json.dump(available_genres, f, indent=4)
    
    print(f"Available genres saved to available_genres.json")
