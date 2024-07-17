#!/usr/bin/python3

import requests
import time
import random


request_counter = 0

def make_request(url, headers, params):
    global request_counter
    while True:
        response = requests.get(url, headers=headers, params=params)
        request_counter += 1

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 10))  # Default to 10 seconds if not provided
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
        else:
            raise Exception(f"Failed to get data. Status code: {response.status_code}\n{response.text}")

def get_recommendations_by_mood(mood, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    if mood == "love":
        words = ['love', 'amor', 'liebe', 'amour', 'любовь', '愛', 'حب']
        query = ' OR '.join(words)
        search_url = 'https://api.spotify.com/v1/search'
        params = {
            'q': query,
            'type': 'track',
            'limit': 50
        }
        data = make_request(search_url, headers, params)
        return data['tracks']['items']
    else:
        recommendation_url = 'https://api.spotify.com/v1/recommendations'
        params = {
            'seed_genres': ','.join(mood),
            'limit': 10
        }
        data = make_request(recommendation_url, headers, params)
        return data['tracks']
    

def display_tracks(tracks):
    current_index = 0
    while True:
        track = tracks[current_index]
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        track_link = track['external_urls']['spotify']
        print(f"- {track_name} by {artist_name} - [Listen]({track_link})")

        user_input = input("Do you want to listen to another recommendation? (yes/no): ").strip().lower()
        if user_input == 'no':
            print("Thank you! Enjoy your music!")
            break
        current_index = (current_index + 1) % len(tracks)
