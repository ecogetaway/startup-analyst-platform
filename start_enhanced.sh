#!/bin/bash

# Enhanced Startup Script for Google Tech Stack Demo
echo "🚀 Starting Enhanced Startup Analyst Platform with Google Tech Stack"
echo "=================================================================="

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded"
else
    echo "⚠️ .env file not found - using defaults"
fi

# Check if Python dependencies are installed
echo ""
echo "🔍 Checking Python dependencies..."
if ! python3 -c "import fastapi, uvicorn" 2>/dev/null; then
    echo "📦 Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

# Check if Node.js dependencies are installed
echo ""
echo "🔍 Checking Node.js dependencies..."
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Build React frontend for production
echo ""
echo "🏗️ Building React frontend..."
cd frontend
npm run build
cd ..

# Check Google services status
echo ""
echo "🔍 Google Services Status:"
echo "  GOOGLE_API_KEY: $(if [ -n "$GOOGLE_API_KEY" ]; then echo "✅ Set"; else echo "❌ Missing"; fi)"
echo "  GOOGLE_CLOUD_PROJECT: $(if [ -n "$GOOGLE_CLOUD_PROJECT" ]; then echo "✅ $GOOGLE_CLOUD_PROJECT"; else echo "❌ Missing"; fi)"
echo "  Service Account: $(if [ -f "service-account-key.json" ]; then echo "✅ Found"; else echo "⚠️ Not found (will use demo mode)"; fi)"

echo ""
echo "🌟 Starting Enhanced FastAPI server..."
echo "   Frontend: http://localhost:8080"
echo "   API Docs: http://localhost:8080/docs"
echo "   Health: http://localhost:8080/api/health"
echo "   Status: http://localhost:8080/api/status"
echo ""
echo "🔥 Features:"
echo "   • Firebase Real-time Collaboration"
echo "   • Google Cloud Storage File Uploads"
echo "   • Google ADK Multi-Agent Analysis"
echo "   • Gemini AI Advanced Analysis"
echo "   • Real-time Progress Tracking"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================================================="

# Start the enhanced FastAPI server
python3 -m uvicorn backend.enhanced_main:app --host 0.0.0.0 --port 8080 --reload
