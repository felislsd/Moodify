# Moodify

**Moodify** is a sentiment-based music recommendation app. It analyzes the user's input text to detect their current mood and recommends a Spotify song that matches the identified mood. 

## Features

- Text sentiment analysis to detect user mood
- Spotify song recommendations based on detected mood
- Simple and intuitive web interface

## File Descriptions

- **`genres.json`**: This file contains a list of music genres that are used to map emotions to corresponding music genres for song recommendations. It acts as a reference for the app to understand which genres are available for recommendations.

- **`main.py`**: This is the main application file that initializes and runs the Flask web server. It handles routes and user interactions, processes the text input to detect emotions using a sentiment analysis model, maps the detected emotion to music genres, fetches song recommendations from Spotify, and renders the results back to the user. It also includes rate limiting to prevent abuse.

- **`mood_to_genre_mapping.py`**: This file defines a mapping between detected emotions and music genres. It includes a function to retrieve genres for a given mood, ensuring the genres are available in the Spotify catalog.

- **`requirements.txt`**: This file lists all the Python dependencies required to run the application. It includes libraries for Flask, sentiment analysis, Spotify API integration, and other necessary packages. It ensures that anyone who wants to set up the app can install all dependencies easily.

- **`spotify_auth.py`**: This file handles authentication with the Spotify API. It includes functions to obtain and refresh access tokens required to make requests to the Spotify API. The credentials for the Spotify API are securely managed using environment variables.

- **`spotify_search.py`**: This file contains functions to interact with the Spotify API for searching and fetching song recommendations based on the detected mood. It manages API requests, handles rate limiting, and processes the responses to extract relevant song information.

### How to run it?

1. **Clone the Repository**:
git clone https://github.com/your-username/moodify.git
cd moodify

2. **Create Spotify Developer account to obtain API credentials**

3. **Create ".env" file:**

'''
FLASK_APP=main.py
FLASK_ENV=development #for debugging purposes
CLIENT_ID='xxx'
CLIENT_SECRET='yyy'

4. **Install the dependencies:**

pip install -r requirements.txt

5. **flask run :)**




