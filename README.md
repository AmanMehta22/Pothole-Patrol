# Pothole-Patrol
**Pothole Patrol** is a smart road monitoring system using IoT and web technologies. It detects potholes through sensors, records their GPS coordinates, and displays them on a web map. Built with Flask, database, and mapping API, it helps authorities monitor and repair roads efficiently, supporting smart city development.

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000 (Windows: gunicorn is not used locally; it is Linux-only for the live deployment.)

## Deploying to a Python Host (Render, Railway, Fly.io, etc.)
This is a server-side Flask app — it must be deployed to a service that runs Python.
**Do not use GitHub Pages for this repo**: Pages only serves static files and renders
this README when there is no root `index.html`. It cannot execute Flask.

- **Render**: Repo → New → Blueprint → it reads `render.yaml` (build: `pip install -r requirements.txt`, start: `gunicorn app:app --bind 0.0.0.0:$PORT`).
- **Railway / Heroku**: They use the `Procfile` automatically.
- **Docker-capable hosts** (Fly.io, Cloud Run, Azure, Koyeb): build from the included `Dockerfile`.

Notes for live deployments:
- `app.py` reads the `PORT` environment variable and binds `0.0.0.0`, as most hosts require.
- SQLite (`database.db`) and `static/uploads/` are part of the repo for demo data; uploads written at runtime are ephemeral on free plans and reset on redeploy.
