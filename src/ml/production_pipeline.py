#!/usr/bin/env python3
"""
Production ML Pipeline for Startup Analysis
Integrates PDF extraction, feature engineering, and ensemble prediction
"""

import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import asyncio
from pathlib import Path

# ML Pipeline Components
try:
    from .production_ensemble_predictor import (
        ProductionEnsemblePredictor, 
        ProductionPredictionResult,
        ProductionStartupFeatures,
        predict_startup_success_production
    )
    from .pdf_financial_extractor import (
        ProductionPDFExtractor,
        ExtractedFinancialData,
        extract_financial_data_from_pdf
    )
except ImportError:
    # Fallback for direct execution
    from production_ensemble_predictor import (
        ProductionEnsemblePredictor, 
        ProductionPredictionResult,
        ProductionStartupFeatures,
        predict_startup_success_production
    )
    from pdf_financial_extractor import (
        ProductionPDFExtractor,
        ExtractedFinancialData,
        extract_financial_data_from_pdf
    )

# Existing components
try:
    import sys
    sys.path.append('../../')
    from agents.startup_analyst_agents import StartupAnalystOrchestrator, StartupData
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    # Create dummy class for type hints
    class StartupData:
        def __init__(self, company_name: str, industry: str = "", description: str = ""):
            self.company_name = company_name
            self.industry = industry
            self.description = description

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProductionAnalysisInput:
    """Input data for production analysis pipeline"""
    # Basic Information
    company_name: str
    industry: Optional[str] = None
    description: Optional[str] = None
    
    # File Inputs
    pdf_path: Optional[str] = None
    audio_path: Optional[str] = None
    video_path: Optional[str] = None
    
    # Manual Overrides
    manual_data: Optional[Dict[str, Any]] = None
    
    # Analysis Options
    use_pdf_extraction: bool = True
    use_ai_agents: bool = True
    use_ml_prediction: bool = True
    
    # Metadata
    analysis_id: Optional[str] = None
    timestamp: Optional[str] = None

@dataclass
class ProductionAnalysisResult:
    """Comprehensive production analysis result"""
    # Input Information
    analysis_id: str
    company_name: str
    timestamp: str
    
    # Core Prediction
    ml_prediction: ProductionPredictionResult
    
    # Extracted Data
    pdf_data: Optional[ExtractedFinancialData] = None
    
    # Agent Analysis (if available)
    agent_analysis: Optional[Dict[str, Any]] = None
    
    # Processing Metadata
    processing_time_seconds: float = 0.0
    pipeline_version: str = "2.0.0"
    components_used: List[str] = None
    
    # Success Metrics
    overall_confidence: float = 0.0
    data_completeness: float = 0.0
    
    def __post_init__(self):
        if self.components_used is None:
            self.components_used = []

