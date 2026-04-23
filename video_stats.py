import requests
import json
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")
API_KEY = os.getenv("API_KEY")


CHANNEL_HANDLE = "MrBeast"


def get_playlist_id(channel_handle):
    try: 
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        channel_items = data["items"][0]
        channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        return channel_playlistId
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching playlist ID: {e}")
        return None
    

if __name__ == "__main__":
    playlist_id = get_playlist_id(CHANNEL_HANDLE)
    if playlist_id:
        print(f"Playlist ID for channel '{CHANNEL_HANDLE}': {playlist_id}")
    else:
        print("Failed to retrieve playlist ID.")

    
