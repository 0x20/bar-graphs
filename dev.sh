#!/bin/bash
# Development server startup script

cd /home/mateo/projects/bar-graphs

# Kill existing processes
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 1

# Start backend
echo "Starting backend on http://localhost:8000..."
source venv/bin/activate
cd backend
uvicorn main:app --reload --port 8000 &
cd ..

# Start frontend
echo "Starting frontend on http://localhost:5173..."
cd frontend
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 20 2>/dev/null
npm run dev &
cd ..

sleep 3
echo ""
echo "=== Servers running ==="
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop (or run: pkill -f uvicorn; pkill -f vite)"
wait
