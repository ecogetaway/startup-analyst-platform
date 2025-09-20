#!/usr/bin/env python3
"""
Production Backend API for Startup Analyst Platform
Integrates enhanced ML pipeline with FastAPI for real startup analysis
"""

import os
import sys
import time
import logging
import asyncio
import uuid
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from pathlib import Path

# FastAPI and dependencies
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Add project paths
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))
sys.path.append(str(current_dir / 'src'))

# Import production ML pipeline
try:
    from src.ml.production_pipeline import (
        ProductionMLPipeline, 
        ProductionAnalysisInput,
        ProductionAnalysisResult,
        analyze_startup_production,
        get_production_pipeline
    )
    from src.ml.production_ensemble_predictor import ProductionPredictionResult
    from src.ml.pdf_financial_extractor import ExtractedFinancialData
    ML_PIPELINE_AVAILABLE = True
except ImportError as e:
    ML_PIPELINE_AVAILABLE = False
    print(f"⚠️ ML Pipeline not available: {e}")

# Import existing components
try:
    from agents.startup_analyst_agents import StartupAnalystOrchestrator, StartupData
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Startup Analyst Platform - Production API",
    description="Production-ready AI-powered startup analysis with ML predictions",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
analysis_cache = {}  # In production, use Redis or database
file_storage_path = Path("uploaded_files")
file_storage_path.mkdir(exist_ok=True)

# Initialize production pipeline
production_pipeline = None
if ML_PIPELINE_AVAILABLE:
    try:
        production_pipeline = get_production_pipeline()
        logger.info("✅ Production ML Pipeline initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize production pipeline: {e}")

# Pydantic models
class ProductionStartupInput(BaseModel):
    """Enhanced input model for production analysis"""
    company_name: str = Field(..., description="Company name")
    industry: Optional[str] = Field(None, description="Industry sector")
    description: Optional[str] = Field(None, description="Company description")
    
    # Optional manual data
    current_revenue: Optional[float] = Field(None, description="Current annual revenue in USD")
    funding_requested: Optional[float] = Field(None, description="Funding amount requested")
    market_size: Optional[float] = Field(None, description="Total addressable market in billions")
    team_size: Optional[int] = Field(None, description="Number of team members")
    founded_year: Optional[int] = Field(None, description="Year company was founded")
    
    # Analysis options
    use_pdf_extraction: bool = Field(True, description="Extract data from uploaded PDFs")
    use_ai_agents: bool = Field(True, description="Use AI agents for analysis")
    use_ml_prediction: bool = Field(True, description="Use ML models for prediction")
    
    class Config:
        schema_extra = {
            "example": {
                "company_name": "TechStartup AI",
                "industry": "Technology",
                "description": "AI-powered solutions for enterprise automation",
                "current_revenue": 500000,
                "funding_requested": 2000000,
                "market_size": 5.0,
                "team_size": 8,
                "founded_year": 2022
            }
        }

class AnalysisStatusResponse(BaseModel):
    """Response model for analysis status"""
    analysis_id: str
    status: str  # "pending", "processing", "completed", "failed"
    progress: float  # 0.0 to 1.0
    message: str
    estimated_completion: Optional[str] = None
    created_at: str

class ProductionAnalysisResponse(BaseModel):
    """Response model for completed analysis"""
    analysis_id: str
    company_name: str
    timestamp: str
    
    # Core results
    success_probability: float
    success_category: str
    investment_recommendation: str
    confidence_interval: List[float]
    
    # Detailed scores
    market_score: float
    team_score: float
    product_score: float
    business_model_score: float
    financial_score: float
    risk_score: float
    
    # Insights
    key_strengths: List[Dict[str, Any]]
    key_risks: List[Dict[str, Any]]
    improvement_areas: List[str]
    
    # Metadata
    processing_time_seconds: float
    components_used: List[str]
    overall_confidence: float
    data_completeness: float
    model_version: str

class FileUploadResponse(BaseModel):
    """Response model for file uploads"""
    file_id: str
    filename: str
    size: int
    file_type: str
    storage_path: str
    upload_timestamp: str
    status: str

# Utility functions
def generate_analysis_id() -> str:
    """Generate unique analysis ID"""
    return f"prod_{uuid.uuid4().hex[:8]}_{int(time.time())}"

def save_uploaded_file(file: UploadFile) -> Dict[str, Any]:
    """Save uploaded file and return metadata"""
    file_id = uuid.uuid4().hex
    timestamp = datetime.now().isoformat()
    
    # Create storage path
    file_extension = Path(file.filename).suffix
    storage_filename = f"{file_id}{file_extension}"
    storage_path = file_storage_path / storage_filename
    
    # Save file
    with open(storage_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "size": len(content),
        "file_type": file.content_type,
        "storage_path": str(storage_path),
        "upload_timestamp": timestamp,
        "status": "uploaded"
    }

