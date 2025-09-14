"""
Risk Assessment Agent - Identifies potential risks and challenges
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..models.startup import StartupInput

class RiskAssessmentAgent(BaseAgent):
    """Agent responsible for risk assessment and mitigation strategies"""
    
    def __init__(self):
        super().__init__(
            name="Risk Assessment Agent",
            description="Identifies potential risks and provides mitigation strategies"
        )
    
    def analyze(self, startup_input: StartupInput) -> Dict[str, Any]:
        """Assess risks and provide mitigation strategies"""
        return self._execute_analysis(startup_input)
    
    def _create_system_instruction(self) -> str:
        """Create system instruction for risk assessment"""
        return """You are a Risk Assessment Agent specializing in startup risk evaluation.

Your role is to:
1. Identify potential risks across multiple categories
2. Assess risk levels (Low/Medium/High)
3. Provide mitigation strategies
4. Evaluate overall risk profile

Focus on:
- Market risks
- Technology risks
- Financial risks
- Team risks
- Regulatory risks
- Operational risks
- Competitive risks

Provide clear risk levels and actionable mitigation strategies.
"""
    
    def _create_prompt(self, startup_input: StartupInput) -> str:
        """Create risk assessment prompt"""
        return f"""Please conduct a comprehensive risk assessment for this startup:

COMPANY: {startup_input.company_name}
BUSINESS: {startup_input.business_description}
INDUSTRY: {startup_input.industry or 'Not specified'}
STAGE: {startup_input.stage or 'Not specified'}
FOUNDER: {startup_input.founder_name or 'Not specified'}

Please provide a detailed risk assessment including:

1. MARKET RISKS (Rate: Low/Medium/High)
   - Market size and growth risks
   - Customer adoption risks
   - Market timing risks
   - Competitive threats
   - Economic sensitivity

2. TECHNOLOGY RISKS (Rate: Low/Medium/High)
   - Technical feasibility
   - Scalability challenges
   - Technology obsolescence
   - Intellectual property risks
   - Development timeline risks

3. FINANCIAL RISKS (Rate: Low/Medium/High)
   - Revenue model risks
   - Funding risks
   - Cash flow risks
   - Unit economics risks
   - Valuation risks

4. TEAM RISKS (Rate: Low/Medium/High)
   - Founder experience gaps
   - Team composition risks
   - Key person dependency
   - Execution capability
   - Leadership risks

5. REGULATORY RISKS (Rate: Low/Medium/High)
   - Compliance requirements
   - Regulatory changes
   - Legal challenges
   - Industry regulations
   - International regulations

6. OPERATIONAL RISKS (Rate: Low/Medium/High)
   - Execution risks
   - Operational scalability
   - Supply chain risks
   - Customer service risks
   - Quality control risks

7. COMPETITIVE RISKS (Rate: Low/Medium/High)
   - Competitive response
   - Market saturation
   - New entrants
   - Substitute products
   - Competitive advantages

8. OVERALL RISK SUMMARY
   - Overall risk level
   - Key risk factors
   - Risk correlation
   - Risk mitigation priorities

9. MITIGATION STRATEGIES
   - Specific mitigation actions
   - Risk monitoring approaches
   - Contingency plans
   - Risk transfer options
   - Risk acceptance criteria

Provide clear risk levels (Low/Medium/High) for each category and specific mitigation strategies.
"""
