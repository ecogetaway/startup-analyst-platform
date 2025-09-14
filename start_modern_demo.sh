#!/bin/bash

# Modern Demo Startup Script - VenturusAI Inspired Design
echo "🎨 Starting Modern Startup Analyst Platform"
echo "=========================================================="
echo "🎯 VenturusAI-Inspired Design with Multi-Modal Capabilities"
echo "=========================================================="

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
echo "🏗️ Building Modern React Frontend..."
echo "   🎨 VenturusAI-inspired design"
echo "   📱 Multi-modal upload interface"
echo "   🔄 Real-time progress tracking"
echo "   📊 Professional results display"
cd frontend
npm run build
cd ..

# Display feature overview
echo ""
echo "🚀 Modern Platform Features:"
echo "   ✅ VenturusAI-inspired landing page"
echo "   ✅ Multi-modal file upload (docs, audio, video)"
echo "   ✅ Real-time AI analysis progress"
echo "   ✅ Professional investment memo generation"
echo "   ✅ Tabbed results interface"
echo "   ✅ Modern gradient design"

# Check Google services status
echo ""
echo "🔍 Google Tech Stack Status:"
echo "  GOOGLE_API_KEY: $(if [ -n "$GOOGLE_API_KEY" ]; then echo "✅ Set"; else echo "❌ Missing"; fi)"
echo "  GOOGLE_CLOUD_PROJECT: $(if [ -n "$GOOGLE_CLOUD_PROJECT" ]; then echo "✅ $GOOGLE_CLOUD_PROJECT"; else echo "❌ Missing"; fi)"
echo "  Multi-Modal Processing: ✅ Ready"
echo "  Deal Memo Generation: ✅ Ready"

echo ""
echo "🌟 Starting Enhanced FastAPI Server with Modern Frontend..."
echo "   🎨 Modern UI: http://localhost:8080"
echo "   📋 API Docs: http://localhost:8080/docs"
echo "   🔧 Health: http://localhost:8080/api/health"
echo "   📊 Status: http://localhost:8080/api/status"
echo ""
echo "🎯 New Capabilities:"
echo "   🎬 Multi-Modal Pitch Ingestion"
echo "   🎤 Voice Note Analysis"
echo "   🎥 Video Pitch Processing"
echo "   📝 Automated Deal Memo Generation"
echo "   🎨 VenturusAI-Inspired Professional Design"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================================="

# Start the enhanced FastAPI server with modern frontend
python3 -m uvicorn backend.enhanced_main:app --host 0.0.0.0 --port 8080 --reload
