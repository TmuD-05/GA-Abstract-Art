# Genova

**Genova turns a song into a one-of-a-kind piece of generative art.**

<img width="1283" height="807" alt="Screenshot 2026-07-01 at 6 20 49 AM" src="https://github.com/user-attachments/assets/16af0aa3-a0bc-4fdc-bfe2-244667aa624c" />

<img width="1173" height="765" alt="Screenshot 2026-07-01 at 6 21 17 AM" src="https://github.com/user-attachments/assets/82240988-6d94-43d5-8997-df1c31b8f466" />

<img width="1125" height="713" alt="Screenshot 2026-07-01 at 6 23 52 AM" src="https://github.com/user-attachments/assets/09090169-ad94-4497-830a-e7dd1b492bb7" />


Search for a track, pull its audio characteristics (energy, valence, tempo), and watch a genetic algorithm evolve a fluid, noise-based image whose colour palette, turbulence, and detail level are shaped by the music. The whole thing is wrapped in a Windows 98 × dark-gallery interface — part retro desktop app, part exhibition wall.

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Roadmap](#roadmap)

---

## Overview

1. **Search** for a track (Spotify search API).
2. **Extract features** — energy, valence, tempo/density — via Soundcharts.
3. **Evolve** — a genetic algorithm evolves a population of "chromosomes" (visual parameters: palette, scale, octaves, warp strength, persistence, noise seeds) to best match the target musical features.
4. **Render** — the winning chromosome is rendered into an 800×800 image using layered OpenSimplex noise with domain warping, producing a fluid, painterly composition.
5. **Exhibit** — the result is displayed in an ornate frame inside a Windows-98-styled gallery UI.

## How It Works

### Feature extraction

`midi_processor.py` handles two integrations:
- **Spotify** — client-credentials OAuth flow (`get_spotify_access_token`) and track search (`search_spotify_track`), used to find candidate tracks and their artwork.
- **Soundcharts** — `get_audio_features` fetches audio characteristics (energy, valence, etc.) for a track by Spotify ID.

### Chromosome design

Each "chromosome" (`chromosome.py`) is a dict of visual genes derived from the target musical features:

| Gene | Driven by | Effect |
|---|---|---|
| `palette_id` | `valence`, `energy` | Colour mood — cool/dark for low valence, warm/bright or neon for high valence + energy |
| `scale` | `energy` | Size of noise features — larger scale = coarser, calmer shapes |
| `octaves` | `density` | Layers of fractal noise — more octaves = more intricate detail |
| `persistence` | random | How quickly each octave's amplitude decays |
| `warp_strength` | `energy` | Intensity of the fluid domain-warping distortion |
| `seed_x`, `seed_y` | random | Uniqueness — same features can still produce different-looking pieces |

### Genetic algorithm

`genetic_algorithm.py` runs a standard GA loop over a population of chromosomes:

- **Population** initialised with `create_population`, biased toward the target features via `chromosome.py`'s heuristics.
- **Selection** via tournament selection (`tournament_selection`, `k=3`).
- **Crossover & mutation** (`src/ga/crossover.py`, `src/ga/mutation.py`).
- **Elitism** — the best chromosome from each generation is always carried forward.
- **Fitness** (`fitness.py`) scores a chromosome against the target features across four weighted components — palette (0.4), scale (0.2), warp (0.2), octaves (0.2) — each scored by how close it lands to an "ideal" value range derived from the target energy/valence/density.

`ga_main(target_features, pop_size, generations)` returns the fittest chromosome after evolving.

### Rendering

`render.py` converts the winning chromosome into an image:
- For every pixel, layered OpenSimplex noise (`opensimplex.noise2`) is summed across `octaves` to compute a warp offset, which displaces the sampling coordinates (domain warping) before a second noise pass determines the final colour value.
- The resulting scalar is mapped to a colour by interpolating across the chosen palette (`palettes.py` — 25 hand-tuned BGR palettes grouped from cool/dark → neutral → warm/bright → neon/intense).
- The final canvas is saved as a PNG and served statically by the FastAPI app.

### Frontend

A Windows-98-styled single page app (`App.tsx`) that:
- Lets the user search for and select a track (`SearchBar.tsx`, debounced live search with keyboard navigation).
- Displays track info in a retro "groupbox" panel.
- Triggers artwork generation and shows a loading state while the GA + renderer run server-side.
- Presents the finished piece in an ornate frame with a museum-style placard (title, artist, year).

## Tech Stack

**Frontend**
- React + TypeScript (Vite)
- Axios for API calls
- Hand-rolled Windows 98 UI kit (`App.css`)

**Backend**
- FastAPI (Python)
- OpenCV + NumPy for image construction
- OpenSimplex for noise generation
- Custom genetic algorithm (selection, crossover, mutation, elitism)

**External APIs**
- Spotify Web API (search, client-credentials auth)
- Soundcharts API (audio feature data)

## Project Structure

```
genova/
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app, CORS, static mount
│   │   ├── api/
│   │   │   └── endpoints.py      # /spotify/search, /soundchart/features, /generate-art
│   │   └── static/               # generated PNGs served here
│   └── src/
│       ├── midi_processor.py     # Spotify + Soundcharts API clients
│       ├── chromosome.py         # gene definitions & feature-driven heuristics
│       ├── genetic_algorithm.py  # GA main loop, selection
│       ├── fitness.py            # fitness scoring
│       ├── palettes.py           # 25 colour palettes
│       ├── render.py             # noise-based rendering + save/show
│       └── ga/
│           ├── crossover.py
│           └── mutation.py
└── frontend/
    └── src/
        ├── main.tsx
        ├── App.tsx                # main layout / gallery view
        ├── App.css                # Windows 98 theming
        ├── index.css
        └── components/
            ├── SearchBar.tsx      # live track search + dropdown
            └── MusicMetrix.tsx    # raw audio-feature display panel
```

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Spotify Developer app (Client ID/Secret)
- Soundcharts API credentials

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install fastapi uvicorn python-dotenv requests opencv-python numpy opensimplex

# create a .env file — see Environment Variables below

python -m app.main
# or: uvicorn backend.app.main:app --reload --port 8080
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the backend at `http://localhost:8080`.

## Environment Variables

Create a `.env` file in `backend/`:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SOUND_CHART_ID=your_soundcharts_app_id
SOUND_CHART_TOKEN=your_soundcharts_api_key
```

> ⚠️ Note: the Soundcharts client currently reads its token from `SOUND_CHART_TOKEN`, so make sure the variable name matches exactly — a common source of silent auth failures.

## API Reference

All routes are mounted under `/api/v1`.

| Method | Route | Description |
|---|---|---|
| `GET` | `/spotify/search?track_title=...` | Search Spotify for tracks; returns id, title, artist, and album art (full + thumbnail) |
| `GET` | `/soundchart/features/{track_id}` | Fetch audio features (energy, valence, etc.) for a track by Spotify ID |
| `POST` | `/generate-art` | Run the GA + renderer for a given `{energy, valence, density?}` payload; returns the generated image URL |

Generated images are served statically from `/static/{filename}`.

## Roadmap

- [ ] Swap the full GA search for a faster/direct feature-to-chromosome mapping for near-instant generation
- [ ] Persist generated pieces + metadata (gallery history)
- [ ] Deploy frontend + backend for public demo access
- [ ] Expand palette set / user-selectable mood overrides
- [ ] Unit tests for fitness scoring and chromosome heuristics

---

*Genova began as a MIDI-driven "Synesthesia Engine" school project and has since evolved into a Spotify/Soundcharts-integrated web app with a genetic-algorithm art engine.*