class ProductionMLPipeline:
    """
    Production ML pipeline that orchestrates all components
    for comprehensive startup analysis
    """
    
    def __init__(self):
        self.version = "2.0.0"
        
        # Initialize components
        self.pdf_extractor = ProductionPDFExtractor()
        self.ml_predictor = ProductionEnsemblePredictor()
        self.agent_orchestrator = None
        
        # Initialize agent orchestrator if available
        if AGENTS_AVAILABLE:
            try:
                self.agent_orchestrator = StartupAnalystOrchestrator()
                logger.info("✅ Agent orchestrator initialized")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize agent orchestrator: {e}")
        
        # Performance tracking
        self.analysis_count = 0
        self.total_processing_time = 0.0
        
        logger.info("🚀 Production ML Pipeline initialized")
    
    def extract_features_from_pdf(self, pdf_path: str) -> Tuple[ExtractedFinancialData, Dict[str, Any]]:
        """Extract financial features from PDF with error handling"""
        try:
            logger.info(f"📄 Extracting features from PDF: {pdf_path}")
            start_time = time.time()
            
            # Extract financial data
            pdf_data = self.pdf_extractor.extract_financial_data(pdf_path)
            
            # Convert to ML features
            ml_features = self._convert_pdf_to_ml_features(pdf_data)
            
            processing_time = time.time() - start_time
            logger.info(f"✅ PDF extraction completed in {processing_time:.2f}s")
            
            return pdf_data, ml_features
            
        except Exception as e:
            logger.error(f"❌ PDF extraction failed: {e}")
            return ExtractedFinancialData(), {}
    
    def _convert_pdf_to_ml_features(self, pdf_data: ExtractedFinancialData) -> Dict[str, Any]:
        """Convert extracted PDF data to ML features"""
        features = {}
        
        # Financial features
        if pdf_data.current_revenue:
            features['revenue'] = pdf_data.current_revenue
            features['current_revenue_usd'] = pdf_data.current_revenue
        
        if pdf_data.projected_revenue_y1:
            features['projected_revenue_y1'] = pdf_data.projected_revenue_y1
        
        if pdf_data.projected_revenue_y3:
            features['projected_revenue_y3'] = pdf_data.projected_revenue_y3
        
        # Calculate growth rate if possible
        if pdf_data.current_revenue and pdf_data.projected_revenue_y1:
            growth_rate = (pdf_data.projected_revenue_y1 / pdf_data.current_revenue) - 1
            features['growth_rate'] = growth_rate
            features['revenue_growth_rate'] = growth_rate
        
        # Funding features
        if pdf_data.funding_requested:
            features['funding_total'] = pdf_data.funding_requested
            features['funding_total_usd'] = pdf_data.funding_requested
        
        if pdf_data.funding_to_date:
            features['funding_rounds'] = 1  # Assume at least one round if they have funding
        
        # Market features
        if pdf_data.market_size_tam:
            features['market_size'] = pdf_data.market_size_tam / 1e9  # Convert to billions
            features['market_size_billions'] = pdf_data.market_size_tam / 1e9
        
        if pdf_data.market_size_sam:
            features['addressable_market_billions'] = pdf_data.market_size_sam / 1e9
        
        # Business features
        if pdf_data.team_size:
            features['team_size'] = pdf_data.team_size
        
        if pdf_data.customers:
            features['customers'] = pdf_data.customers
            # Derive user traction score
            features['user_traction_score'] = min(pdf_data.customers / 10000, 1.0)
        
        # Financial health features
        if pdf_data.gross_margin:
            features['gross_margin_percent'] = pdf_data.gross_margin
        
        if pdf_data.burn_rate:
            features['burn_rate_monthly'] = pdf_data.burn_rate
        
        if pdf_data.runway_months:
            features['runway_months'] = pdf_data.runway_months
        
        # Business model scoring
        if pdf_data.business_model:
            features['business_model'] = pdf_data.business_model
            # Simple business model clarity score based on description length
            features['business_model_clarity'] = min(len(pdf_data.business_model) / 100, 1.0)
        
        # Product readiness estimation
        if pdf_data.current_revenue and pdf_data.current_revenue > 0:
            features['product_readiness_score'] = 0.8  # Has revenue = product ready
        elif pdf_data.customers and pdf_data.customers > 0:
            features['product_readiness_score'] = 0.6  # Has customers = partially ready
        else:
            features['product_readiness_score'] = 0.4  # Default
        
        # Confidence-based features
        features['extraction_confidence'] = pdf_data.extraction_confidence
        features['data_completeness'] = pdf_data.completeness_score
        
        logger.info(f"📊 Converted PDF data to {len(features)} ML features")
        return features
    
    def run_agent_analysis(self, startup_data: StartupData) -> Optional[Dict[str, Any]]:
        """Run agent-based analysis if available"""
        if not self.agent_orchestrator:
            logger.warning("⚠️ Agent orchestrator not available")
            return None
        
        try:
            logger.info("🤖 Running agent-based analysis...")
            start_time = time.time()
            
            # Run agent analysis
            agent_results = self.agent_orchestrator.analyze_startup(startup_data)
            
            processing_time = time.time() - start_time
            logger.info(f"✅ Agent analysis completed in {processing_time:.2f}s")
            
            return {
                'agent_results': agent_results,
                'processing_time': processing_time
            }
            
        except Exception as e:
            logger.error(f"❌ Agent analysis failed: {e}")
            return None
    
    def run_ml_prediction(self, features: Dict[str, Any]) -> ProductionPredictionResult:
        """Run ML-based success prediction"""
        try:
            logger.info("🔮 Running ML prediction...")
            start_time = time.time()
            
            # Run prediction
            prediction = self.ml_predictor.predict_startup_success(features)
            
            processing_time = time.time() - start_time
            logger.info(f"✅ ML prediction completed in {processing_time:.2f}s")
            logger.info(f"📊 Success probability: {prediction.success_probability:.1%}")
            logger.info(f"🎯 Recommendation: {prediction.investment_recommendation}")
            
            return prediction
            
        except Exception as e:
            logger.error(f"❌ ML prediction failed: {e}")
            # Return default prediction
            return ProductionPredictionResult(
                success_probability=0.5,
                success_category="Unknown",
                confidence_interval=(0.3, 0.7),
                investment_recommendation="WATCH",
                market_score=50.0,
                team_score=50.0,
                product_score=50.0,
                business_model_score=50.0,
                financial_score=50.0,
                risk_score=50.0,
                key_strengths=[],
                key_risks=[],
                improvement_areas=["Unable to complete analysis"],
                model_confidence=0.3,
                prediction_timestamp=datetime.now().isoformat(),
                model_version="error",
                feature_count=0
            )
    
    def combine_analysis_results(
        self, 
        ml_prediction: ProductionPredictionResult,
        pdf_data: Optional[ExtractedFinancialData],
        agent_analysis: Optional[Dict[str, Any]]
    ) -> Tuple[float, float]:
        """Combine results to calculate overall confidence and completeness"""
        
        confidence_scores = [ml_prediction.model_confidence]
        completeness_scores = []
        
        # Add PDF extraction confidence
        if pdf_data:
            confidence_scores.append(pdf_data.extraction_confidence)
            completeness_scores.append(pdf_data.completeness_score)
        
        # Add agent analysis confidence (if available)
        if agent_analysis and 'confidence' in agent_analysis:
            confidence_scores.append(agent_analysis['confidence'])
        
        # Calculate weighted averages
        overall_confidence = sum(confidence_scores) / len(confidence_scores)
        data_completeness = sum(completeness_scores) / len(completeness_scores) if completeness_scores else 0.5
        
        return overall_confidence, data_completeness
    
    def analyze_startup(self, input_data: ProductionAnalysisInput) -> ProductionAnalysisResult:
        """
        Main function to run comprehensive startup analysis
        """
        # Initialize analysis
        analysis_id = input_data.analysis_id or f"analysis_{int(time.time())}"
        start_time = time.time()
        timestamp = datetime.now().isoformat()
        components_used = []
        
        logger.info(f"🚀 Starting production analysis for {input_data.company_name}")
        logger.info(f"📋 Analysis ID: {analysis_id}")
        
        # Initialize results
        pdf_data = None
        agent_analysis = None
        ml_features = input_data.manual_data or {}
        
        # Add basic information to features
        ml_features.update({
            'company_name': input_data.company_name,
            'industry': input_data.industry or 'Technology',
            'description': input_data.description or ''
        })
        
        # Step 1: PDF Data Extraction
        if input_data.use_pdf_extraction and input_data.pdf_path:
            logger.info("📄 Step 1: PDF Data Extraction")
            try:
                pdf_data, pdf_features = self.extract_features_from_pdf(input_data.pdf_path)
                ml_features.update(pdf_features)
                components_used.append("PDF_EXTRACTION")
            except Exception as e:
                logger.error(f"PDF extraction failed: {e}")
        
        # Step 2: Agent Analysis (if available and enabled)
        if input_data.use_ai_agents and AGENTS_AVAILABLE:
            logger.info("🤖 Step 2: AI Agent Analysis")
            try:
                startup_data = StartupData(
                    company_name=input_data.company_name,
                    industry=input_data.industry or 'Technology',
                    description=input_data.description or ''
                )
                agent_analysis = self.run_agent_analysis(startup_data)
                components_used.append("AI_AGENTS")
            except Exception as e:
                logger.error(f"Agent analysis failed: {e}")
        
        # Step 3: ML Prediction
        if input_data.use_ml_prediction:
            logger.info("🔮 Step 3: ML Success Prediction")
            ml_prediction = self.run_ml_prediction(ml_features)
            components_used.append("ML_PREDICTION")
        else:
            # Create dummy prediction
            ml_prediction = ProductionPredictionResult(
                success_probability=0.5,
                success_category="Analysis Skipped",
                confidence_interval=(0.4, 0.6),
                investment_recommendation="WATCH",
                market_score=50.0,
                team_score=50.0,
                product_score=50.0,
                business_model_score=50.0,
                financial_score=50.0,
                risk_score=50.0,
                key_strengths=[],
                key_risks=[],
                improvement_areas=[],
                model_confidence=0.5,
                prediction_timestamp=timestamp,
                model_version=self.version,
                feature_count=len(ml_features)
            )
        
        # Step 4: Combine Results
        logger.info("🔄 Step 4: Combining Analysis Results")
        overall_confidence, data_completeness = self.combine_analysis_results(
            ml_prediction, pdf_data, agent_analysis
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Create final result
        result = ProductionAnalysisResult(
            analysis_id=analysis_id,
            company_name=input_data.company_name,
            timestamp=timestamp,
            ml_prediction=ml_prediction,
            pdf_data=pdf_data,
            agent_analysis=agent_analysis,
            processing_time_seconds=processing_time,
            pipeline_version=self.version,
            components_used=components_used,
            overall_confidence=overall_confidence,
            data_completeness=data_completeness
        )
        
        # Update pipeline statistics
        self.analysis_count += 1
        self.total_processing_time += processing_time
        
        logger.info(f"✅ Analysis completed in {processing_time:.2f}s")
        logger.info(f"📊 Overall confidence: {overall_confidence:.1%}")
        logger.info(f"📈 Success probability: {ml_prediction.success_probability:.1%}")
        logger.info(f"🎯 Recommendation: {ml_prediction.investment_recommendation}")
        
        return result
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get pipeline performance statistics"""
        avg_processing_time = self.total_processing_time / self.analysis_count if self.analysis_count > 0 else 0
        
        return {
            'version': self.version,
            'total_analyses': self.analysis_count,
            'total_processing_time': self.total_processing_time,
            'average_processing_time': avg_processing_time,
            'components_available': {
                'pdf_extraction': True,
                'ml_prediction': True,
                'ai_agents': AGENTS_AVAILABLE
            }
        }
    
    async def analyze_startup_async(self, input_data: ProductionAnalysisInput) -> ProductionAnalysisResult:
        """Async version of startup analysis"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.analyze_startup, input_data)

# Global pipeline instance
_global_pipeline = None

def get_production_pipeline() -> ProductionMLPipeline:
    """Get or create global pipeline instance"""
    global _global_pipeline
    if _global_pipeline is None:
        _global_pipeline = ProductionMLPipeline()
    return _global_pipeline

def analyze_startup_production(
    company_name: str,
    pdf_path: Optional[str] = None,
    industry: Optional[str] = None,
    description: Optional[str] = None,
    manual_data: Optional[Dict[str, Any]] = None
) -> ProductionAnalysisResult:
    """
    Convenience function for production startup analysis
    """
    pipeline = get_production_pipeline()
    
    input_data = ProductionAnalysisInput(
        company_name=company_name,
        industry=industry,
        description=description,
        pdf_path=pdf_path,
        manual_data=manual_data,
        analysis_id=f"prod_{int(time.time())}"
    )
    
    return pipeline.analyze_startup(input_data)

if __name__ == "__main__":
    # Test the production pipeline
    import sys
    
    # Test with sample data
    test_input = ProductionAnalysisInput(
        company_name="TestStartup AI",
        industry="Technology",
        description="AI-powered startup analysis platform",
        manual_data={
            'revenue': 500000,
            'market_size': 5.0,
            'team_size': 8,
            'founder_experience': 7
        }
    )
    
    # If PDF path provided, test with PDF
    if len(sys.argv) > 1:
        test_input.pdf_path = sys.argv[1]
    
    print("🚀 Testing Production ML Pipeline")
    
    pipeline = ProductionMLPipeline()
    result = pipeline.analyze_startup(test_input)
    
    print(f"\n📊 Analysis Results for {result.company_name}:")
    print(f"  Analysis ID: {result.analysis_id}")
    print(f"  Processing Time: {result.processing_time_seconds:.2f}s")
    print(f"  Components Used: {', '.join(result.components_used)}")
    print(f"  Overall Confidence: {result.overall_confidence:.1%}")
    print(f"  Data Completeness: {result.data_completeness:.1%}")
    print(f"\n🎯 ML Prediction:")
    print(f"  Success Probability: {result.ml_prediction.success_probability:.1%}")
    print(f"  Category: {result.ml_prediction.success_category}")
    print(f"  Recommendation: {result.ml_prediction.investment_recommendation}")
    print(f"  Market Score: {result.ml_prediction.market_score:.1f}/100")
    print(f"  Team Score: {result.ml_prediction.team_score:.1f}/100")
    print(f"  Product Score: {result.ml_prediction.product_score:.1f}/100")
    
    # Print pipeline stats
    stats = pipeline.get_pipeline_stats()
    print(f"\n📈 Pipeline Statistics:")
    print(f"  Version: {stats['version']}")
    print(f"  Total Analyses: {stats['total_analyses']}")
    print(f"  Average Processing Time: {stats['average_processing_time']:.2f}s")
