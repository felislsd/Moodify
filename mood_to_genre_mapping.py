import json

# Load the list of genres from genres.json
with open('genres.json', 'r') as f:
    genres_data = json.load(f)

# Create a set of available genres for quick lookup
available_genres = {genre['name'].lower() for genre in genres_data}


# Print available genres to debug
#print(f"Available genres: {available_genres}")

# Define a mapping from detected emotions to Spotify genres
mood_to_genres = {
    "joy": ["pop", "eurodance", "dancehall", "funk"],
    "sadness": ["blues", "soul"],
    "anger": ["metal", "punk"],
    "fear": ["ambient", "minimal techno" ],
    "love": ["lounge house", "r&b", "romantic", "lovers rock"],
    "surprise": ["electronic", "glitch"],
    

}

# mood_to_genres = {
#     "joy": ["pop", "eurodance", "dancehall", "funk", "disco", "happy hardcore", "disco house", "uplifting trance", "bubblegum pop", "italo dance", "electro house"],
#     "sadness": ["blues", "soul", "southern soul", "gospel blues", "louisiana blues", "piano blues", "delta blues"],
#     "anger": ["death metal", "metal", "punk", "thrash metal", "grindcore", "hardcore punk", "industrial metal", "black metal"],
#     "fear": ["ambient", "minimal techno", "new age", "dark ambient", "organic ambient", "ambient trance", "deep ambient", "drone", "dark wave", "illbient", "experimental dubstep", "deep darkpsy" ],
#     "surprise": ["electronic", "glitch", "idm", "breakcore", "futurepop", "wonky"],
#     "love": ["lovers rock", "r&b", "romantic", "quiet storm", "neo-soul", "smooth urban r&b", "soul flow"],
#
# }

# Function to get genres for a detected mood
def get_genres_for_mood(mood):
    genres = mood_to_genres.get(mood, ["pop"])
    return [genre for genre in genres if genre in available_genres]
