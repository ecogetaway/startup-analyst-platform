"""
Agent Orchestrator - Coordinates all analysis agents
"""
import asyncio
import concurrent.futures
from typing import Dict, Any, List
import time
import logging
from ..models.startup import StartupInput, AnalysisResults
from .data_collection_agent import DataCollectionAgent
from .business_analysis_agent import BusinessAnalysisAgent
from .risk_assessment_agent import RiskAssessmentAgent
from .investment_insights_agent import InvestmentInsightsAgent
from .report_generation_agent import ReportGenerationAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """Orchestrates all analysis agents for startup evaluation"""
    
    def __init__(self):
        """Initialize the orchestrator with all agents"""
        self.agents = {
            "data_collection": DataCollectionAgent(),
            "business_analysis": BusinessAnalysisAgent(),
            "risk_assessment": RiskAssessmentAgent(),
            "investment_insights": InvestmentInsightsAgent(),
            "report_generation": ReportGenerationAgent()
        }
        self.start_time = None
        self.end_time = None
    
    def analyze_startup(self, startup_input: StartupInput) -> AnalysisResults:
        """Run complete startup analysis using all agents"""
        self.start_time = time.time()
        
        try:
            logger.info(f"Starting comprehensive analysis for {startup_input.company_name}")
            
            # Run agents in parallel for better performance
            agent_results = self._run_agents_parallel(startup_input)
            
            # Process results and create final analysis
            analysis_results = self._process_results(startup_input, agent_results)
            
            self.end_time = time.time()
            total_time = self.end_time - self.start_time
            
            logger.info(f"Completed analysis for {startup_input.company_name} in {total_time:.2f} seconds")
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in startup analysis: {str(e)}")
            raise Exception(f"Analysis failed: {str(e)}")
    
    def _run_agents_parallel(self, startup_input: StartupInput) -> Dict[str, Dict[str, Any]]:
        """Run all agents in parallel for better performance"""
        agent_results = {}
        
        # Use ThreadPoolExecutor for parallel execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all agent tasks
            future_to_agent = {
                executor.submit(agent.analyze, startup_input): agent_name
                for agent_name, agent in self.agents.items()
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_agent):
                agent_name = future_to_agent[future]
                try:
                    result = future.result()
                    agent_results[agent_name] = result
                    logger.info(f"Completed {agent_name} analysis")
                except Exception as e:
                    logger.error(f"Error in {agent_name}: {str(e)}")
                    agent_results[agent_name] = {
                        "agent_name": agent_name,
                        "status": "error",
                        "error": str(e),
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
        
        return agent_results
    
    def _process_results(self, startup_input: StartupInput, agent_results: Dict[str, Dict[str, Any]]) -> AnalysisResults:
        """Process agent results and create final analysis"""
        try:
            # Extract analysis from each agent
            data_collection = agent_results.get("data_collection", {}).get("analysis", "")
            business_analysis = agent_results.get("business_analysis", {}).get("analysis", "")
            risk_assessment = agent_results.get("risk_assessment", {}).get("analysis", "")
            investment_insights = agent_results.get("investment_insights", {}).get("analysis", "")
            report_generation = agent_results.get("report_generation", {}).get("analysis", "")
            
            # Create structured results (simplified for now)
            from ..models.startup import MarketAnalysis, BusinessModelAnalysis, RiskAssessment, InvestmentInsights
            
            # Parse and structure the results
            market_analysis = MarketAnalysis(
                market_size="To be extracted from analysis",
                growth_rate="To be extracted from analysis",
                competition_level="To be extracted from analysis",
                market_trends="To be extracted from analysis",
                target_customers="To be extracted from analysis"
            )
            
            business_model_analysis = BusinessModelAnalysis(
                revenue_model="To be extracted from analysis",
                scalability="To be extracted from analysis",
                competitive_advantage="To be extracted from analysis",
                monetization_strategy="To be extracted from analysis",
                unit_economics="To be extracted from analysis"
            )
            
            risk_assessment_result = RiskAssessment(
                market_risk="MEDIUM",  # Default, to be extracted
                technology_risk="MEDIUM",
                financial_risk="MEDIUM",
                team_risk="MEDIUM",
                regulatory_risk="MEDIUM",
                risk_summary="To be extracted from analysis",
                mitigation_strategies=["To be extracted from analysis"]
            )
            
            investment_insights_result = InvestmentInsights(
                recommendation="WATCH",  # Default, to be extracted
                confidence_score=7.0,
                key_thesis=["To be extracted from analysis"],
                valuation_considerations="To be extracted from analysis",
                due_diligence_priorities=["To be extracted from analysis"],
                exit_potential="To be extracted from analysis"
            )
            
            # Calculate total processing time
            total_time = self.end_time - self.start_time if self.end_time and self.start_time else 0
            
            return AnalysisResults(
                startup_input=startup_input,
                market_analysis=market_analysis,
                business_model_analysis=business_model_analysis,
                risk_assessment=risk_assessment_result,
                investment_insights=investment_insights_result,
                analysis_timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                processing_time=total_time,
                agent_results=agent_results
            )
            
        except Exception as e:
            logger.error(f"Error processing results: {str(e)}")
            raise Exception(f"Result processing failed: {str(e)}")
    
    def get_agent_status(self) -> Dict[str, str]:
        """Get status of all agents"""
        return {
            agent_name: "ready" for agent_name in self.agents.keys()
        }
    
    def get_processing_time(self) -> float:
        """Get total processing time"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
