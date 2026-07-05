#!/bin/bash

echo "🚀 Starting Portfolio Agent..."

# Start FastAPI backend
echo "📡 Starting API server on port 8000..."
python3 api/main.py &
API_PID=$!

# Wait for API to start
sleep 2

# Start Next.js frontend
echo "🖥️  Starting frontend on port 3000..."
cd frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers started!"
echo "   Frontend: http://localhost:3000"
echo "   API:      http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $API_PID $FRONTEND_PID; exit" SIGINT SIGTERM
wait
