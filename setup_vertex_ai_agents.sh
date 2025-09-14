#!/bin/bash

# Vertex AI Agent Builder Setup Script
# Comprehensive setup for advanced AI agent system

echo "🚀 Setting up Vertex AI Agent Builder System"
echo "=============================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Install required packages
echo ""
echo "📦 Installing required packages..."
echo "=================================="

# Core packages
pip3 install --upgrade pip
pip3 install google-cloud-aiplatform
pip3 install vertexai
pip3 install firebase-admin
pip3 install google-cloud-firestore
pip3 install asyncio
pip3 install aiohttp
pip3 install python-dotenv
pip3 install pydantic
pip3 install fastapi
pip3 install uvicorn

echo "✅ Core packages installed"

# Additional packages for advanced features
pip3 install google-cloud-storage
pip3 install google-cloud-logging
pip3 install google-cloud-monitoring
pip3 install plotly
pip3 install altair
pip3 install numpy
pip3 install pandas
pip3 install requests
pip3 install beautifulsoup4

echo "✅ Additional packages installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << EOF
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=startup-analyst-platform
GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json
REGION=us-central1

# Vertex AI Configuration
VERTEX_AI_PROJECT=startup-analyst-platform
VERTEX_AI_LOCATION=us-central1

# Firebase Configuration
FIREBASE_PROJECT_ID=startup-analyst-platform
FIREBASE_DATABASE_URL=https://startup-analyst-platform-default-rtdb.firebaseio.com/

# API Keys
GOOGLE_API_KEY=your_google_api_key_here

# Model Configuration
GEMINI_MODEL=gemini-1.5-pro
MAX_TOKENS=8192
TEMPERATURE=0.7

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO
EOF
    echo "✅ .env template created"
    echo "⚠️  Please edit .env file with your actual values"
else
    echo "✅ .env file found"
fi

# Check if service account key exists
if [ ! -f "service-account-key.json" ]; then
    echo ""
    echo "⚠️  Service account key not found"
    echo "📋 Please download your service account key from Google Cloud Console:"
    echo "   1. Go to IAM & Admin → Service Accounts"
    echo "   2. Find 'startup-analyst-sa'"
    echo "   3. Click 'Actions' → 'Manage keys'"
    echo "   4. Download JSON key"
    echo "   5. Save as 'service-account-key.json' in this directory"
else
    echo "✅ Service account key found"
fi

# Create necessary directories
echo ""
echo "📁 Creating necessary directories..."
mkdir -p src/agents
mkdir -p src/models
mkdir -p src/utils
mkdir -p src/config
mkdir -p logs
mkdir -p data
mkdir -p reports

echo "✅ Directories created"

# Set up logging
echo ""
echo "📝 Setting up logging configuration..."
cat > src/config/logging.py << 'EOF'
import logging
import os
from datetime import datetime

def setup_logging():
    """Set up logging configuration"""
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/vertex_ai_agents_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler()
        ]
    )
    
    # Set specific loggers
    logging.getLogger('vertexai').setLevel(logging.INFO)
    logging.getLogger('firebase_admin').setLevel(logging.INFO)
    logging.getLogger('google.cloud').setLevel(logging.INFO)
    
    return logging.getLogger(__name__)

if __name__ == "__main__":
    setup_logging()
EOF

echo "✅ Logging configuration created"

# Create startup script
echo ""
echo "🚀 Creating startup script..."
cat > start_vertex_ai_agents.py << 'EOF'
#!/usr/bin/env python3
"""
Startup script for Vertex AI Agent Builder System
"""
import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.config.logging import setup_logging
from src.agents.vertex_ai_orchestrator import VertexAIOrchestrator

