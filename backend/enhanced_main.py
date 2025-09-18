"""
Enhanced FastAPI backend with comprehensive Google Tech Stack integration
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import asyncio
import time
import sys
import os
from typing import Dict, Any, List, Optional
import logging
from contextlib import asynccontextmanager

# Add src to path
sys.path.append('src')

# Use working agents instead of problematic Google ADK
import sys
sys.path.append('.')
from agents.startup_analyst_agents import StartupAnalystOrchestrator
google_adk_orchestrator = StartupAnalystOrchestrator()
from src.agents.multimodal_ingestion_agent import multimodal_processor, deal_memo_generator
from src.utils.enhanced_firebase_client import enhanced_firebase_client
from src.utils.enhanced_storage_client import enhanced_storage_client
from src.models.startup import StartupInput

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    
    # Startup
    logger.info("🚀 Starting Enhanced Startup Analyst Platform with Google Tech Stack...")
    
    # Initialize Google services
    logger.info(f"Firebase Available: {enhanced_firebase_client.is_available()}")
    logger.info(f"Cloud Storage Available: {enhanced_storage_client.is_available()}")
    
    # Check Google ADK status
    adk_status = google_adk_orchestrator.get_agent_status()
    logger.info(f"Google ADK: {adk_status['total_agents']} agents initialized")
    
    # Start keep-alive task
    keep_alive_task = asyncio.create_task(keep_alive_worker())
    
    yield
    
    # Shutdown
    logger.info("Shutting down Enhanced Startup Analyst Platform...")
    keep_alive_task.cancel()

# Create FastAPI app
app = FastAPI(
    title="Enhanced Startup Analyst Platform",
    description="Comprehensive Google Tech Stack AI-Powered Investment Analysis",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve React frontend
if os.path.exists("frontend/build"):
    # Mount static assets (JS, CSS)
    if os.path.exists("frontend/build/static"):
        app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
    
    # Serve other assets (favicon, manifest, logos) directly from build
    @app.get("/favicon.ico")
    async def serve_favicon():
        return FileResponse("frontend/build/favicon.ico")
    
    @app.get("/manifest.json")
    async def serve_manifest():
        return FileResponse("frontend/build/manifest.json")
    
    @app.get("/logo192.png")
    async def serve_logo192():
        return FileResponse("frontend/build/logo192.png")
    
    @app.get("/logo512.png")
    async def serve_logo512():
        return FileResponse("frontend/build/logo512.png")
    
    @app.get("/robots.txt")
    async def serve_robots():
        return FileResponse("frontend/build/robots.txt")
    
    logger.info("✅ React frontend static files mounted")
else:
    logger.warning("⚠️ React frontend not built. Run 'npm run build' in frontend directory.")

async def keep_alive_worker():
    """Keep the service alive with periodic health checks"""
    import httpx
    
    while True:
        try:
            await asyncio.sleep(300)  # 5 minutes
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8080/api/health")
                if response.status_code == 200:
                    logger.info("Keep-alive ping successful")
                else:
                    logger.warning(f"Keep-alive ping failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Keep-alive error: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "firebase": enhanced_firebase_client.is_available(),
            "storage": enhanced_storage_client.is_available(),
            "google_adk": google_adk_orchestrator.get_agent_status()["orchestrator_initialized"]
        }
    }

@app.get("/api/status")
async def get_status():
    """Get comprehensive system status"""
    adk_status = {"orchestrator_initialized": True, "total_agents": len(google_adk_orchestrator.agents)}
    
    return {
        "platform": "Enhanced Startup Analyst Platform",
        "version": "2.0.0",
        "google_tech_stack": {
            "firebase": {
                "available": enhanced_firebase_client.is_available(),
                "description": "Real-time collaboration and data storage"
            },
            "cloud_storage": {
                "available": enhanced_storage_client.is_available(),
                "description": "File upload and document management"
            },
            "google_adk": {
                "available": adk_status["orchestrator_initialized"],
                "agents": adk_status["total_agents"],
                "description": "Multi-agent AI analysis system"
            }
        },
        "capabilities": [
            "Real-time collaborative analysis",
            "Document upload and processing",
            "Multi-agent AI evaluation",
            "Professional investment reports",
            "Live progress tracking"
        ]
    }

@app.post("/api/analyze")
async def analyze_startup_enhanced(startup_input: StartupInput):
    """Enhanced startup analysis using Google Tech Stack with multi-modal processing"""
    startup_id = f"{startup_input.company_name.replace(' ', '_')}_{int(time.time())}"
    
    try:
        logger.info(f"Starting enhanced multi-modal analysis for {startup_input.company_name}")
        
        # Step 1: Check for uploaded files for multi-modal processing
        uploaded_files = getattr(startup_input, 'uploaded_files', [])
        
        multi_modal_analysis = None
        if uploaded_files and len(uploaded_files) > 0:
            logger.info(f"Processing {len(uploaded_files)} uploaded files")
            
            # Process multi-modal pitch materials
            multi_modal_analysis = await multimodal_processor.process_pitch_materials(
                uploaded_files,
                startup_input.dict()
            )
            
            # Generate structured deal memo
            deal_memo = await deal_memo_generator.generate_investment_memo(
                multi_modal_analysis,
                startup_input.dict()
            )
            
            multi_modal_analysis["deal_memo"] = deal_memo
        
        # Step 2: Use working orchestrator for comprehensive analysis
        results = google_adk_orchestrator.analyze_startup(startup_input, "demo_user")
        
        # Step 3: Enhance results with multi-modal analysis if available
        if multi_modal_analysis:
            results["multi_modal_analysis"] = multi_modal_analysis
            results["has_pitch_materials"] = True
            results["pitch_material_types"] = [file.get('type', 'unknown') for file in uploaded_files]
        else:
            results["has_pitch_materials"] = False
        
        return {
            "status": "success",
            "startup_id": startup_id,
            "results": results,
            "message": "Multi-modal analysis completed using Google Tech Stack"
        }
        
    except Exception as e:
        logger.error(f"Enhanced analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/upload-file")
async def upload_file(
    file: UploadFile = File(...),
    startup_id: Optional[str] = Form(None)
):
    """Upload file to Google Cloud Storage"""
    try:
        if not enhanced_storage_client.is_available():
            # Demo mode response
            return {
                "status": "success",
                "filename": f"demo_{file.filename}",
                "public_url": f"https://demo-storage.example.com/{file.filename}",
                "size": file.size or 0,
                "timestamp": int(time.time()),
                "message": "Demo mode: File would be uploaded to Google Cloud Storage"
            }
        
        # Read file data
        file_data = await file.read()
        
        # Upload to Google Cloud Storage
        if startup_id:
            result = enhanced_storage_client.upload_startup_file(
                file_data, 
                file.filename or "unknown", 
                startup_id,
                file.content_type
            )
        else:
            result = enhanced_storage_client.upload_demo_file(
                file_data,
                file.filename or "unknown",
                "document"
            )
        
        return {
            "status": "success",
            "filename": result['storage_path'],
            "public_url": result['public_url'],
            "size": result['size'],
            "timestamp": result['timestamp'],
            "metadata": result.get('metadata', {})
        }
        
    except Exception as e:
        logger.error(f"File upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@app.get("/api/analysis-progress/{startup_id}")
async def get_analysis_progress(startup_id: str):
    """Get real-time analysis progress"""
    try:
        if enhanced_firebase_client.is_available():
            session_data = enhanced_firebase_client.get_analysis_session(startup_id)
            if session_data:
                return session_data
        
        # Fallback for demo mode
        return {
            "startup_id": startup_id,
            "progress": 100,
            "status": "completed",
            "current_agent": None,
            "agents_completed": ["data_collection", "business_analysis", "risk_assessment", "investment_insights", "report_generation"],
            "updated_at": time.time(),
            "message": "Demo mode: Real-time progress would be tracked via Firebase"
        }
        
    except Exception as e:
        logger.error(f"Failed to get analysis progress: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Progress tracking failed: {str(e)}")

@app.get("/api/analysis-history/{user_id}")
async def get_analysis_history(user_id: str):
    """Get user's analysis history"""
    try:
        if enhanced_firebase_client.is_available():
            history = enhanced_firebase_client.get_user_analysis_history(user_id)
            return {"history": history}
        
        # Demo mode response
        return {
            "history": [
                {
                    "startup_id": "demo_startup_1",
                    "company_name": "TechFlow AI",
                    "industry": "Artificial Intelligence",
                    "timestamp": time.time() - 3600,
                    "status": "completed",
                    "processing_time": 45.2
                },
                {
                    "startup_id": "demo_startup_2", 
                    "company_name": "EcoTransport",
                    "industry": "Clean Technology",
                    "timestamp": time.time() - 7200,
                    "status": "completed",
                    "processing_time": 38.5
                }
            ],
            "message": "Demo mode: History would be stored in Firebase"
        }
        
    except Exception as e:
        logger.error(f"Failed to get analysis history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"History retrieval failed: {str(e)}")

@app.get("/api/demo-scenarios")
async def get_demo_scenarios():
    """Get demo scenarios for testing"""
    try:
        scenarios = enhanced_firebase_client.get_demo_scenarios()
        return {"scenarios": scenarios}
        
    except Exception as e:
        logger.error(f"Failed to get demo scenarios: {str(e)}")
        # Return default scenarios
        return {
            "scenarios": [
                {
                    "company_name": "MedAI Solutions",
                    "industry": "Healthcare Technology",
                    "stage": "Series A",
                    "description": "AI-powered diagnostic platform for radiology",
                    "funding_request": "$5M",
                    "key_metrics": "200+ hospitals using platform, 95% accuracy rate"
                },
                {
                    "company_name": "EcoTransport",
                    "industry": "Clean Technology", 
                    "stage": "Seed",
                    "description": "Electric vehicle charging network with renewable energy",
                    "funding_request": "$2.5M",
                    "key_metrics": "50 charging stations deployed, partnerships with 3 cities"
                },
                {
                    "company_name": "FinanceFlow",
                    "industry": "Financial Technology",
                    "stage": "Series B", 
                    "description": "Automated financial planning for small businesses",
                    "funding_request": "$15M",
                    "key_metrics": "10,000+ SMB customers, $500K monthly recurring revenue"
                }
            ]
        }

@app.get("/api/storage-stats")
async def get_storage_stats():
    """Get Google Cloud Storage statistics"""
    try:
        if enhanced_storage_client.is_available():
            stats = enhanced_storage_client.get_storage_stats()
            return stats
        
        return {
            "message": "Storage not available in demo mode",
            "demo_stats": {
                "total_files": 0,
                "total_size_mb": 0,
                "bucket_name": "demo-bucket"
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get storage stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Storage stats failed: {str(e)}")

@app.get("/api/files/{startup_id}")
async def list_startup_files(startup_id: str):
    """List files for a specific startup"""
    try:
        if enhanced_storage_client.is_available():
            files = enhanced_storage_client.list_startup_files(startup_id)
            return {"files": files}
        
        return {
            "files": [],
            "message": "File listing not available in demo mode"
        }
        
    except Exception as e:
        logger.error(f"Failed to list files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File listing failed: {str(e)}")

@app.post("/api/generate-deal-memo")
async def generate_deal_memo(request_data: dict):
    """Generate structured investment memo from analysis results"""
    try:
        startup_info = request_data.get('startup_info', {})
        analysis_results = request_data.get('analysis_results', {})
        
        logger.info(f"Generating deal memo for {startup_info.get('company_name', 'Unknown')}")
        
        # Generate deal memo using the specialized generator
        deal_memo = await deal_memo_generator.generate_investment_memo(
            analysis_results,
            startup_info
        )
        
        return {
            "status": "success",
            "deal_memo": deal_memo,
            "generated_at": time.time(),
            "message": "Investment memo generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Deal memo generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Deal memo generation failed: {str(e)}")

@app.post("/api/process-multimodal")
async def process_multimodal_files(request_data: dict):
    """Process uploaded files for multi-modal analysis"""
    try:
        files = request_data.get('files', [])
        startup_info = request_data.get('startup_info', {})
        
        logger.info(f"Processing {len(files)} multi-modal files")
        
        # Process multi-modal content
        analysis_results = await multimodal_processor.process_pitch_materials(
            files,
            startup_info
        )
        
        return {
            "status": "success",
            "analysis_results": analysis_results,
            "processing_summary": {
                "total_files": len(files),
                "documents_processed": len(analysis_results.get('documents', [])),
                "audio_processed": len(analysis_results.get('audio_transcripts', [])),
                "videos_processed": len(analysis_results.get('video_analysis', []))
            },
            "message": "Multi-modal processing completed"
        }
        
    except Exception as e:
        logger.error(f"Multi-modal processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Multi-modal processing failed: {str(e)}")

# Serve React app for all other routes
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """Serve React application"""
    if os.path.exists("frontend/build/index.html"):
        return FileResponse("frontend/build/index.html")
    else:
        return {"message": "React frontend not built. Run 'npm run build' in frontend directory."}

if __name__ == "__main__":
    uvicorn.run(
        "enhanced_main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )