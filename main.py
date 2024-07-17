#!/usr/bin/python3

from spotify_auth import get_access_token
from spotify_search import get_recommendations_by_mood, display_tracks, request_counter
from mood_to_genre_mapping import get_genres_for_mood
from dotenv import load_dotenv
import os
from transformers import pipeline
# from search_love_song import search_songs_with_love
# import random

# Load environment variables from .env file
load_dotenv()

# Load the emotion detection model
emotion_classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

def detect_emotion(text):
    predictions = emotion_classifier(text)
    top_emotion = max(predictions, key=lambda x: x['score'])
    return top_emotion['label']

if __name__ == "__main__":
    user_text = input("How was your day: ").strip().lower()

    detected_emotion = detect_emotion(user_text)
    print(f"Detected emotion: {detected_emotion}")

    genres = get_genres_for_mood(detected_emotion)
    print(f"Matched genres for emotion '{detected_emotion}': {genres}")

    access_token = get_access_token()

    try:
        if detected_emotion != "love":
            if not genres:
                print(f"No available genres found for mood '{user_text}'. Please try a different mood.")
            else:
                # Get recommendations based on the mapped Spotify genres
                tracks = []
                for genre in genres:
                    tracks.extend(get_recommendations_by_mood([genre], access_token))

                if not tracks:
                    print("No recommendations found for this mood. Please try a different mood.")
                else:
                    display_tracks(tracks)
        else:
            tracks = get_recommendations_by_mood("love", access_token)
            if not tracks:
                print("No tracks found containing the word 'love'.")
            else:
                display_tracks(tracks)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print(f"Total requests made: {request_counter}")


