"""
Business Analysis Agent - Evaluates business model and strategy
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..models.startup import StartupInput

class BusinessAnalysisAgent(BaseAgent):
    """Agent responsible for business model and strategy analysis"""
    
    def __init__(self):
        super().__init__(
            name="Business Analysis Agent",
            description="Evaluates business model, strategy, and market opportunity"
        )
    
    def analyze(self, startup_input: StartupInput) -> Dict[str, Any]:
        """Analyze business model and strategy"""
        return self._execute_analysis(startup_input)
    
    def _create_system_instruction(self) -> str:
        """Create system instruction for business analysis"""
        return """You are a Business Analysis Agent specializing in startup business model evaluation.

Your role is to:
1. Evaluate the business model and strategy
2. Assess market opportunity and scalability
3. Analyze revenue streams and monetization
4. Evaluate competitive positioning
5. Assess execution capability

Focus on:
- Business model viability
- Market opportunity size and accessibility
- Revenue model and unit economics
- Scalability and growth potential
- Competitive advantages and moats
- Execution risk and capability
- Go-to-market strategy

Provide scores (1-10) for different business aspects and detailed analysis.
"""
    
    def _create_prompt(self, startup_input: StartupInput) -> str:
        """Create business analysis prompt"""
        return f"""Please conduct a comprehensive business analysis for this startup:

COMPANY: {startup_input.company_name}
BUSINESS: {startup_input.business_description}
INDUSTRY: {startup_input.industry or 'Not specified'}
STAGE: {startup_input.stage or 'Not specified'}

Please provide a detailed business analysis including:

1. BUSINESS MODEL ANALYSIS
   - Revenue model and streams
   - Value proposition
   - Customer acquisition strategy
   - Unit economics
   - Scalability assessment

2. MARKET OPPORTUNITY (Score 1-10)
   - Total addressable market (TAM)
   - Serviceable addressable market (SAM)
   - Serviceable obtainable market (SOM)
   - Market growth rate and trends
   - Market accessibility

3. COMPETITIVE POSITIONING (Score 1-10)
   - Competitive landscape
   - Unique value proposition
   - Competitive advantages
   - Barriers to entry
   - Market differentiation

4. EXECUTION CAPABILITY (Score 1-10)
   - Team strength and experience
   - Product-market fit
   - Go-to-market strategy
   - Operational capability
   - Track record

5. FINANCIAL VIABILITY (Score 1-10)
   - Revenue potential
   - Cost structure
   - Profitability path
   - Funding requirements
   - Return on investment

6. RISK ASSESSMENT
   - Business model risks
   - Market risks
   - Execution risks
   - Financial risks
   - Mitigation strategies

7. GROWTH POTENTIAL (Score 1-10)
   - Scalability factors
   - Expansion opportunities
   - International potential
   - Product line extensions
   - Market expansion

Provide specific scores (1-10) for each category and detailed reasoning for your assessments.
"""
