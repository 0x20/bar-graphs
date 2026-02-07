# Bar Graphs

Run in Linux or WSL - ledger filenames contain `:` which Windows doesn't allow.

Requires [tab-data](https://github.com/0x20/tab-data) cloned into this directory.

## Quick Start

### Docker (Recommended)

```bash
# 1. Copy environment template
cp .env.docker.example .env

# 2. Edit .env with your credentials
nano .env  # or your preferred editor

# 3. Deploy
./docker-deploy.sh
```

Access at:
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Local Development

```bash
# Option 1: Start both servers at once
./dev.sh

# Option 2: Run individually
# Backend (Terminal 1)
source venv/bin/activate
cd backend
uvicorn main:app --reload --port 8000

# Frontend (Terminal 2)
cd frontend
nvm use 20
npm run dev
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

## Configuration

### GitHub OAuth Setup

1. Go to https://github.com/settings/developers
2. Click "New OAuth App"
3. Fill in:
   - **Application name**: Bar Graphs (or your choice)
   - **Homepage URL**: `http://localhost` (or your domain)
   - **Authorization callback URL**: `http://localhost/auth/callback` (or your domain)
4. Click "Register application"
5. Copy the **Client ID** and **Client Secret** to your `.env` file

### Environment Variables

For Docker, edit `.env`:

```bash
# GitHub OAuth App (create at https://github.com/settings/developers)
GITHUB_CLIENT_ID=your_github_oauth_app_client_id
GITHUB_CLIENT_SECRET=your_github_oauth_app_client_secret

# JWT Secret (generate with: openssl rand -hex 32)
JWT_SECRET=your_long_random_secret_key_here

# Allowed GitHub usernames (comma-separated)
ALLOWED_USERS=username1,username2,username3

# Frontend URL (adjust for your domain)
FRONTEND_URL=http://localhost              # Local development
# FRONTEND_URL=https://yourdomain.com      # Production
```

For local dev, edit `backend/.env`:

```env
GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx
JWT_SECRET=xxx
ALLOWED_USERS=user1,user2
FRONTEND_URL=http://localhost:5173
TAB_DATA_PATH=../tab-data
```

## Docker Commands

```bash
# Start containers
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop containers
docker-compose down

# Rebuild after code changes
docker-compose build && docker-compose up -d

# Remove everything (including volumes)
docker-compose down -v
```

## Tech Stack

- **Backend**: FastAPI + GitHub OAuth + JWT
- **Frontend**: React 19 + TypeScript + Vite 7 + Recharts
- **Data**: Beancount ledger parsing with pandas
- **Infrastructure**: Docker + Nginx

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system architecture.

## API Endpoints

| Endpoint | Auth | Description |
|----------|------|-------------|
| `GET /health` | No | Health check |
| `GET /auth/login` | No | Redirect to GitHub OAuth |
| `GET /auth/callback?code=` | No | Exchange code for JWT |
| `GET /api/debtors` | Yes | List users with negative balances |

## Production Deployment

For production:

1. **Update `.env`**:
   ```bash
   FRONTEND_URL=https://yourdomain.com
   VITE_API_URL=https://api.yourdomain.com  # Optional
   ```

2. **Use HTTPS**: Set up nginx or reverse proxy with SSL certificates

3. **Update GitHub OAuth**: Set callback URL to your production domain

4. **Secure secrets**: Use strong, randomly generated values for `JWT_SECRET`

5. **Update ports** in `docker-compose.yml` if needed

## Setup for Local Development

**Requirements:**
- Python 3.11+
- Node.js 20+ (`nvm use 20`)

**Installation:**
```bash
# Backend dependencies
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Frontend dependencies
cd frontend && npm install && cd ..

# Configure backend
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials
```

## Troubleshooting

### Docker containers won't start

```bash
# Check logs
docker-compose logs

# Check if ports are in use
sudo lsof -i :80
sudo lsof -i :8000
```

### Environment variables not loading

Ensure `.env` file exists in the project root and contains all required variables.

### tab-data not found

The backend requires the tab-data directory:
```bash
git clone https://github.com/0x20/tab-data
```

### Permission errors

Ensure Docker has permission to mount the tab-data directory:
```bash
ls -la tab-data/
```
