from flask import Flask, jsonify, request
import random
import requests
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GENIUS_API_KEY = os.getenv('GENIUS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

def fetch_top_songs():

    headers = {"Authorization": f"Bearer {GENIUS_API_KEY}"}

    while True:
        random_artist_id = random.randint(1, 10)
        url = f"https://api.genius.com/artists/563/songs?sort=popularity&per_page=2&page={random_artist_id}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            break  # Exit the loop if the request is successful
        elif response.status_code == 404:
            print(f"Artist with ID {random_artist_id} not found. Trying again...")

    print(f"{url}")
    print(data['response']['songs'][0]['full_title'])
    print(data['response']['songs'][1]['full_title'])

    return data['response']['songs']

top_songs = fetch_top_songs()

def generate_description(song):
    prompt = f"Describe the song '{song['title']}' by {song['primary_artist']['name']} with key visual moments."
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        #model="gpt4o",
        messages=messages,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

descriptions = {song['id']: generate_description(song) for song in top_songs}


def generate_images(description):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=description,
        n=1,
        size="1024x1024"
)
    image_url = response.data[0].url
    return [{"url":image_url}]

images = {song_id: generate_images(description) for song_id, description in descriptions.items()}

user_scores = {}

@app.route("/api/random-image")
def random_image():
    try:
        song_id = random.choice(list(images.keys()))
        image_url = images[song_id][0]['url']
        return jsonify({"url": image_url, "song_id": song_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#def guess():
    try:
        data = request.get_json()
        user = data["user"]
        guess = data["guess"]
        song_id = data["song_id"]
        print(f"Received guess: {guess} for song ID: {song_id}")

     #   if song_id not in top_songs[0]['id']:
      #      raise ValueError("Invalid song ID")

        if guess.lower() == top_songs[0]['title'].lower():
            user_scores[user] = user_scores.get(user, 0) + 1
            print(f"Correct guess. Score for {user}: {user_scores[user]}")
            return jsonify({"correct": True, "score": user_scores[user]})
        else:
            print("Incorrect guess.")
            return jsonify({"correct": False, "score": user_scores.get(user, 0)})
    except Exception as e:
        print(f"Error: {e}")  # Log the error to help with debugging
        return jsonify({"error": str(e)}), 500

@app.route("/api/guess", methods=["POST"])
def guess():
    try:
        data = request.get_json()
        user = data["user"]
        guess = data["guess"]
        song_id = data["song_id"]
        print(f"Received guess: {guess} for song ID: {song_id}")

        if guess.lower() == top_songs[0]['title'].lower():
            user_scores[user] = user_scores.get(user, 0) + 1
            print(f"Correct guess. Score for {user}: {user_scores[user]}")

            # Generate new song and image
            new_song = top_songs[1]
            new_description = generate_description(new_song)
            new_image_url = generate_images(new_description)
            new_song_id = new_song['id']

            # Update the images dictionary
            images[new_song_id] = new_image_url

            return jsonify({"correct": True, "score": user_scores[user], "new_image_url": new_image_url, "new_song_id": new_song_id})
        else:
            print("Incorrect guess.")
            return jsonify({"correct": False, "score": user_scores.get(user, 0)})
    except Exception as e:
        print(f"Error: {e}")  # Log the error to help with debugging
        return jsonify({"error": str(e)}), 500

@app.route("/api/hint", methods=["POST"])
def hint():
    try:
        data = request.get_json()
        song_id = data["song_id"]
      #  if song_id not in images:
     #       raise ValueError("Invalid song ID")
        new_image_url = images[song_id][1]['url']
        return jsonify({"url": new_image_url, "song_id": song_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)