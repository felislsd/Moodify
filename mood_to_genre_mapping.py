import json

# Load the list of genres from genres.json
with open('genres.json', 'r') as f:
    genres_data = json.load(f)

# Create a set of available genres for quick lookup
available_genres = {genre['name'].lower() for genre in genres_data}

# Define a mapping from detected emotions to Spotify genres
mood_to_genres = {
    "joy": ["pop", "dance-pop", "happy", "party", "funk", "disco"],
    "sadness": ["blues", "sad", "acoustic blues", "soul blues", "gospel blues"],
    "anger": ["metal", "heavy metal", "hard rock", "punk", "hardcore"],
    "fear": ["ambient", "minimal", "drone", "meditation", "new age"],
    "surprise": ["electronic", "experimental", "avant-garde", "psychedelic"],
    "love": ["romantic", "love songs", "soft rock", "r&b"],
}

# Function to get genres for a detected mood
def get_genres_for_mood(mood):
    genres = mood_to_genres.get(mood, ["pop"])
    return [genre for genre in genres if genre in available_genres]
