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

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=['200 per day']
)

#cache model
def load_emotion_classifier():
    if 'emotion_classifier' not in g:
        g.emotion_classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")
    return g.emotion_classifier



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods = ['POST'])
@limiter.limit("10 per minute")
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
@limiter.limit("10 per minute")
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
    app.run()


