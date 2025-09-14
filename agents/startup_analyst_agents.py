#!/usr/bin/env python3
"""
Startup Analyst Platform - AI Agents
Multi-agent system for startup analysis using Google's agentic framework
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

# Google AI imports
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import google.generativeai as genai

@dataclass
class StartupData:
    """Data structure for startup information"""
    company_name: str
    founder_name: str
    business_description: str
    pitch_deck_url: Optional[str] = None
    website_url: Optional[str] = None
    industry: Optional[str] = None
    funding_stage: Optional[str] = None
    team_size: Optional[int] = None

@dataclass
class AnalysisResult:
    """Result structure for analysis"""
    agent_name: str
    analysis_type: str
    findings: Dict[str, Any]
    confidence_score: float
    timestamp: datetime

class BaseAnalystAgent:
    """Base class for all analyst agents"""
    
    def __init__(self, agent_name: str, model_name: str = "gemini-1.5-flash"):
        self.agent_name = agent_name
        self.model_name = model_name
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Google AI model"""
        try:
            # Try Vertex AI first (for production)
            vertexai.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location="us-central1")
            self.model = GenerativeModel(self.model_name)
            print(f"✅ {self.agent_name}: Using Vertex AI")
        except Exception:
            # Fallback to Google AI SDK
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.model = genai.GenerativeModel(self.model_name)
            print(f"✅ {self.agent_name}: Using Google AI SDK")
    
    def analyze(self, startup_data: StartupData, context: Dict = None) -> AnalysisResult:
        """Base analysis method to be overridden"""
        raise NotImplementedError("Subclasses must implement analyze method")

class DataCollectionAgent(BaseAnalystAgent):
    """Agent responsible for collecting and synthesizing data"""
    
    def __init__(self):
        super().__init__("Data Collection Agent")
    
    def analyze(self, startup_data: StartupData, context: Dict = None) -> AnalysisResult:
        """Collect and synthesize startup data"""
        
        prompt = f"""
        As a data collection specialist, analyze the following startup information and gather relevant public data:
        
        Company: {startup_data.company_name}
        Founder: {startup_data.founder_name}
        Description: {startup_data.business_description}
        Industry: {startup_data.industry or 'Not specified'}
        Website: {startup_data.website_url or 'Not provided'}
        
        Please provide:
        1. Market size and growth potential
        2. Competitive landscape analysis
        3. Industry trends and opportunities
        4. Founder background and experience
        5. Company traction and milestones
        
        Format your response as structured JSON with clear categories and data points.
        """
        
        try:
            response = self.model.generate_content(prompt)
            findings = self._parse_response(response.text)
            
            return AnalysisResult(
                agent_name=self.agent_name,
                analysis_type="data_collection",
                findings=findings,
                confidence_score=0.85,
                timestamp=datetime.now()
            )
        except Exception as e:
            return AnalysisResult(
                agent_name=self.agent_name,
                analysis_type="data_collection",
                findings={"error": str(e)},
                confidence_score=0.0,
                timestamp=datetime.now()
            )
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse the AI response into structured data"""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback to structured text parsing
                return {
                    "raw_analysis": response_text,
                    "parsed": False
                }
        except:
            return {"raw_analysis": response_text, "parsed": False}

class BusinessAnalysisAgent(BaseAnalystAgent):
    """Agent for analyzing business model and strategy"""
    
    def __init__(self):
        super().__init__("Business Analysis Agent")
    
    def analyze(self, startup_data: StartupData, context: Dict = None) -> AnalysisResult:
        """Analyze business model and strategy"""
        
        prompt = f"""
        As a business analyst, evaluate the following startup's business model and strategy:
        
        Company: {startup_data.company_name}
        Description: {startup_data.business_description}
        Industry: {startup_data.industry or 'Not specified'}
        Funding Stage: {startup_data.funding_stage or 'Not specified'}
        
        Analyze:
        1. Business Model Viability
        2. Revenue Streams and Monetization
        3. Value Proposition and Differentiation
        4. Scalability and Growth Potential
        5. Market Positioning and Strategy
        
        Provide a structured analysis with scores (1-10) for each category and detailed reasoning.
        """
        
        try:
            response = self.model.generate_content(prompt)
            findings = self._parse_business_analysis(response.text)
            
            return AnalysisResult(
                agent_name=self.agent_name,
                analysis_type="business_analysis",
                findings=findings,
                confidence_score=0.90,
                timestamp=datetime.now()
            )
        except Exception as e:
            return AnalysisResult(
                agent_name=self.agent_name,
                analysis_type="business_analysis",
                findings={"error": str(e)},
                confidence_score=0.0,
                timestamp=datetime.now()
            )
    
    def _parse_business_analysis(self, response_text: str) -> Dict:
        """Parse business analysis response"""
        return {
            "analysis": response_text,
            "scores": self._extract_scores(response_text),
            "recommendations": self._extract_recommendations(response_text)
        }
    
    def _extract_scores(self, text: str) -> Dict:
        """Extract numerical scores from analysis"""
        import re
        scores = {}
        score_pattern = r'(\w+.*?):\s*(\d+)/10'
        matches = re.findall(score_pattern, text, re.IGNORECASE)
        for category, score in matches:
            scores[category.strip()] = int(score)
        return scores
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract recommendations from analysis"""
        import re
        recommendations = []
        rec_pattern = r'(?:recommend|suggest|advise).*?([^.!?]*[.!?])'
        matches = re.findall(rec_pattern, text, re.IGNORECASE)
        return matches[:5]  # Top 5 recommendations

