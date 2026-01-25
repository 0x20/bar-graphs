# Backend

FastAPI server with GitHub OAuth.

## Files

```
backend/
├── main.py           # App entry point, CORS setup, mounts routers
├── config.py         # Loads env vars into Settings class
├── auth.py           # GitHub OAuth flow + JWT create/validate
├── dependencies.py   # get_current_user() auth middleware
├── routers/
│   ├── auth.py       # /auth/login, /auth/callback endpoints
│   └── debtors.py    # /api/debtors endpoint (reads beancount data)
├── .env              # Your secrets (gitignored)
├── .env.example      # Template for .env
└── requirements.txt  # Python dependencies
```

## Run

```bash
source ../venv/bin/activate
uvicorn main:app --reload --port 8000
```
