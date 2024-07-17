#!/usr/bin/python3

from spotify_auth import get_access_token
from spotify_search import get_recommendations_by_mood, request_counter
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
    # Take user input for text describing mood
    user_text = input("How was your day: ").strip().lower()

    # Detect emotion from the text input
    detected_emotion = detect_emotion(user_text)
    print(f"Detected emotion: {detected_emotion}")

    # Get genres for the detected emotion
    genres = get_genres_for_mood(detected_emotion)
    print(f"Matched genres for emotion '{detected_emotion}': {genres}")

    if not genres:
        print(f"No available genres found for mood '{user_text}'. Please try a different mood.")
    else:
        # Get a valid access token before making the request
        access_token = get_access_token()

        # Get recommendations based on the mapped Spotify genres
        try:
            tracks = []
            for genre in genres:
                tracks.extend(get_recommendations_by_mood([genre], access_token))

            if not tracks:
                print("No recommendations found for this mood. Please try a different mood.")
            else:
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
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print(f"Total requests made: {request_counter}")
