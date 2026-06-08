"""
main.py

Main entry point for the Genetic Algorithm for Abstract Art.
Orchestrates feature extraction, GA evolution, rendering, and visualization.
"""

import sys
import os

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.api.endpoints import router as api_router
from backend.src.genetic_algorithm import ga_main
from backend.src.render import make_fluid_image, save_image
from backend.src.fitness import calculate_fitness

"""
   Main workflow:
   1. Extract emotional features from MIDI
   2. Run genetic algorithm to evolve best chromosome
   3. Render final image
   4. Save output
   """
load_dotenv()
app = FastAPI(title="Genetic Algorithm Art Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your React frontend to communicate with this server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")
app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8080, reload=True)