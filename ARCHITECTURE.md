# Architecture

## System Overview

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       │ :80
       ▼
┌─────────────┐
│   Nginx     │  (Frontend container)
│  - Serves   │  - React SPA
│    React    │  - Proxies /api/* and /auth/* to backend
│  - Proxy    │
└──────┬──────┘
       │
       │ internal network
       ▼
┌─────────────┐
│   FastAPI   │  (Backend container)
│  - Auth     │  - GitHub OAuth
│  - API      │  - JWT tokens
│  - Data     │  - Beancount parsing
└─────────────┘
       │
       │ volume mount (read-only)
       ▼
┌─────────────┐
│  tab-data   │  (Local directory)
│  - Ledgers  │  - Beancount files
│  - History  │
└─────────────┘
```

## Components

### Frontend Container
- **Base**: `nginx:alpine`
- **Build**: Multi-stage (Node 20 build → Nginx serve)
- **Port**: 80
- **Serves**: Optimized production React build
- **Routing**: SPA routing with nginx fallback to index.html
- **Proxy**: Routes `/api/*` and `/auth/*` to backend container

### Backend Container
- **Base**: `python:3.11-slim`
- **Framework**: FastAPI with Uvicorn
- **Port**: 8000
- **Auth**: GitHub OAuth + JWT tokens
- **Data**: Beancount ledger parsing with pandas
- **Volume**: Read-only mount of `tab-data/`

### Data Flow

1. **User visits** http://localhost → Nginx serves React SPA
2. **User clicks login** → React redirects to `/auth/login`
3. **Nginx proxies** `/auth/*` → Backend FastAPI
4. **Backend redirects** to GitHub OAuth
5. **GitHub callback** → Backend validates, creates JWT
6. **Frontend stores** JWT in localStorage
7. **API requests** include JWT in Authorization header
8. **Nginx proxies** `/api/*` → Backend (with JWT)
9. **Backend validates** JWT, reads beancount data, returns JSON
10. **React renders** charts from API response

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Beancount** - Ledger parsing
- **Pandas** - Data processing
- **PyJWT** - Token generation/validation
- **httpx** - GitHub API calls

### Frontend
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite 7** - Build tool & dev server
- **Recharts** - Chart library
- **React Router** - Client-side routing

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Static file serving & reverse proxy

## File Structure

```
bar-graphs/
├── backend/
│   ├── main.py           # FastAPI app entry
│   ├── config.py         # Settings from env vars
│   ├── auth.py           # OAuth + JWT logic
│   ├── dependencies.py   # Auth middleware
│   ├── routers/
│   │   ├── auth.py       # /auth endpoints
│   │   └── debtors.py    # /api/debtors endpoint
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── main.tsx      # Entry point
│   │   ├── App.tsx       # Router setup
│   │   ├── auth.tsx      # Auth context
│   │   ├── api.ts        # API client
│   │   ├── pages/        # Route components
│   │   └── components/   # Reusable UI
│   ├── package.json
│   └── vite.config.ts
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── nginx.conf
└── .env
```

## Security

- **OAuth**: GitHub as identity provider
- **JWT**: Stateless authentication
- **CORS**: Configured for frontend origin
- **Secrets**: Environment variables (not in git)
- **User whitelist**: `ALLOWED_USERS` env var
- **Read-only**: tab-data mounted read-only

## Development vs Production

### Development (dev.sh)
- Backend: Uvicorn with `--reload`
- Frontend: Vite dev server with HMR
- Ports: 8000 (backend), 5173 (frontend)

### Production (Docker)
- Backend: Uvicorn without reload
- Frontend: Nginx serving optimized build
- Ports: 8000 (backend), 80 (frontend)
- Single network for inter-container communication
