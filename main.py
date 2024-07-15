#!/usr/bin/python3

from spotify_auth import get_spotify_token, read_saved_token
from spotify_search import get_recommendations_by_mood
from mood_to_genre_mapping import get_genres_for_mood
from dotenv import load_dotenv
import os
from transformers import pipeline

# Load environment variables from .env file
load_dotenv()

# Load the emotion detection model
emotion_classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

def detect_emotion(text):
    predictions = emotion_classifier(text)
    # Get the emotion with the highest score
    top_emotion = max(predictions, key=lambda x: x['score'])
    return top_emotion['label']

if __name__ == "__main__":
    # Read saved token or get a new one
    access_token = read_saved_token()
    if not access_token:
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        access_token = get_spotify_token(client_id, client_secret)


    # Take user input for text describing mood
    #user_text = input("Enter your mood (e.g., happy, sad, relaxed, energetic, angry, anxious): ").strip().lower()

    # Take user input for text describing mood
    user_text = input("How was your day: ").strip().lower()

    # Get genres for the given mood
    #genres = get_genres_for_mood(user_text)

    # Detect emotion from the text input
    detected_emotion = detect_emotion(user_text)
    print(f"Detected emotion: {detected_emotion}")

    # Get genres for the detected emotion
    genres = get_genres_for_mood(detected_emotion)

    if not genres:
        print(f"No available genres found for mood '{user_text}'. Please try a different mood.")
    else:
      

        # Get recommendations based on the mapped Spotify genres
        try:
            tracks = []
            for genre in genres:
                tracks.extend(get_recommendations_by_mood(genre, access_token))
            
            if not tracks:
                print("No recommendations found for this mood. Please try a different mood.")
            else:
                print("Based on your mood, we recommend these songs:")
                for track in tracks:
                    track_name = track['name']
                    artist_name = track['artists'][0]['name']
                    track_link = track['external_urls']['spotify']
                    print(f"- {track_name} by {artist_name} - [Listen]({track_link})")
        except Exception as e:
            print(f"An error occurred: {e}")
