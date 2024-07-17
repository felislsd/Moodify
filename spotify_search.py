#!/usr/bin/python3

import requests
import time


request_counter = 0

def get_recommendations_by_mood(mood, access_token):
    global request_counter  # Declare the counter as global
    recommendation_url = "https://api.spotify.com/v1/recommendations"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        #'seed_genres': mood,
        'seed_genres': ','.join(mood),
        'limit': 10
    }
    response = requests.get(recommendation_url, headers=headers, params=params)

    #print("Request URL:", response.url)
    #print("Status Code:", response.status_code)
    #print("Response JSON:", response.json())

    # if response.status_code == 200:
    #     return response.json()['tracks']
    # else:
    #     raise Exception(f"Failed to get recommendations. Status code: {response.status_code}\n{response.text}")

    while True:
        response = requests.get(recommendation_url, headers=headers, params=params)

        # Increment the request counter
        request_counter += 1

        if response.status_code == 200:
            return response.json()['tracks']
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 1))  # Default to 1 second if not provided
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
        else:
            raise Exception(f"Failed to get recommendations. Status code: {response.status_code}\n{response.text}")
