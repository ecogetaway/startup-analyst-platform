#!/bin/bash

echo "🚀 Setting up Startup Analyst Platform..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup Python backend
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Setup React frontend
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads
mkdir -p logs

# Set permissions
chmod +x simple_demo_backend.py

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "1. Backend:  python3 simple_demo_backend.py"
echo "2. Frontend: cd frontend && npm start"
echo ""
echo "📱 Access the app at: http://localhost:3000"
echo "📚 API docs at: http://localhost:8080/docs"
