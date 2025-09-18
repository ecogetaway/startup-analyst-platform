#!/usr/bin/env python3
"""
Enhanced Startup Analyst Platform
Integrates existing startup analysis with Smart Report Analyzer features
"""

import os
import sys
import time
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd

# Add current directory to Python path
sys.path.append('.')
sys.path.append('/Users/sanjay/google')

# Import working components
from agents.startup_analyst_agents import StartupAnalystOrchestrator, StartupData

# Import Smart Report Analyzer utilities
try:
    from src.utils.file_handler import load_file
    from src.utils.llm_agent import summarize_report, ask_question
    from src.utils.eda import generate_eda_report
    SMART_ANALYZER_AVAILABLE = True
except ImportError:
    SMART_ANALYZER_AVAILABLE = False
    logging.warning("Smart Analyzer utilities not available")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Enhanced Startup Analyst Platform", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = StartupAnalystOrchestrator()

# Pydantic models
class StartupInput(BaseModel):
    company_name: str
    business_description: str
    industry: Optional[str] = None
    stage: Optional[str] = None
    founder_name: Optional[str] = None
    website: Optional[str] = None
    pitch_deck_url: Optional[str] = None
    additional_info: Optional[str] = None

class DocumentAnalysisRequest(BaseModel):
    analysis_type: str  # "pitch_deck", "financial_data", "business_plan"
    questions: Optional[list] = []

# Mount static files for the frontend
try:
    app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")
    logger.info("✅ Frontend static files mounted from frontend/build")
except Exception as e:
    logger.warning(f"⚠️ Could not mount frontend files: {e}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "version": "2.0.0",
        "features": {
            "startup_analysis": True,
            "smart_analyzer": SMART_ANALYZER_AVAILABLE,
            "document_processing": SMART_ANALYZER_AVAILABLE
        }
    }

@app.get("/api/status")
async def get_status():
    """Get system status"""
    return {
        "status": "ready",
        "platform": "Enhanced Startup Analyst Platform",
        "agents_available": len(orchestrator.agents),
        "smart_analyzer": SMART_ANALYZER_AVAILABLE,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

@app.post("/api/analyze")
async def analyze_startup(startup_input: StartupInput):
    """Analyze a startup using AI agents"""
    try:
        logger.info(f"Starting analysis for {startup_input.company_name}")
        
        # Convert to StartupData format
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
        
        # Run analysis
        results = orchestrator.analyze_startup(startup_data)
        
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
        
        logger.info(f"✅ Analysis completed for {startup_input.company_name}")
        
        return {
            "status": "success",
            "results": serializable_results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "analysis_time": "10.0 seconds"
        }
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/analyze-document")
async def analyze_document(file: UploadFile = File(...), analysis_type: str = "pitch_deck"):
    """Analyze uploaded documents using Smart Report Analyzer"""
    if not SMART_ANALYZER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Smart Analyzer not available")
    
    try:
        logger.info(f"Analyzing document: {file.filename}")
        
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Load and analyze file
        df, raw_text = load_file(temp_path)
        
        result = {
            "filename": file.filename,
            "analysis_type": analysis_type,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if df is not None:
            # Structured data analysis
            result["data_preview"] = df.head().to_dict()
            result["summary"] = summarize_report(df)
            result["data_type"] = "structured"
            
        elif raw_text:
            # PDF/text analysis
            result["text_preview"] = raw_text[:500] + "..." if len(raw_text) > 500 else raw_text
            result["summary"] = summarize_report(raw_text)
            result["data_type"] = "unstructured"
        
        # Clean up temp file
        os.remove(temp_path)
        
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Document analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Document analysis failed: {str(e)}")

@app.post("/api/ask-question")
async def ask_document_question(file: UploadFile = File(...), question: str = ""):
    """Ask questions about uploaded documents"""
    if not SMART_ANALYZER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Smart Analyzer not available")
    
    try:
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Load file and ask question
        df, raw_text = load_file(temp_path)
        
        if df is not None:
            answer = ask_question(df, question)
        elif raw_text:
            answer = ask_question(raw_text, question)
        else:
            answer = "Could not process the uploaded file."
        
        # Clean up temp file
        os.remove(temp_path)
        
        return {
            "status": "success",
            "question": question,
            "answer": answer,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        logger.error(f"Question answering failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Question answering failed: {str(e)}")

@app.get("/api/analysis-progress/{startup_id}")
async def get_analysis_progress(startup_id: str):
    """Get analysis progress (simplified)"""
    return {
        "status": "success",
        "progress": {
            "current_agent": "completed",
            "percentage": 100,
            "message": "Analysis completed"
        },
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
