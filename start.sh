#!/bin/bash

# Startup Analyst Platform - Development Server
echo "🚀 Starting Startup Analyst Platform..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your Google API key"
    echo "   export GOOGLE_API_KEY='your-api-key-here'"
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if Google API key is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "❌ GOOGLE_API_KEY not set in .env file"
    echo "   Please add your Google API key to the .env file"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Build React frontend
echo "🏗️  Building React frontend..."
cd frontend
npm install
npm run build
cd ..

# Start the FastAPI server
echo "🌟 Starting FastAPI server..."
echo "   Frontend: http://localhost:8080"
echo "   API Docs: http://localhost:8080/docs"
echo "   Health: http://localhost:8080/api/health"

python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8080 --reload
