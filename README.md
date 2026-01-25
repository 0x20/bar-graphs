## Bar Graphs

Run in Linux or WSL - ledger filenames contain `:` which Windows doesn't allow.

Requires [tab-data](https://github.com/0x20/tab-data) cloned into this directory.

### Quick Start

```bash
# Start both servers
./dev.sh
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

### Stack

- **Backend**: FastAPI + GitHub OAuth + JWT
- **Frontend**: React 19 + TypeScript + Vite 7 + Recharts
- **Data**: Beancount ledger parsing with pandas

### API

| Endpoint | Auth | Description |
|----------|------|-------------|
| `GET /health` | No | Health check |
| `GET /auth/login` | No | Redirect to GitHub OAuth |
| `GET /auth/callback?code=` | No | Exchange code for JWT |
| `GET /api/debtors` | Yes | List users with negative balances |

### Config

Edit `backend/.env`:

```env
GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx
JWT_SECRET=xxx
ALLOWED_USERS=user1,user2
FRONTEND_URL=http://localhost:5173
TAB_DATA_PATH=../tab-data
```

Create GitHub OAuth App at https://github.com/settings/developers with callback `http://localhost:5173/auth/callback`

### Requirements

- Python 3.11+
- Node.js 20+ (`nvm use 20`)
