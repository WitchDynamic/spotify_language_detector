import requests
import json
from langdetect import detect


class SpotifyClient(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def get_liked_songs(self, track_limit, cache=False):
        if cache:
            try:
                with open("tracks.json") as f:
                    track_cache = json.load(f)
                print("Found existing cache...returning tracks.json")
                all_tracks = track_cache
            except Exception as e:
                print("Cache does not exist, will create later")
                all_tracks = []
        else:
            all_tracks = []

        while len(all_tracks) < track_limit:
            url = f"https://api.spotify.com/v1/me/tracks?offset={len(all_tracks)}&limit=50"

            print(f"Fetching songs {len(all_tracks)} - {len(all_tracks)+50}")
            response = requests.get(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
            )

            response_json = response.json()

            tracks = [
                {
                    "track_name": item["track"]["name"],
                    "track_artist": item["track"]["artists"][0]["name"],
                }
                for item in response_json["items"]
            ]

            all_tracks += tracks
            if len(tracks) < 50:
                break

        print(f"Found {len(all_tracks)} from your search")

        if cache:
            with open("tracks.json", "w") as f:
                json.dump(all_tracks, f)

        return all_tracks

    def get_filtered_tracks(self, tracks, lang_code):
        return list(
            filter(lambda track: self.detect_language(track, lang_code), tracks)
        )

    def detect_language(self, track, lang_code):
        song_name = track["track_name"]
        print(f"Detecting {song_name}")
        try:
            lang = detect(song_name)
        except Exception as e:
            print(f"The song: {song_name} failed with error {e}")
            return False

        if lang == lang_code:
            return True
        else:
            return False
