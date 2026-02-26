# 📸 File Drop

A lightweight, self-hosted web app for quickly transferring photos from your phone to your computer. Open the page on your mobile browser, tap to select photos, and they land on your desktop — no cloud, no cables, no accounts.

![File Drop UI](https://img.shields.io/badge/dark_mode-mobile_first-6c63ff?style=for-the-badge)

## Features

- **Instant transfers** — photos arrive on your computer in seconds
- **Multi-file upload** — select or drag multiple photos at once
- **Real progress bars** — per-file percentage with thumbnail previews
- **Instant access to uploads** — view, copy, or download uploaded photos from the app
- **Built-in quick editor** — add text, boxes, freehand drawing, highlights, and crop before sharing
- **Drag & drop** — works on desktop browsers too
- **No accounts, no cloud** — everything stays on your local network
- **Dark mode** — clean, mobile-optimized UI

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI, Uvicorn |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Deployment | Docker, Docker Compose |

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)

### Run

```bash
git clone https://github.com/joelchan413/file-drop.git
cd file-drop
docker compose up -d --build
```

The app is now running at **https://localhost:8000**.

To access it from your phone, open `https://<your-pc-ip>:8000` (both devices must be on the same network).

### HTTPS (for clipboard image copy)

The container now starts with HTTPS enabled and auto-generates a self-signed certificate on first run.

- Local access: `https://localhost:8000`
- LAN access: `https://<your-pc-ip>:8000`

If you want the cert to include your LAN IP/hostname (recommended for fewer browser warnings), set `SSL_EXTRA_SANS` in `docker-compose.yml`, then recreate:

```bash
docker compose down
docker compose up -d --build
```

> Browsers may still show a one-time warning for self-signed certificates until you trust the cert on your device.

### Where Do My Photos Go?

Uploaded photos are saved to the `./received_photos/` directory on your host machine. Each file is automatically prefixed with a Unix timestamp to prevent collisions.

```
received_photos/
├── 1709000001234_IMG_0042.jpg
├── 1709000005678_IMG_0043.jpg
└── 1709000009012_sunset.png
```

## Configuration

| Setting | Default | How to Change |
|---------|---------|---------------|
| Port | `8000` | Edit `ports` in `docker-compose.yml` |
| Upload directory | `./received_photos` | Edit `volumes` in `docker-compose.yml` |

## Project Structure

```
file-drop/
├── main.py              # FastAPI backend
├── static/
│   └── index.html       # Frontend UI
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container image
├── docker-compose.yml   # Orchestration + volume mount
└── README.md
```

## Development

Run locally without Docker:

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

> **Note:** When running outside Docker, files are saved to `/app/uploads` by default. You may want to adjust the `UPLOAD_DIR` path in `main.py` for local development.

## License

[MIT](LICENSE)
