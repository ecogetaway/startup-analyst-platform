"""
Base agent class for startup analysis
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
import logging
from ..utils.ai_client import AIClient
from ..models.startup import StartupInput

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all analysis agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.ai_client = AIClient()
        self.start_time = None
        self.end_time = None
    
    @abstractmethod
    def analyze(self, startup_input: StartupInput) -> Dict[str, Any]:
        """Analyze startup data and return results"""
        pass
    
    def _create_system_instruction(self) -> str:
        """Create system instruction for the agent"""
        return f"""You are a {self.name} - {self.description}.
        
        Your role is to provide expert analysis for startup investment decisions.
        Be thorough, objective, and provide actionable insights.
        Focus on facts and data-driven analysis.
        """
    
    def _create_prompt(self, startup_input: StartupInput) -> str:
        """Create analysis prompt for the agent"""
        return f"""Please analyze the following startup information:

Company Name: {startup_input.company_name}
Business Description: {startup_input.business_description}
Industry: {startup_input.industry or 'Not specified'}
Stage: {startup_input.stage or 'Not specified'}
Founder: {startup_input.founder_name or 'Not specified'}
Founder Background: {startup_input.founder_background or 'Not specified'}
Website: {startup_input.website or 'Not specified'}
Additional Info: {startup_input.additional_info or 'None'}

Please provide a comprehensive analysis focusing on your area of expertise.
"""
    
    def _execute_analysis(self, startup_input: StartupInput) -> Dict[str, Any]:
        """Execute the analysis with timing"""
        self.start_time = time.time()
        
        try:
            logger.info(f"Starting {self.name} analysis for {startup_input.company_name}")
            
            system_instruction = self._create_system_instruction()
            prompt = self._create_prompt(startup_input)
            
            # Get AI response
            response = self.ai_client.analyze_with_retry(prompt, system_instruction)
            
            self.end_time = time.time()
            processing_time = self.end_time - self.start_time
            
            logger.info(f"Completed {self.name} analysis in {processing_time:.2f} seconds")
            
            return {
                "agent_name": self.name,
                "status": "completed",
                "processing_time": processing_time,
                "analysis": response,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            self.end_time = time.time()
            processing_time = self.end_time - self.start_time if self.start_time else 0
            
            logger.error(f"Error in {self.name} analysis: {str(e)}")
            
            return {
                "agent_name": self.name,
                "status": "error",
                "processing_time": processing_time,
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def get_processing_time(self) -> Optional[float]:
        """Get the processing time for this agent"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