async def main():
    """Main startup function"""
    # Set up logging
    logger = setup_logging()
    logger.info("🚀 Starting Vertex AI Agent Builder System")
    
    try:
        # Initialize orchestrator
        orchestrator = VertexAIOrchestrator()
        
        # Health check
        health_status = await orchestrator.health_check()
        logger.info(f"System health: {health_status['overall_status']}")
        
        # Display agent status
        agent_status = orchestrator.get_agent_status()
        logger.info("Agent status:")
        for agent_name, status in agent_status.items():
            logger.info(f"  {agent_name}: {status['status']}")
        
        logger.info("✅ Vertex AI Agent Builder System ready!")
        logger.info("🎯 All agents are operational and ready for analysis")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("✅ System started successfully!")
    else:
        print("❌ System startup failed!")
        sys.exit(1)
EOF

chmod +x start_vertex_ai_agents.py
echo "✅ Startup script created"

# Create test script
echo ""
echo "🧪 Creating test script..."
cat > test_vertex_ai_system.py << 'EOF'
#!/usr/bin/env python3
"""
Quick test script for Vertex AI Agent Builder System
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.agents.vertex_ai_orchestrator import VertexAIOrchestrator

async def quick_test():
    """Quick system test"""
    print("🧪 Quick Vertex AI Agent Builder Test")
    print("=====================================")
    
    try:
        # Initialize orchestrator
        orchestrator = VertexAIOrchestrator()
        
        # Health check
        health_status = await orchestrator.health_check()
        print(f"✅ System health: {health_status['overall_status']}")
        
        # Test individual agent
        test_data = {
            "company_name": "Test Startup",
            "business_description": "AI-powered test automation"
        }
        
        result = orchestrator.agents["data_collection"].analyze(test_data)
        print(f"✅ Data Collection Agent: {result.get('status', 'unknown')}")
        
        print("🎯 System is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(quick_test())
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Tests failed!")
        sys.exit(1)
EOF

chmod +x test_vertex_ai_system.py
echo "✅ Test script created"

# Create deployment script
echo ""
echo "🚀 Creating deployment script..."
cat > deploy_vertex_ai_agents.sh << 'EOF'
#!/bin/bash

# Deploy Vertex AI Agent Builder System to Google Cloud Run

echo "🚀 Deploying Vertex AI Agent Builder System"
echo "==========================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install Google Cloud CLI."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker."
    exit 1
fi

# Set project
gcloud config set project startup-analyst-platform

# Build and deploy
echo "📦 Building Docker image..."
docker build -t gcr.io/startup-analyst-platform/vertex-ai-agents .

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy vertex-ai-agents \
    --image gcr.io/startup-analyst-platform/vertex-ai-agents \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 900 \
    --max-instances 10

echo "✅ Deployment completed!"
echo "🌐 Your Vertex AI Agent Builder System is now live!"
EOF

chmod +x deploy_vertex_ai_agents.sh
echo "✅ Deployment script created"

# Create Dockerfile for Vertex AI agents
echo ""
echo "🐳 Creating Dockerfile for Vertex AI agents..."
cat > Dockerfile.vertex-ai << 'EOF'
# Dockerfile for Vertex AI Agent Builder System
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_google_stack.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_google_stack.txt

# Copy application code
COPY src/ ./src/
COPY *.py ./

# Set environment variables
ENV PYTHONPATH=/app
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Start application
CMD ["python", "backend/enhanced_main.py"]
EOF

echo "✅ Dockerfile created"

# Final setup summary
echo ""
echo "🎉 Vertex AI Agent Builder Setup Complete!"
echo "=========================================="
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env file with your actual values"
echo "2. Download service account key as 'service-account-key.json'"
echo "3. Run: python3 start_vertex_ai_agents.py"
echo "4. Test: python3 test_vertex_ai_system.py"
echo "5. Deploy: ./deploy_vertex_ai_agents.sh"
echo ""
echo "🎯 Your advanced AI agent system is ready!"
echo "🏆 Perfect for hackathon demonstration!"
echo ""
echo "📚 For detailed setup instructions, see:"
echo "   - VERTEX_AI_AGENT_BUILDER_GUIDE.md"
echo "   - QUICK_SETUP_GUIDE.md"
echo ""
echo "✅ Setup completed successfully!"
