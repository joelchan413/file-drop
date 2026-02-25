"""File Drop — lightweight photo transfer server."""

import time
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="File Drop")

# Serve static assets (CSS, JS, etc.) from /static path
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Serve the main upload page."""
    return FileResponse("static/index.html")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Accept an uploaded file, timestamp-prefix it, and save to disk."""
    if not file.filename:
        return JSONResponse(
            status_code=400,
            content={"detail": "No filename provided."},
        )

    # Build a collision-free filename: <unix_ms>_<original_name>
    timestamp = int(time.time() * 1000)
    stem = Path(file.filename).stem
    suffix = Path(file.filename).suffix
    safe_name = f"{timestamp}_{stem}{suffix}"

    dest = UPLOAD_DIR / safe_name
    contents = await file.read()
    dest.write_bytes(contents)

    return {"filename": safe_name, "size": len(contents)}
