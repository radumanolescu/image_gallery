# Deployment Guide

This document covers deploying the modernized image gallery (Django + React)
to a production environment. The current setup is optimized for local
development; the steps below are required before exposing the app beyond
`localhost`.

## Prerequisites

- Python 3.x with `backend/venv` dependencies installed (`pip install -r backend/requirements.txt`)
- Node.js + npm for building the frontend
- The image/media collection in `static/images/`

## 1. Build the frontend

```bash
cd frontend
npm install
npm run build
```

This produces a static bundle in `frontend/dist/`. Serve it with any static
file server or a reverse proxy (nginx, IIS, Caddy). The app expects `/api`
and `/media` to reach the Django backend on the same origin — configure your
proxy accordingly (the Vite dev config shows the mapping).

## 2. Configure the backend environment

Deployment-critical settings are read from environment variables (see
`backend/image_gallery_project/settings.py`). Set these before starting
the server:

| Variable | Required | Description |
|---|---|---|
| `DJANGO_SECRET_KEY` | **Yes** | New random secret key. Never reuse the dev fallback. Generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DJANGO_DEBUG` | **Yes** | Set to `False` in production |
| `DJANGO_ALLOWED_HOSTS` | **Yes** | Comma-separated hostnames, e.g. `gallery.example.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | If cross-origin | Comma-separated origins allowed to POST, e.g. `https://gallery.example.com` |
| `DJANGO_CORS_ORIGINS` | If cross-origin | Comma-separated origins allowed by CORS |

## 3. Database and migrations

```bash
cd backend
venv/Scripts/activate
python manage.py migrate
python manage.py load_metadata          # import TXT metadata (one-time)
python manage.py validate_metadata      # verify the migration
python manage.py createsuperuser        # production admin account
```

SQLite (`backend/db.sqlite3`) is the metadata store. **Back it up regularly** —
a simple file copy while the server is stopped is sufficient for this
collection size.

## 4. Static and media files

```bash
python manage.py collectstatic   # gathers admin/DRF assets into staticfiles/
```

- `STATIC_ROOT` → `backend/staticfiles/` (serve via your web server or WhiteNoise)
- `MEDIA_ROOT` → `static/images/` — the existing image collection; serve at `/media/`

With `DEBUG=False`, Django does **not** serve media files itself; the web
server must handle `/media/` and `/static/` (or add WhiteNoise).

## 5. Run a production server

Use a real WSGI server instead of `manage.py runserver`:

```bash
pip install waitress
waitress-serve --listen=0.0.0.0:8000 image_gallery_project.wsgi:application
```

(gunicorn works the same way on Linux/macOS.)

## 6. Security checklist

- [ ] `DJANGO_DEBUG=False`
- [ ] `DJANGO_SECRET_KEY` set to a fresh value (dev key must never ship)
- [ ] `DJANGO_ALLOWED_HOSTS` restricted to real hostnames
- [ ] `DJANGO_CSRF_TRUSTED_ORIGINS` / `DJANGO_CORS_ORIGINS` restricted
- [ ] New admin password (the dev account `admin`/`admin123` is **not** for production)
- [ ] HTTPS in front of the app (session cookies + CSRF assume it)
- [ ] `backend/db.sqlite3` and `static/images/` excluded from public exposure
- [ ] Regular SQLite backups scheduled

## 7. Smoke test after deploy

1. `GET /api/images/` returns the paginated collection
2. Log in via `/login`, then confirm `GET /api/auth/me/` returns the user
3. Edit one record through the UI and verify the change persists
4. Export CSV/Excel/PDF and open the downloads
5. Run `python manage.py validate_metadata` to confirm DB matches TXT sources
