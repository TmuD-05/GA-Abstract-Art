from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from backend.src.midi_processor import get_spotify_access_token, search_spotify_track, get_audio_features
from backend.src.genetic_algorithm import ga_main
from backend.src.render import make_fluid_image, save_image
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import os
import cv2
import base64
import asyncio

from backend.src.midi_processor import get_spotify_access_token, search_spotify_track, get_audio_features
from backend.src.genetic_algorithm import ga_main, find_best,create_population
# from backend.src.chromosome import create_population
from backend.src.fitness import calculate_fitness
from backend.src.render import make_fluid_image, save_image

router = APIRouter()
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

        return {"audio_features": track_data}
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
@router.websocket("/ws/generate-art")
async def websocket_generate_art(websocket: WebSocket):
    await websocket.accept()
    try:
        # Receive target configurations from frontend client
        data = await websocket.receive_json()
        target_features = {
            "energy": float(data.get("energy", 0.5)),
            "valence": float(data.get("valence", 0.5)),
            "density": float(data.get("density", 0.5))
        }

        # Step 1: Run GA generations manually to catch intermediate steps
        pop_size = 15
        generations = 20
        TOURNAMENT_K = 3

        # Pull internal building blocks to step through generation frames manually
        from backend.src.genetic_algorithm import tournament_selection, crossover, mutation

        population = create_population(pop_size, target_features)
        best_ever = find_best(population, target_features)

        for generation in range(generations):
            new_population = []
            best = find_best(population, target_features)
            new_population.append(best)

            while len(new_population) < pop_size:
                p1 = tournament_selection(population, target_features, TOURNAMENT_K)
                p2 = tournament_selection(population, target_features, TOURNAMENT_K)
                child = crossover(p1, p2)
                child = mutation(child)
                new_population.append(child)

            new_best = find_best(new_population, target_features)
            if calculate_fitness(new_best, target_features) > calculate_fitness(best_ever, target_features):
                best_ever = new_best

            population = new_population

            # Step 2: Render a quick visual intermediate frame of the current best chromosome
            # Lower generation rendering canvas slightly to optimize pipe transmission speed
            preview_canvas = make_fluid_image(width=400, height=400, chromosome=best_ever)

            # Encode frame to memory buffer as PNG format, then convert to base64 text string
            _, buffer = cv2.imencode('.png', preview_canvas)
            b64_string = base64.b64encode(buffer).decode('utf-8')

            # Broadcast continuous string frame down the pipeline
            await websocket.send_json({
                "type": "generation_frame",
                "generation": generation + 1,
                "total_generations": generations,
                "frame": f"data:image/png;base64,{b64_string}"
            })

            # Tiny async break to let the socket buffer flush smoothly
            await asyncio.sleep(0.05)

        # Step 3: Generation complete. Build high-quality presentation canvas
        final_canvas = make_fluid_image(width=800, height=800, chromosome=best_ever)
        STATIC_DIR = "backend/app/static"
        filename = save_image(final_canvas, folder=STATIC_DIR)
        base_filename = os.path.basename(filename)

        # Send final resolution asset location path pointers
        await websocket.send_json({
            "type": "final_result",
            "image_url": f"/static/{base_filename}"
        })

    except WebSocketDisconnect:
        print("Frontend closed connection before generation cycle completed.")
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})