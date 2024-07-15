#!/usr/bin/python3

import requests

def get_recommendations_by_mood(mood, access_token):
    recommendation_url = "https://api.spotify.com/v1/recommendations"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'seed_genres': mood,
        'limit': 10
    }
    response = requests.get(recommendation_url, headers=headers, params=params)

    #print("Request URL:", response.url)
    #print("Status Code:", response.status_code)
    #print("Response JSON:", response.json())

    if response.status_code == 200:
        return response.json()['tracks']
    else:
        raise Exception(f"Failed to get recommendations. Status code: {response.status_code}\n{response.text}")
