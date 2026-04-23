import requests
import json
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"
max_Results = 50

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
    

def get_video_ids(playlist_id):
    video_ids = []
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_Results}&playlistId={playlist_id}&key={API_KEY}"
    pageToken = None

    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            for item in data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)

            pageToken = data.get("nextPageToken")

            if not pageToken:
                break

        return video_ids

    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    playlist_id = get_playlist_id(CHANNEL_HANDLE)
    # if playlist_id:
    #     print(f"Playlist ID for channel '{CHANNEL_HANDLE}': {playlist_id}")
    # else:
    #     print("Failed to retrieve the playlist ID.")

    video_ids = get_video_ids(playlist_id)
    # print(f"Video IDs in the playlist: {video_ids}")