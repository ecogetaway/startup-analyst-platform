"""
Data Collection Agent - Synthesizes founder materials and public data
"""
from typing import Dict, Any
import requests
from .base_agent import BaseAgent
from ..models.startup import StartupInput

class DataCollectionAgent(BaseAgent):
    """Agent responsible for collecting and synthesizing startup data"""
    
    def __init__(self):
        super().__init__(
            name="Data Collection Agent",
            description="Synthesizes founder materials and public data to gather comprehensive startup information"
        )
    
    def analyze(self, startup_input: StartupInput) -> Dict[str, Any]:
        """Collect and synthesize startup data"""
        return self._execute_analysis(startup_input)
    
    def _create_system_instruction(self) -> str:
        """Create system instruction for data collection"""
        return """You are a Data Collection Agent specializing in startup research and data synthesis.

Your role is to:
1. Analyze the provided startup information
2. Identify key data points and insights
3. Synthesize information from multiple sources
4. Provide a comprehensive data overview

Focus on:
- Company background and mission
- Market positioning
- Key metrics and data points
- Founder and team information
- Business model insights
- Competitive landscape
- Recent developments and news

Provide your analysis in a structured format with clear sections and actionable insights.
"""
    
    def _create_prompt(self, startup_input: StartupInput) -> str:
        """Create data collection prompt"""
        return f"""Please collect and synthesize comprehensive data about this startup:

COMPANY INFORMATION:
- Name: {startup_input.company_name}
- Business Description: {startup_input.business_description}
- Industry: {startup_input.industry or 'Not specified'}
- Stage: {startup_input.stage or 'Not specified'}

FOUNDER INFORMATION:
- Name: {startup_input.founder_name or 'Not specified'}
- Background: {startup_input.founder_background or 'Not specified'}

ADDITIONAL SOURCES:
- Website: {startup_input.website or 'Not specified'}
- Additional Info: {startup_input.additional_info or 'None'}

Please provide a comprehensive data collection analysis including:

1. COMPANY OVERVIEW
   - Mission and vision
   - Core products/services
   - Target market
   - Business model

2. MARKET ANALYSIS
   - Industry size and growth
   - Market trends
   - Competitive landscape
   - Market opportunity

3. TEAM ASSESSMENT
   - Founder experience and background
   - Team composition
   - Advisory board
   - Key personnel

4. BUSINESS METRICS
   - Revenue model
   - Key performance indicators
   - Growth metrics
   - Financial projections

5. COMPETITIVE POSITIONING
   - Direct competitors
   - Competitive advantages
   - Market differentiation
   - Barriers to entry

6. RECENT DEVELOPMENTS
   - Recent news and updates
   - Funding history
   - Partnerships
   - Product launches

Provide specific, actionable insights based on the available information.
"""
