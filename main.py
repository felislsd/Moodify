#!/usr/bin/python3

from spotify_auth import get_access_token
from spotify_search import get_recommendations_by_mood, display_tracks, request_counter
from mood_to_genre_mapping import get_genres_for_mood
from dotenv import load_dotenv
import os
from transformers import pipeline
from flask import Flask, request, render_template, jsonify, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random

app = Flask(__name__)

load_dotenv()

# limiter = Limiter(
#     app,
#     key_func=get_remote_address
#     default_limits=['200 per day']
# )

#cache model
def load_emotion_classifier():
    if 'emotion_classifier' not in g:
        g.emotion_classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")
    return g.emotion_classifier


# emotion_texts = {
#     "joy": [
#         "Good for you!",
#         "What a day!",
#         "I'm on top of the world!"
#     ],
#     "sadness": [
#         "Yep... sorry to hear that",
#         "Man, I feel so sorry for you, listen to this, maybe you'll get evem more depressed",
#         "Not in a good mood, huh?"
#     ],
#     "anger": [
#         "I'm so angry right now!",
#         "Everything is making me mad.",
#         "I'm furious!"
#     ],
#     "fear": [
#         "I'm really scared.",
#         "I feel very anxious and afraid.",
#         "This is terrifying."
#     ],
#     "love": [
#         "I'm feeling so much love.",
#         "Love is in the air.",
#         "I'm overwhelmed with love."
#     ],
#     "surprise": [
#         "What a surprise!",
#         "I didn't see that coming!",
#         "Wow, that's unexpected!"
#     ]
# }

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods = ['POST'])
# @limiter.limit("10 per minute")
def predict():
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    emotion_classifier = load_emotion_classifier()
    predictions = emotion_classifier(text)
    top_emotion = max(predictions, key=lambda x: x['score'])
    genres = get_genres_for_mood(top_emotion['label'])
    access_token = get_access_token()

    if top_emotion['label'] == "love":
        tracks = get_recommendations_by_mood("love", access_token)
    else:
        tracks = []
        for genre in genres:
            tracks.extend(get_recommendations_by_mood([genre], access_token))

    selected_track = random.choice(tracks) if tracks else None
    return render_template('result.html', emotion=top_emotion['label'], track=selected_track)


@app.route('/refresh', methods=['POST'])
# @limiter.limit("10 per minute")
def refresh():
    emotion = request.form.get('emotion')
    access_token = get_access_token()
    if emotion == "love":
        tracks = get_recommendations_by_mood("love", access_token)
    else:
        genres = get_genres_for_mood(emotion)
        tracks = []
        for genre in genres:
            tracks.extend(get_recommendations_by_mood([genre], access_token))
    
    selected_track = random.choice(tracks) if tracks else None
    return render_template('result.html', emotion=emotion, track=selected_track)

@app.teardown_appcontext
def teardown(exception):
    g.pop('emotion_classifier', None)


if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == '__main__':
#     app.run(debug=True)

# def detect_emotion(text):
#     predictions = emotion_classifier(text)
#     top_emotion = max(predictions, key=lambda x: x['score'])
#     return top_emotion['label']

# if __name__ == "__main__":
#     user_text = input("How was your day: ").strip().lower()

#     detected_emotion = detect_emotion(user_text)
#     print(f"Detected emotion: {detected_emotion}")

#     genres = get_genres_for_mood(detected_emotion)
#     print(f"Matched genres for emotion '{detected_emotion}': {genres}")

#     access_token = get_access_token()

#     try:
#         if detected_emotion != "love":
#             if not genres:
#                 print(f"No available genres found for mood '{user_text}'. Please try a different mood.")
#             else:
#                 # Get recommendations based on the mapped Spotify genres
#                 tracks = []
#                 for genre in genres:
#                     tracks.extend(get_recommendations_by_mood([genre], access_token))

#                 if not tracks:
#                     print("No recommendations found for this mood. Please try a different mood.")
#                 else:
#                     display_tracks(tracks)
#         else:
#             tracks = get_recommendations_by_mood("love", access_token)
#             if not tracks:
#                 print("No tracks found containing the word 'love'.")
#             else:
#                 display_tracks(tracks)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         print(f"Total requests made: {request_counter}")


