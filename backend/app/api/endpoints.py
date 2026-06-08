from fastapi import APIRouter
import os
from backend.src.midi_processor import get_spotify_access_token, search_spotify_track, get_audio_features

router = APIRouter()


# Cache token locally so you don't call Spotify on every single page click
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


@router.get("/api/spotify/track-features")
def get_track_audio_features(track_title: str):
    # 1. Grab a fresh valid token
    print(f"DEBUG ID: {SPOTIFY_CLIENT_ID}")
    print(f"DEBUG SECRET: {SPOTIFY_CLIENT_SECRET}")
    token = get_spotify_access_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

    # 2. Query Spotify's metadata
    search_results = search_spotify_track(track_title, token)
    id = search_results["tracks"]["items"][0]["id"]
    audio_features = get_audio_features(id, token)
    # (Extract target features like tempo, valence, or energy to pass to your Genetic Algorithm!)
    return {"track_data": audio_features}