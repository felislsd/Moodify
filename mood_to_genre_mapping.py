import json


with open('genres.json', 'r') as f:
    genres_data = json.load(f)


available_genres = {genre['name'].lower() for genre in genres_data}




# mapping from detected emotions to Spotify genres
mood_to_genres = {
    "joy": ["pop", "eurodance", "dancehall", "funk"],
    "sadness": ["blues", "soul"],
    "anger": ["metal", "punk"],
    "fear": ["ambient", "minimal techno" ],
    "love": ["lounge house", "r&b", "romantic", "lovers rock"],
    "surprise": ["electronic", "glitch"],
    

}



# to get genres for a detected mood
def get_genres_for_mood(mood):
    genres = mood_to_genres.get(mood, ["pop"])
    return [genre for genre in genres if genre in available_genres]
