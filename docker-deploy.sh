#!/bin/bash
# Docker deployment helper script

set -e

echo "Bar Graphs - Docker Deployment"
echo "==============================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "Warning: .env not found. Creating from template..."
    cp .env.docker.example .env
    echo ""
    echo "Please edit .env with your credentials before deploying:"
    echo "  - GITHUB_CLIENT_ID"
    echo "  - GITHUB_CLIENT_SECRET"
    echo "  - JWT_SECRET (generate with: openssl rand -hex 32)"
    echo "  - ALLOWED_USERS"
    echo "  - FRONTEND_URL"
    echo ""
    echo "After configuring, run this script again."
    exit 1
fi

# Check if tab-data exists
if [ ! -d tab-data ]; then
    echo "Error: tab-data directory not found."
    echo "Please clone tab-data into this directory:"
    echo "  git clone https://github.com/0x20/tab-data"
    exit 1
fi

echo "Building Docker images..."
docker-compose build

echo ""
echo "Starting containers..."
docker-compose up -d

echo ""
echo "Deployment complete!"
echo ""
echo "Frontend: http://localhost"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "View logs:  docker-compose logs -f"
echo "Stop:       docker-compose down"
echo ""
