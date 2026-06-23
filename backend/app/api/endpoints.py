from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from backend.src.midi_processor import get_spotify_access_token, search_spotify_track, get_audio_features
from backend.src.genetic_algorithm import ga_main
from backend.src.render import make_fluid_image, save_image

router = APIRouter()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SOUND_CHART_ID = os.getenv("SOUND_CHART_ID")
SOUND_CHART_SECRET = os.getenv("SOUND_CHART_TOKEN")

STATIC_DIR = "backend/app/static"

class AudioFeaturesPayload(BaseModel):
    energy: float
    valence: float
    density: float | None = None

@router.get("/spotify/search")
def search_song(track_title: str):
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
            "album_art": item.get("album", {}).get("images", [{}])[0].get("url") if item.get("album", {}).get("images") else None,
            "album_art_thumb": item.get("album", {}).get("images", [{}])[-1].get("url") if item.get("album", {}).get("images") else None,
        })
    return {"results": formatted_results}


@router.get("/soundchart/features/{track_id}")
def get_track_audio_features(track_id: str):
    try:
        track_data = get_audio_features(track_id, SOUND_CHART_ID, SOUND_CHART_SECRET)
        return {"audio_features": track_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate-art")
def generate_track_art(payload: AudioFeaturesPayload):
    try:
        target_features = {
            "energy": payload.energy,
            "valence": payload.valence,
            "density": payload.density if payload.density is not None else payload.energy
        }

        best_chromosome = ga_main(target_features, pop_size=15, generations=20)
        canvas = make_fluid_image(width=800, height=800, chromosome=best_chromosome)
        filename = save_image(canvas, folder=STATIC_DIR)
        image_url = f"/static/{os.path.basename(filename)}"

        return {
            "success": True,
            "image_url": image_url,
            "features_used": target_features
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))