class RiskAssessmentAgent(BaseAnalystAgent):
    """Agent for assessing risks and challenges"""
    
    def __init__(self):
        super().__init__("Risk Assessment Agent")
    
    def analyze(self, startup_data: StartupData, context: Dict = None) -> AnalysisResult:
        """Assess risks and challenges"""
        
        prompt = f"""
        As a risk assessment specialist, evaluate potential risks and challenges for this startup:
        
        Company: {startup_data.company_name}
        Description: {startup_data.business_description}
        Industry: {startup_data.industry or 'Not specified'}
        Team Size: {startup_data.team_size or 'Not specified'}
        
        Assess:
        1. Market Risks (competition, demand, timing)
        2. Technology Risks (scalability, security, obsolescence)
        3. Financial Risks (burn rate, funding, revenue)
        4. Team Risks (key person dependency, skills gap)
        5. Regulatory Risks (compliance, legal issues)
        
        Provide risk levels (Low/Medium/High) and mitigation strategies for each category.
        """
        
        try:
            response = self.model.generate_content(prompt)
            findings = self._parse_risk_analysis(response.text)
            
            return AnalysisResult(
                agent_name=self.agent_name,
                analysis_type="risk_assessment",
                findings=findings,
                confidence_score=0.88,
                timestamp=datetime.now()
            )
        except Exception as e:
            return AnalysisResult(
                agent_name=self.agent_name,
                analysis_type="risk_assessment",
                findings={"error": str(e)},
                confidence_score=0.0,
                timestamp=datetime.now()
            )
    
    def _parse_risk_analysis(self, response_text: str) -> Dict:
        """Parse risk analysis response"""
        return {
            "risk_analysis": response_text,
            "risk_levels": self._extract_risk_levels(response_text),
            "mitigation_strategies": self._extract_mitigation_strategies(response_text)
        }
    
    def _extract_risk_levels(self, text: str) -> Dict:
        """Extract risk levels from analysis"""
        import re
        risks = {}
        risk_pattern = r'(\w+.*?)\s*risk[s]?:\s*(low|medium|high)'
        matches = re.findall(risk_pattern, text, re.IGNORECASE)
        for risk_type, level in matches:
            risks[risk_type.strip()] = level.lower()
        return risks
    
    def _extract_mitigation_strategies(self, text: str) -> List[str]:
        """Extract mitigation strategies"""
        import re
        strategies = []
        strategy_pattern = r'(?:mitigate|reduce|address).*?([^.!?]*[.!?])'
        matches = re.findall(strategy_pattern, text, re.IGNORECASE)
        return matches[:5]

