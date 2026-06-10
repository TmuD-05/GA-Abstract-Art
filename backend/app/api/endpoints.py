from fastapi import APIRouter, HTTPException
import os
from backend.src.midi_processor import get_spotify_access_token, search_spotify_track, get_audio_features

router = APIRouter()


# Cache token locally so you don't call Spotify on every single page click
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SOUND_CHART_ID = os.getenv("SOUND_CHART_ID")
SOUND_CHART_SECRET = os.getenv("SOUND_CHART_TOKEN")

@router.get("/spotify/search")
def search_song(track_title:str):

    token = get_spotify_access_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    search_results = search_spotify_track(track_title, token)
    items = search_results.get("tracks", {}).get("items", [])

    if not items:
        return {"results": []}

    formatted_results = []

    for item in items:
        artists_list = item.get("artists") or []
        artist_name = artists_list[0].get("name", "Unknown Artist") if artists_list else "Unknown Artist"
        formatted_results.append({
            "id": item.get("id"),
            "title": item.get("name"),
            "artist": artist_name,
            "preview_url": item.get("preview_url"),
            "album_art": item.get("album", {}).get("images", [{}])[-1].get("url") if item.get("album", {}).get(
                "images") else None
        })
    return {"results": formatted_results}

@router.get("/soundchart/features/{track_id}")
def get_track_audio_features(track_id: str):
    try:

        track_data = get_audio_features(track_id, SOUND_CHART_ID, SOUND_CHART_SECRET)
        audio_features = track_data.get("object", {}).get("audio", {})
        return {"audio_features": audio_features}

    except Exception as e:

        raise HTTPException(status_code=400, detail=str(e))
