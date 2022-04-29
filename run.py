import os
import json
from dotenv import load_dotenv
from spotify_client import SpotifyClient

load_dotenv()

def run():
    # Get a list of Spotify Liked songs
    spotify_client = SpotifyClient(os.getenv('SPOTIFY_AUTH_TOKEN'))
    track_limit = 50
    liked_tracks = spotify_client.get_liked_songs(track_limit)

    # Detect language to extract list of only Spanish titles
    spanish_tracks = spotify_client.get_filtered_tracks(liked_tracks, 'es')

    with open ("spanish_tracks.json", "w") as f:
        json.dump(spanish_tracks, f, indent=4)

if __name__ == '__main__':
    run()