def convert_production_result_to_response(result: ProductionAnalysisResult) -> ProductionAnalysisResponse:
    """Convert internal result to API response"""
    return ProductionAnalysisResponse(
        analysis_id=result.analysis_id,
        company_name=result.company_name,
        timestamp=result.timestamp,
        success_probability=result.ml_prediction.success_probability,
        success_category=result.ml_prediction.success_category,
        investment_recommendation=result.ml_prediction.investment_recommendation,
        confidence_interval=list(result.ml_prediction.confidence_interval),
        market_score=result.ml_prediction.market_score,
        team_score=result.ml_prediction.team_score,
        product_score=result.ml_prediction.product_score,
        business_model_score=result.ml_prediction.business_model_score,
        financial_score=result.ml_prediction.financial_score,
        risk_score=result.ml_prediction.risk_score,
        key_strengths=[{"factor": k, "score": v} for k, v in result.ml_prediction.key_strengths],
        key_risks=[{"factor": k, "score": v} for k, v in result.ml_prediction.key_risks],
        improvement_areas=result.ml_prediction.improvement_areas,
        processing_time_seconds=result.processing_time_seconds,
        components_used=result.components_used,
        overall_confidence=result.overall_confidence,
        data_completeness=result.data_completeness,
        model_version=result.ml_prediction.model_version
    )

# Background task for analysis
async def run_analysis_background(analysis_id: str, input_data: ProductionAnalysisInput, pdf_path: Optional[str] = None):
    """Run analysis in background"""
    try:
        # Update status
        analysis_cache[analysis_id]["status"] = "processing"
        analysis_cache[analysis_id]["progress"] = 0.1
        analysis_cache[analysis_id]["message"] = "Starting analysis..."
        
        if not production_pipeline:
            raise Exception("Production pipeline not available")
        
        # Create pipeline input
        pipeline_input = ProductionAnalysisInput(
            company_name=input_data.company_name,
            industry=input_data.industry,
            description=input_data.description,
            pdf_path=pdf_path,
            manual_data={
                k: v for k, v in {
                    'current_revenue': input_data.current_revenue,
                    'funding_requested': input_data.funding_requested,
                    'market_size': input_data.market_size,
                    'team_size': input_data.team_size,
                    'founded_year': input_data.founded_year
                }.items() if v is not None
            },
            use_pdf_extraction=input_data.use_pdf_extraction,
            use_ai_agents=input_data.use_ai_agents,
            use_ml_prediction=input_data.use_ml_prediction,
            analysis_id=analysis_id
        )
        
        # Update progress
        analysis_cache[analysis_id]["progress"] = 0.3
        analysis_cache[analysis_id]["message"] = "Running ML analysis..."
        
        # Run analysis
        result = production_pipeline.analyze_startup(pipeline_input)
        
        # Update progress
        analysis_cache[analysis_id]["progress"] = 1.0
        analysis_cache[analysis_id]["status"] = "completed"
        analysis_cache[analysis_id]["message"] = "Analysis completed successfully"
        analysis_cache[analysis_id]["result"] = result
        
        logger.info(f"✅ Analysis {analysis_id} completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Analysis {analysis_id} failed: {e}")
        analysis_cache[analysis_id]["status"] = "failed"
        analysis_cache[analysis_id]["message"] = f"Analysis failed: {str(e)}"
        analysis_cache[analysis_id]["error"] = str(e)

# API Routes

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Startup Analyst Platform - Production API",
        "version": "2.0.0",
        "status": "running",
        "ml_pipeline_available": ML_PIPELINE_AVAILABLE,
        "ai_agents_available": AGENTS_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "ml_pipeline": ML_PIPELINE_AVAILABLE,
            "ai_agents": AGENTS_AVAILABLE,
            "file_storage": file_storage_path.exists()
        }
    }

@app.get("/pipeline/stats", tags=["Pipeline"])
async def get_pipeline_stats():
    """Get pipeline performance statistics"""
    if not production_pipeline:
        raise HTTPException(status_code=503, detail="Production pipeline not available")
    
    stats = production_pipeline.get_pipeline_stats()
    return stats

@app.post("/upload-file", response_model=FileUploadResponse, tags=["Files"])
async def upload_file(file: UploadFile = File(...)):
    """Upload a file for analysis"""
    try:
        # Validate file type
        allowed_types = ["application/pdf", "audio/mpeg", "audio/wav", "video/mp4"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file.content_type} not supported. Allowed: {allowed_types}"
            )
        
        # Validate file size (max 100MB)
        max_size = 100 * 1024 * 1024  # 100MB
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File size {file_size} exceeds maximum {max_size} bytes"
            )
        
        # Save file
        file_metadata = save_uploaded_file(file)
        
        return FileUploadResponse(**file_metadata)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@app.post("/analyze", response_model=AnalysisStatusResponse, tags=["Analysis"])
