import requests
import random
from spotify_auth import get_access_token

def search_songs_with_love(access_token):
    headers = {
        'Authorization' : f'Bearer {access_token}'
    }

    words = ['love', 'amor', 'liebe', 'amour', 'любовь', '愛', 'حب']
    query = ' OR '.join(words)
    search_url = 'https://api.spotify.com/v1/search'
    params = {
        'q': query,
        'type': 'track',
        'limit': 50
    }

    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['tracks']['items']
    else:
        raise Exception(f"Failed to search tracks. Status code: {response.status_code}\n{response.text}")

if __name__ == "__main__":
    try:
        access_token = get_access_token()
        tracks = search_songs_with_love(access_token)
        
        if tracks:
            selected_track = random.choice(tracks)
            track_name = selected_track['name']
            artist_name = selected_track['artists'][0]['name']
            track_link = selected_track['external_urls']['spotify']
            print(f"- {track_name} by {artist_name} - [Listen]({track_link})")
        else:
            print("No tracks found containing the word 'love'.")
    except Exception as e:
        print(f"An error occurred: {e}")  