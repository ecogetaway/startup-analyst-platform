"""
Data models for startup analysis
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class InvestmentRecommendation(str, Enum):
    INVEST = "INVEST"
    PASS = "PASS"
    WATCH = "WATCH"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class StartupInput(BaseModel):
    """Input data for startup analysis"""
    company_name: str = Field(..., description="Name of the startup company")
    business_description: str = Field(..., description="Description of the business")
    industry: Optional[str] = Field(None, description="Industry sector")
    stage: Optional[str] = Field(None, description="Funding stage (seed, series A, etc.)")
    founder_name: Optional[str] = Field(None, description="Founder name")
    founder_background: Optional[str] = Field(None, description="Founder background and experience")
    website: Optional[str] = Field(None, description="Company website URL")
    pitch_deck_url: Optional[str] = Field(None, description="URL to pitch deck")
    additional_info: Optional[str] = Field(None, description="Additional information")

class MarketAnalysis(BaseModel):
    """Market analysis results"""
    market_size: Optional[str] = Field(None, description="Total addressable market size")
    growth_rate: Optional[str] = Field(None, description="Market growth rate")
    competition_level: Optional[str] = Field(None, description="Level of competition")
    market_trends: Optional[str] = Field(None, description="Key market trends")
    target_customers: Optional[str] = Field(None, description="Target customer segments")

class BusinessModelAnalysis(BaseModel):
    """Business model analysis results"""
    revenue_model: Optional[str] = Field(None, description="How the company makes money")
    scalability: Optional[str] = Field(None, description="Business model scalability")
    competitive_advantage: Optional[str] = Field(None, description="Unique competitive advantages")
    monetization_strategy: Optional[str] = Field(None, description="Monetization strategy")
    unit_economics: Optional[str] = Field(None, description="Unit economics analysis")

class RiskAssessment(BaseModel):
    """Risk assessment results"""
    market_risk: RiskLevel = Field(..., description="Market-related risks")
    technology_risk: RiskLevel = Field(..., description="Technology-related risks")
    financial_risk: RiskLevel = Field(..., description="Financial risks")
    team_risk: RiskLevel = Field(..., description="Team-related risks")
    regulatory_risk: RiskLevel = Field(..., description="Regulatory risks")
    risk_summary: str = Field(..., description="Overall risk assessment summary")
    mitigation_strategies: List[str] = Field(default_factory=list, description="Risk mitigation strategies")

class InvestmentInsights(BaseModel):
    """Investment insights and recommendations"""
    recommendation: InvestmentRecommendation = Field(..., description="Investment recommendation")
    confidence_score: float = Field(..., ge=0, le=10, description="Confidence score (0-10)")
    key_thesis: List[str] = Field(..., description="Key investment thesis points")
    valuation_considerations: Optional[str] = Field(None, description="Valuation considerations")
    due_diligence_priorities: List[str] = Field(default_factory=list, description="Due diligence priorities")
    exit_potential: Optional[str] = Field(None, description="Exit potential analysis")

class AnalysisResults(BaseModel):
    """Complete analysis results"""
    startup_input: StartupInput = Field(..., description="Original startup input data")
    market_analysis: MarketAnalysis = Field(..., description="Market analysis results")
    business_model_analysis: BusinessModelAnalysis = Field(..., description="Business model analysis")
    risk_assessment: RiskAssessment = Field(..., description="Risk assessment results")
    investment_insights: InvestmentInsights = Field(..., description="Investment insights")
    analysis_timestamp: str = Field(..., description="When the analysis was performed")
    processing_time: float = Field(..., description="Total processing time in seconds")
    agent_results: Dict[str, Any] = Field(default_factory=dict, description="Individual agent results")