async def start_analysis(
    startup_input: ProductionStartupInput,
    background_tasks: BackgroundTasks,
    file_id: Optional[str] = None
):
    """Start startup analysis"""
    try:
        if not production_pipeline:
            raise HTTPException(status_code=503, detail="Production pipeline not available")
        
        # Generate analysis ID
        analysis_id = generate_analysis_id()
        
        # Initialize analysis tracking
        analysis_cache[analysis_id] = {
            "status": "pending",
            "progress": 0.0,
            "message": "Analysis queued",
            "created_at": datetime.now().isoformat(),
            "input": startup_input.dict()
        }
        
        # Get file path if file_id provided
        pdf_path = None
        if file_id:
            # Find uploaded file
            for file_path in file_storage_path.glob("*"):
                if file_id in file_path.name:
                    pdf_path = str(file_path)
                    break
            
            if not pdf_path:
                raise HTTPException(status_code=404, detail="Uploaded file not found")
        
        # Start background analysis
        background_tasks.add_task(run_analysis_background, analysis_id, startup_input, pdf_path)
        
        return AnalysisStatusResponse(
            analysis_id=analysis_id,
            status="pending",
            progress=0.0,
            message="Analysis started",
            created_at=analysis_cache[analysis_id]["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start analysis: {str(e)}")

@app.get("/analysis/{analysis_id}/status", response_model=AnalysisStatusResponse, tags=["Analysis"])
async def get_analysis_status(analysis_id: str):
    """Get analysis status"""
    if analysis_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    cache_data = analysis_cache[analysis_id]
    
    return AnalysisStatusResponse(
        analysis_id=analysis_id,
        status=cache_data["status"],
        progress=cache_data["progress"],
        message=cache_data["message"],
        created_at=cache_data["created_at"]
    )

@app.get("/analysis/{analysis_id}/result", response_model=ProductionAnalysisResponse, tags=["Analysis"])
async def get_analysis_result(analysis_id: str):
    """Get analysis result"""
    if analysis_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    cache_data = analysis_cache[analysis_id]
    
    if cache_data["status"] != "completed":
        raise HTTPException(
            status_code=400, 
            detail=f"Analysis not completed. Status: {cache_data['status']}"
        )
    
    if "result" not in cache_data:
        raise HTTPException(status_code=500, detail="Analysis result not available")
    
    result = cache_data["result"]
    return convert_production_result_to_response(result)

@app.post("/analyze-sync", response_model=ProductionAnalysisResponse, tags=["Analysis"])
async def analyze_sync(startup_input: ProductionStartupInput, file_id: Optional[str] = None):
    """Synchronous analysis (for smaller requests)"""
    try:
        if not production_pipeline:
            raise HTTPException(status_code=503, detail="Production pipeline not available")
        
        # Get file path if file_id provided
        pdf_path = None
        if file_id:
            for file_path in file_storage_path.glob("*"):
                if file_id in file_path.name:
                    pdf_path = str(file_path)
                    break
        
        # Create pipeline input
        pipeline_input = ProductionAnalysisInput(
            company_name=startup_input.company_name,
            industry=startup_input.industry,
            description=startup_input.description,
            pdf_path=pdf_path,
            manual_data={
                k: v for k, v in {
                    'current_revenue': startup_input.current_revenue,
                    'funding_requested': startup_input.funding_requested,
                    'market_size': startup_input.market_size,
                    'team_size': startup_input.team_size,
                    'founded_year': startup_input.founded_year
                }.items() if v is not None
            },
            use_pdf_extraction=startup_input.use_pdf_extraction,
            use_ai_agents=startup_input.use_ai_agents,
            use_ml_prediction=startup_input.use_ml_prediction
        )
        
        # Run analysis
        result = production_pipeline.analyze_startup(pipeline_input)
        
        return convert_production_result_to_response(result)
        
    except Exception as e:
        logger.error(f"Synchronous analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.delete("/analysis/{analysis_id}", tags=["Analysis"])
async def delete_analysis(analysis_id: str):
    """Delete analysis from cache"""
    if analysis_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    del analysis_cache[analysis_id]
    return {"message": "Analysis deleted successfully"}

@app.get("/analyses", tags=["Analysis"])
async def list_analyses(limit: int = 50, status: Optional[str] = None):
    """List recent analyses"""
    analyses = []
    
    for analysis_id, data in list(analysis_cache.items())[-limit:]:
        if status and data.get("status") != status:
            continue
        
        analyses.append({
            "analysis_id": analysis_id,
            "company_name": data.get("input", {}).get("company_name", "Unknown"),
            "status": data.get("status"),
            "progress": data.get("progress"),
            "created_at": data.get("created_at")
        })
    
    return {"analyses": analyses, "total": len(analyses)}

# Keep-alive endpoint for deployment
@app.get("/keep-alive", tags=["Health"])
async def keep_alive():
    """Keep-alive endpoint to prevent service from sleeping"""
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat(),
        "uptime": time.time()
    }

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# Production server configuration
if __name__ == "__main__":
    # Development server
    logger.info("🚀 Starting Production Startup Analyst API")
    
    uvicorn.run(
        "production_main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
