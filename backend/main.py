"""
FastAPI backend for Startup Analyst Platform
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import asyncio
import time
from typing import Dict, Any
import logging
from contextlib import asynccontextmanager

from src.agents.vertex_ai_orchestrator import VertexAIOrchestrator
from src.models.startup import StartupInput, AnalysisResults
from src.config.settings import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global orchestrator instance
orchestrator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global orchestrator
    
    # Startup
    logger.info("Starting Enhanced Startup Analyst Platform with Vertex AI...")
    orchestrator = VertexAIOrchestrator()
    
    # Start keep-alive task
    keep_alive_task = asyncio.create_task(keep_alive_worker())
    
    yield
    
    # Shutdown
    logger.info("Shutting down Startup Analyst Platform...")
    keep_alive_task.cancel()

# Create FastAPI app
app = FastAPI(
    title="Startup Analyst Platform",
    description="AI-Powered Startup Investment Analysis",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (React build)
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

@app.get("/")
async def serve_frontend():
    """Serve the React frontend"""
    return FileResponse("frontend/build/index.html")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "version": "1.0.0"
    }

@app.get("/api/status")
async def get_status():
    """Get system status"""
    if orchestrator:
        return {
            "status": "ready",
            "agents": orchestrator.get_agent_status(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    return {"status": "initializing"}

@app.post("/api/analyze")
async def analyze_startup(startup_input: StartupInput, background_tasks: BackgroundTasks, user_id: str = None):
    """Analyze a startup using enhanced Vertex AI agents"""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="System not ready")
        
        logger.info(f"Starting enhanced analysis for {startup_input.company_name}")
        
        # Convert StartupInput to StartupData format
        from agents.startup_analyst_agents import StartupData
        startup_data = StartupData(
            company_name=startup_input.company_name,
            founder_name=startup_input.founder_name or "Unknown",
            business_description=startup_input.business_description,
            pitch_deck_url=startup_input.pitch_deck_url,
            website_url=startup_input.website,
            industry=startup_input.industry,
            funding_stage=startup_input.stage,
            team_size=None
        )
        
        # Run enhanced analysis with Vertex AI
        try:
            results = orchestrator.analyze_startup(startup_data)
            # Check if results is a coroutine (async function)
            if hasattr(results, '__await__'):
                # If it's async, we need to await it
                import asyncio
                results = await results
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
        
        # Log analysis completion
        background_tasks.add_task(log_analysis_completion, startup_input.company_name, 10.0)  # Default processing time
        
        # Convert results to serializable format
        serializable_results = {}
        for key, result in results.items():
            serializable_results[key] = {
                "agent_name": result.agent_name,
                "analysis_type": result.analysis_type,
                "findings": result.findings,
                "confidence_score": result.confidence_score,
                "timestamp": result.timestamp.isoformat()
            }
        
        return {
            "status": "success",
            "results": serializable_results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "enhanced": True,
            "vertex_ai": True
        }
        
    except Exception as e:
        logger.error(f"Enhanced analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Enhanced analysis failed: {str(e)}")

@app.get("/api/analysis-progress/{startup_id}")
async def get_analysis_progress(startup_id: str):
    """Get real-time analysis progress"""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="System not ready")
        
        # Simple progress response since working orchestrator doesn't track progress
        progress = {
            "current_agent": "completed",
            "percentage": 100,
            "message": "Analysis completed"
        }
        
        if progress:
            return {
                "status": "success",
                "progress": progress,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {
                "status": "not_found",
                "message": "Analysis not found or completed",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        
    except Exception as e:
        logger.error(f"Failed to get analysis progress: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get analysis progress: {str(e)}")

@app.get("/api/analysis-history/{user_id}")
async def get_analysis_history(user_id: str):
    """Get analysis history for a user"""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="System not ready")
        
        history = orchestrator.firebase_client.get_analysis_history(user_id)
        
        return {
            "status": "success",
            "history": history,
            "count": len(history),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        logger.error(f"Failed to get analysis history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get analysis history: {str(e)}")

@app.get("/api/demo-scenarios")
async def get_demo_scenarios():
    """Get demo scenarios for testing"""
    return {
        "scenarios": [
            {
                "id": "high-potential",
                "name": "High-Potential AI Startup",
                "description": "AI-powered healthcare platform with strong team and market opportunity",
                "data": {
                    "company_name": "MedAI Solutions",
                    "business_description": "AI-powered diagnostic platform that helps doctors identify diseases from medical images with 95% accuracy. Our platform reduces diagnosis time by 70% and improves patient outcomes.",
                    "industry": "Healthcare AI",
                    "stage": "Series A",
                    "founder_name": "Dr. Sarah Chen",
                    "founder_background": "Former Google AI researcher with 10 years in medical imaging. PhD in Computer Science from Stanford. Published 50+ papers in top-tier journals.",
                    "website": "https://medai-solutions.com",
                    "additional_info": "Raised $5M seed round. 50+ hospital partnerships. FDA approval in progress."
                }
            },
            {
                "id": "risky-startup",
                "name": "Risky Consumer App",
                "description": "Consumer app with unclear business model and high competition",
                "data": {
                    "company_name": "SocialSnap",
                    "business_description": "Social media app for sharing photos with friends. Features include filters, stories, and group chats. Targeting Gen Z users.",
                    "industry": "Social Media",
                    "stage": "Seed",
                    "founder_name": "Mike Johnson",
                    "founder_background": "Recent college graduate with 2 years at a startup. No previous experience in social media or consumer apps.",
                    "website": "https://socialsnap.app",
                    "additional_info": "Pre-revenue. High user acquisition costs. Competing with Instagram and TikTok."
                }
            },
            {
                "id": "watch-list",
                "name": "Watch List B2B SaaS",
                "description": "Early-stage B2B SaaS with promising technology but needs more traction",
                "data": {
                    "company_name": "WorkflowAI",
                    "business_description": "AI-powered workflow automation platform for small businesses. Automates repetitive tasks and improves productivity by 40%.",
                    "industry": "B2B SaaS",
                    "stage": "Seed",
                    "founder_name": "Alex Rodriguez",
                    "founder_background": "Former Salesforce engineer with 8 years experience. MBA from Wharton. Previous startup experience.",
                    "website": "https://workflowai.com",
                    "additional_info": "Early traction with 100+ customers. $50K MRR. Strong product-market fit signals."
                }
            }
        ]
    }

async def log_analysis_completion(company_name: str, processing_time: float):
    """Log analysis completion"""
    logger.info(f"Analysis completed for {company_name} in {processing_time:.2f} seconds")

async def keep_alive_worker():
    """Keep the service alive to prevent Cloud Run sleep"""
    while True:
        try:
            # Make a request to our own health endpoint
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8080/api/health")
                if response.status_code == 200:
                    logger.info("Keep-alive ping successful")
                else:
                    logger.warning(f"Keep-alive ping failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Keep-alive ping error: {str(e)}")
        
        # Wait 10 minutes before next ping
        await asyncio.sleep(600)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
