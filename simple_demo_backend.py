#!/usr/bin/env python3
"""
Simple Demo Backend for Hackathon
- Fast responses for prototype demo
- Simplified output
- No complex processing
"""

import sys
import os
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Startup Analyst Demo", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class StartupInput(BaseModel):
    company_name: str
    business_description: str
    industry: Optional[str] = None
    stage: Optional[str] = None
    founder_name: Optional[str] = None
    founder_background: Optional[str] = None
    website: Optional[str] = None
    pitch_deck_url: Optional[str] = None
    additional_info: Optional[str] = None
    pdf_content: Optional[Dict[str, Any]] = None
    uploaded_files: Optional[list] = None

# Simple demo responses
DEMO_ANALYSIS_TEMPLATES = {
    "technology": {
        "recommendation": "INVEST",
        "confidence_score": 0.87,
        "summary": "Strong technology platform with significant market potential. The team demonstrates deep expertise in AI/ML with a clear path to monetization.",
        "key_strengths": [
            "Innovative technology solution",
            "Experienced technical team", 
            "Large addressable market",
            "Clear revenue model"
        ],
        "risk_factors": [
            "Competitive landscape",
            "Market timing",
            "Technical execution risk"
        ]
    },
    "healthcare": {
        "recommendation": "WATCH",
        "confidence_score": 0.73,
        "summary": "Promising healthcare solution with regulatory challenges. Market need is validated but execution timeline extended due to compliance requirements.",
        "key_strengths": [
            "Clear market need",
            "Regulatory pathway identified",
            "Strong medical advisory board"
        ],
        "risk_factors": [
            "Regulatory approval timeline",
            "Clinical validation required",
            "Reimbursement strategy"
        ]
    },
    "default": {
        "recommendation": "INVEST",
        "confidence_score": 0.82,
        "summary": "Well-positioned startup with strong fundamentals. The business model shows clear value proposition and scalable growth potential.",
        "key_strengths": [
            "Strong value proposition",
            "Scalable business model",
            "Experienced team",
            "Market validation"
        ],
        "risk_factors": [
            "Market competition",
            "Execution challenges",
            "Funding requirements"
        ]
    }
}

# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/status")
async def get_status():
    return {
        "status": "ready",
        "platform": "Startup Analyst Demo",
        "version": "1.0.0",
        "demo_mode": True,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.post("/api/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """Simple file upload for demo"""
    try:
        logger.info(f"Demo file upload: {file.filename}")
        
        # Create uploads directory
        os.makedirs("uploads", exist_ok=True)
        
        # Generate filename
        timestamp = int(time.time() * 1000)
        filename = f"{timestamp}_{file.filename}"
        file_path = f"uploads/{filename}"
        
        # Save file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "filename": filename,
            "original_filename": file.filename,
            "size": len(content),
            "file_path": file_path,
            "public_url": f"/uploads/{filename}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "extracted_content": {
                "success": True,
                "text": f"Demo content extracted from {file.filename}",
                "text_length": 500,
                "page_count": 10,
                "extraction_method": "demo"
            }
        }
        
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/analyze")
async def analyze_startup(startup_input: StartupInput):
    """Fast demo analysis"""
    try:
        logger.info(f"Demo analysis for: {startup_input.company_name}")
        
        # Simulate processing time (very short for demo)
        await asyncio.sleep(2)
        
        # Select template based on industry
        industry_key = "default"
        if startup_input.industry:
            industry_lower = startup_input.industry.lower()
            if "tech" in industry_lower or "ai" in industry_lower or "software" in industry_lower:
                industry_key = "technology"
            elif "health" in industry_lower or "medical" in industry_lower:
                industry_key = "healthcare"
        
        template = DEMO_ANALYSIS_TEMPLATES[industry_key]
        
        # Generate demo ML prediction
        success_prob = 0.75 + (len(startup_input.company_name) * 0.01)
        success_prob = min(success_prob, 0.95)
        
        # Create simplified results
        has_pitch_deck = bool(startup_input.pdf_content or startup_input.uploaded_files)
        analysis_source = "pitch_deck" if has_pitch_deck else "company_metadata"
        
        results = {
            "company_name": startup_input.company_name,
            "recommendation": template["recommendation"],
            "confidence_score": template["confidence_score"] + (0.05 if has_pitch_deck else 0),  # Higher confidence with pitch deck
            "processing_time": 2.0,
            "has_pitch_materials": has_pitch_deck,
            "analysis_source": analysis_source,
            "agents_used": ["business_analysis", "risk_assessment", "investment_insights"],
            "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            
            # Simplified agent results
            "agent_results": {
                "business_analysis": {
                    "agent_name": "Business Analysis Agent",
                    "analysis_type": "business_analysis",
                    "findings": {
                        "analysis": f"Based on {'pitch deck analysis' if has_pitch_deck else 'company metadata'}: {template['summary']}",
                        "key_points": template["key_strengths"],
                        "data_source": "pitch_deck" if has_pitch_deck else "metadata"
                    },
                    "confidence_score": template["confidence_score"],
                    "timestamp": datetime.now().isoformat()
                },
                "risk_assessment": {
                    "agent_name": "Risk Assessment Agent", 
                    "analysis_type": "risk_assessment",
                    "findings": {
                        "risk_analysis": f"Key risks for {startup_input.company_name}: " + ", ".join(template["risk_factors"]),
                        "risk_levels": template["risk_factors"]
                    },
                    "confidence_score": 0.85,
                    "timestamp": datetime.now().isoformat()
                },
                "investment_insights": {
                    "agent_name": "Investment Insights Agent",
                    "analysis_type": "investment_insights", 
                    "findings": {
                        "investment_insights": f"Investment Recommendation: {template['recommendation']}\n\nAnalysis Source: {'Comprehensive pitch deck review' if has_pitch_deck else 'Company metadata analysis'}\n\nRationale: {template['summary']}\n\nKey Investment Highlights:\n" + "\n".join([f"• {point}" for point in template['key_strengths']]),
                        "recommendation": template["recommendation"],
                        "key_thesis": template["key_strengths"],
                        "analysis_basis": "pitch_deck_driven" if has_pitch_deck else "metadata_driven"
                    },
                    "confidence_score": template["confidence_score"],
                    "timestamp": datetime.now().isoformat()
                }
            },
            
            # Simple ML prediction
            "ml_prediction": {
                "success_probability": success_prob,
                "prediction": "Success" if success_prob > 0.7 else "Watch",
                "confidence": 0.85,
                "key_factors": [
                    ["market_opportunity", 0.85],
                    ["team_strength", 0.78],
                    ["product_readiness", 0.82]
                ],
                "model_accuracy": 0.85
            }
        }
        
        logger.info(f"✅ Demo analysis completed for {startup_input.company_name}")
        
        return {
            "status": "success",
            "results": results,
            "startup_id": f"{startup_input.company_name.lower().replace(' ', '_')}_{int(time.time())}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analysis_time": "2.0 seconds",
            "demo_mode": True
        }
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Mount static files AFTER API routes
try:
    app.mount("/", StaticFiles(directory="frontend/build", html=True), name="frontend")
    logger.info("✅ Frontend static files mounted")
except Exception as e:
    logger.warning(f"Could not mount frontend: {e}")

if __name__ == "__main__":
    import uvicorn
    import asyncio
    logger.info("🚀 Starting Simple Demo Backend...")
    uvicorn.run(app, host="0.0.0.0", port=8080)
