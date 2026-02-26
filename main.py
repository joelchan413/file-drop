"""File Drop — lightweight photo transfer server."""

import time
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="File Drop")

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".heic", ".heif"}

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


def _resolve_upload(filename: str) -> Path:
    """Resolve filename inside UPLOAD_DIR and block path traversal."""
    candidate = (UPLOAD_DIR / filename).resolve()
    upload_root = UPLOAD_DIR.resolve()
    if upload_root not in candidate.parents and candidate != upload_root:
        raise HTTPException(status_code=400, detail="Invalid filename.")
    if not candidate.is_file():
        raise HTTPException(status_code=404, detail="File not found.")
    return candidate


@app.get("/uploads")
async def list_uploads():
    """List uploaded image files, newest first."""
    files = []
    for file_path in UPLOAD_DIR.glob("*"):
        if not file_path.is_file() or file_path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        stat = file_path.stat()
        files.append(
            {
                "filename": file_path.name,
                "size": stat.st_size,
                "modified": int(stat.st_mtime),
                "url": f"/uploads/{file_path.name}",
                "download_url": f"/downloads/{file_path.name}",
            }
        )

    files.sort(key=lambda item: item["modified"], reverse=True)
    return {"files": files}


@app.get("/uploads/{filename}")
async def serve_upload(filename: str):
    """Serve uploaded file for preview/display."""
    path = _resolve_upload(filename)
    return FileResponse(path)


@app.get("/downloads/{filename}")
async def download_upload(filename: str):
    """Serve uploaded file as an attachment download."""
    path = _resolve_upload(filename)
    return FileResponse(path, filename=path.name)
