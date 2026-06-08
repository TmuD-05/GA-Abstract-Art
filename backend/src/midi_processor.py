import requests
import base64

def get_spotify_access_token(client_id:str, client_secret:str):
    url = "https://accounts.spotify.com/api/token"

    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), encoding="utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"--- SPOTIFY REJECTION DETAILS: Status {response.status_code} | Body: {response.text}")
        raise Exception("Failed to get access token")

def search_spotify_track (track_name:str,access_token:str):
    url = f"https://api.spotify.com/v1/search?q={track_name}&type=track&limit=1"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response =requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"--- SPOTIFY REJECTION DETAILS: Status {response.status_code} | Body: {response.text}")
        raise Exception("Failed to get track list")
def get_audio_features(track_id:str,access_token:str):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url,headers=headers)
    print(f"--- MOCK AUDIO FEATURES DEBUG: Status {response.status_code} | Body: {response.text}")
    if response.status_code == 200:
        return response.json()
    else:
        return "Failed to get audio features"