# Image Gallery Frontend

React + TypeScript + Vite + Material-UI frontend for the image gallery application. Talks to the Django REST API in `../backend/`.

## Running

```bash
# Terminal 1: Django backend (port 8000)
cd backend
venv/Scripts/activate
python manage.py runserver

# Terminal 2: React frontend (port 5173)
cd frontend
npm install   # first time only
npm run dev
```

Open http://localhost:5173/

The Vite dev server proxies `/api` and `/media` to `localhost:8000`, so
session cookies and CSRF work without CORS issues. Always use `localhost`
(not `127.0.0.1`) for both servers so cookies stay same-site.

## Features

- **Gallery grid** — card-based image grid with lazy-loaded thumbnails
- **Search** — debounced full-text search across titles, keywords, medium, location
- **Filtering** — dropdowns for medium, location, gallery, orientation, substrate, inventory status
- **Sorting** — sort by file name, date, title, price, etc. (asc/desc)
- **Pagination** — 20 items per page
- **Lightbox** — click an image to open the preview gallery with zoom and a metadata strip
- **Edit metadata** — per-image edit dialog with all fields grouped by section
- **Bulk edit** — select multiple images and apply a field update to all
- **Bulk import** — upload CSV/Excel to create/update records
- **Export** — download the current filtered view as CSV, Excel, or PDF
- **Login** — session auth; read-only for anonymous users, editing requires login

## Project Structure

```
src/
├── api/
│   ├── client.ts          # axios instance + CSRF/session handling
│   ├── auth.ts            # login/logout/me
│   ├── images.ts          # CRUD, bulk ops, export URLs
│   └── types.ts           # TypeScript types mirroring the API
├── components/
│   ├── SearchBar.tsx      # search + sort controls
│   ├── FilterPanel.tsx    # collapsible filter dropdowns
│   ├── ImageCard.tsx      # single image card
│   ├── ImageGrid.tsx      # responsive card grid
│   ├── ImageLightbox.tsx  # preview gallery (yet-another-react-lightbox)
│   ├── EditMetadataDialog.tsx
│   ├── BulkEditDialog.tsx
│   ├── ImportDialog.tsx
│   └── ExportMenu.tsx
├── hooks/
│   └── useAuth.tsx        # auth context provider + hook
├── pages/
│   ├── GalleryPage.tsx    # main view
│   └── LoginPage.tsx
├── App.tsx                # router + theme
└── theme.ts               # MUI theme
```

## Commands

```bash
npm run dev      # dev server on :5173
npm run build    # type-check (tsc) + production build to dist/
npm run lint     # oxlint
npm run preview  # serve the production build
```

## Notes

- Write operations require login (Django session auth); reads are public.
- The CSRF token is fetched lazily via `GET /api/auth/csrf/` and sent as
  `X-CSRFToken` on every mutating request.
- `bulk_import` accepts `.csv`, `.xlsx`, `.xls`; column names are normalized
  (lowercase, underscores) and matched to model fields.
- PDF export is capped at 50 records on the backend.