class InvestmentInsightsAgent(BaseAnalystAgent):
    """Agent for generating investment insights and recommendations"""
    
    def __init__(self):
        super().__init__("Investment Insights Agent")
    
    def analyze(self, startup_data: StartupData, context: Dict = None) -> AnalysisResult:
        """Generate investment insights and recommendations"""
        
        # Combine previous analysis results
        previous_analysis = context.get("previous_analysis", {}) if context else {}
        
        prompt = f"""
        As an investment analyst, provide investment insights and recommendations for this startup:
        
        Company: {startup_data.company_name}
        Description: {startup_data.business_description}
        
        Previous Analysis Results:
        {json.dumps(previous_analysis, indent=2)}
        
        Provide:
        1. Investment Recommendation (Invest/Pass/Watch)
        2. Key Investment Thesis (3-5 bullet points)
        3. Valuation Considerations
        4. Due Diligence Priorities
        5. Exit Strategy Potential
        6. Timeline and Milestones
        
        Be specific and actionable in your recommendations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            findings = self._parse_investment_insights(response.text)
            
            return AnalysisResult(
                agent_name=self.agent_name,
                analysis_type="investment_insights",
                findings=findings,
                confidence_score=0.92,
                timestamp=datetime.now()
            )
        except Exception as e:
            return AnalysisResult(
                agent_name=self.agent_name,
                analysis_type="investment_insights",
                findings={"error": str(e)},
                confidence_score=0.0,
                timestamp=datetime.now()
            )
    
    def _parse_investment_insights(self, response_text: str) -> Dict:
        """Parse investment insights response"""
        return {
            "investment_insights": response_text,
            "recommendation": self._extract_recommendation(response_text),
            "key_thesis": self._extract_key_thesis(response_text),
            "valuation_considerations": self._extract_valuation_considerations(response_text)
        }
    
    def _extract_recommendation(self, text: str) -> str:
        """Extract investment recommendation"""
        import re
        rec_pattern = r'(?:recommend|recommendation):\s*(invest|pass|watch)'
        match = re.search(rec_pattern, text, re.IGNORECASE)
        return match.group(1).lower() if match else "unknown"
    
    def _extract_key_thesis(self, text: str) -> List[str]:
        """Extract key investment thesis points"""
        import re
        thesis_points = []
        thesis_pattern = r'(?:thesis|key point)[s]?:\s*([^.!?]*[.!?])'
        matches = re.findall(thesis_pattern, text, re.IGNORECASE)
        return matches[:5]
    
    def _extract_valuation_considerations(self, text: str) -> List[str]:
        """Extract valuation considerations"""
        import re
        valuation_points = []
        val_pattern = r'(?:valuation|value).*?([^.!?]*[.!?])'
        matches = re.findall(val_pattern, text, re.IGNORECASE)
        return matches[:3]

class StartupAnalystOrchestrator:
    """Orchestrator for coordinating all analyst agents"""
    
    def __init__(self):
        self.agents = {
            "data_collection": DataCollectionAgent(),
            "business_analysis": BusinessAnalysisAgent(),
            "risk_assessment": RiskAssessmentAgent(),
            "investment_insights": InvestmentInsightsAgent()
        }
        self.analysis_results = {}
    
    def analyze_startup(self, startup_data: StartupData) -> Dict[str, AnalysisResult]:
        """Run complete startup analysis using all agents"""
        
        print(f"🚀 Starting analysis for {startup_data.company_name}")
        
        # Run agents in sequence
        results = {}
        context = {}
        
        # 1. Data Collection
        print("📊 Collecting data...")
        results["data_collection"] = self.agents["data_collection"].analyze(startup_data, context)
        context["previous_analysis"] = results["data_collection"].findings
        
        # 2. Business Analysis
        print("💼 Analyzing business model...")
        results["business_analysis"] = self.agents["business_analysis"].analyze(startup_data, context)
        context["previous_analysis"].update(results["business_analysis"].findings)
        
        # 3. Risk Assessment
        print("⚠️ Assessing risks...")
        results["risk_assessment"] = self.agents["risk_assessment"].analyze(startup_data, context)
        context["previous_analysis"].update(results["risk_assessment"].findings)
        
        # 4. Investment Insights
        print("💰 Generating investment insights...")
        results["investment_insights"] = self.agents["investment_insights"].analyze(startup_data, context)
        
        self.analysis_results = results
        print("✅ Analysis complete!")
        
        return results
    
    def generate_summary_report(self) -> str:
        """Generate a summary report from all analysis results"""
        
        if not self.analysis_results:
            return "No analysis results available"
        
        summary_prompt = f"""
        Create a comprehensive executive summary report for startup analysis based on these results:
        
        {json.dumps(self.analysis_results, indent=2, default=str)}
        
        Include:
        1. Executive Summary
        2. Key Findings
        3. Investment Recommendation
        4. Risk Assessment
        5. Next Steps
        
        Make it professional and actionable for investors.
        """
        
        try:
            # Use the investment insights agent for final summary
            response = self.agents["investment_insights"].model.generate_content(summary_prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Sample startup data
    sample_startup = StartupData(
        company_name="TechFlow Solutions",
        founder_name="Sarah Johnson",
        business_description="AI-powered workflow automation platform for small businesses",
        industry="SaaS",
        funding_stage="Seed",
        team_size=8
    )
    
    # Run analysis
    orchestrator = StartupAnalystOrchestrator()
    results = orchestrator.analyze_startup(sample_startup)
    
    # Generate summary
    summary = orchestrator.generate_summary_report()
    print("\n" + "="*60)
    print("EXECUTIVE SUMMARY")
    print("="*60)
    print(summary)
