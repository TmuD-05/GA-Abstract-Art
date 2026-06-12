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

# Pydantic model so the frontend can safely pass the audio features
class AudioFeaturesPayload(BaseModel):
    energy: float
    valence: float
    density: float | None = None  # Fallback handled in the endpoint if missing

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
            "album_art": item.get("album", {}).get("images", [{}])[-1].get("url") if item.get("album", {}).get("images") else None
        })
    return {"results": formatted_results}


# --- KEEPING THIS UNTOUCHED FOR YOUR FRONTEND BARS ---
@router.get("/soundchart/features/{track_id}")
def get_track_audio_features(track_id: str):
    try:
        track_data = get_audio_features(track_id, SOUND_CHART_ID, SOUND_CHART_SECRET)
        audio_features = track_data.get("object", {}).get("audio", {})
        return {"audio_features": audio_features}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- NEW STATELESS ART GENERATION ENDPOINT ---
@router.post("/generate-art")
def generate_track_art(payload: AudioFeaturesPayload):
    try:
        # Map features safely, using energy as a fallback for density if Soundcharts doesn't provide it
        target_features = {
            "energy": payload.energy,
            "valence": payload.valence,
            "density": payload.density if payload.density is not None else payload.energy
        }

        # Run genetic algorithm
        best_chromosome = ga_main(target_features, pop_size=15, generations=20)

        # Render the fluid visualization canvas (800x800 presentation size)
        canvas = make_fluid_image(width=800, height=800, chromosome=best_chromosome)

        # Save directly to the mounted static directory
        filename = save_image(canvas, folder=STATIC_DIR)
        base_filename = os.path.basename(filename)
        image_url = f"/static/{base_filename}"

        return {
            "success": True,
            "image_url": image_url,
            "features_used": target_features
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))