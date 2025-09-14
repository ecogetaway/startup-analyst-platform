"""
Investment Insights Agent - Generates actionable investment recommendations
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..models.startup import StartupInput

class InvestmentInsightsAgent(BaseAgent):
    """Agent responsible for generating investment insights and recommendations"""
    
    def __init__(self):
        super().__init__(
            name="Investment Insights Agent",
            description="Generates actionable investment recommendations and insights"
        )
    
    def analyze(self, startup_input: StartupInput) -> Dict[str, Any]:
        """Generate investment insights and recommendations"""
        return self._execute_analysis(startup_input)
    
    def _create_system_instruction(self) -> str:
        """Create system instruction for investment insights"""
        return """You are an Investment Insights Agent specializing in startup investment recommendations.

Your role is to:
1. Synthesize all analysis results
2. Generate investment recommendations (Invest/Pass/Watch)
3. Provide key investment thesis
4. Assess valuation considerations
5. Identify due diligence priorities

Focus on:
- Investment recommendation with clear reasoning
- Key investment thesis points
- Valuation considerations and comparables
- Due diligence priorities
- Exit potential and timeline
- Risk-return profile

Provide actionable insights for investment decision-making.
"""
    
    def _create_prompt(self, startup_input: StartupInput) -> str:
        """Create investment insights prompt"""
        return f"""Please provide comprehensive investment insights for this startup:

COMPANY: {startup_input.company_name}
BUSINESS: {startup_input.business_description}
INDUSTRY: {startup_input.industry or 'Not specified'}
STAGE: {startup_input.stage or 'Not specified'}

Please provide detailed investment insights including:

1. INVESTMENT RECOMMENDATION
   - Recommendation: INVEST/PASS/WATCH
   - Confidence Score: 1-10
   - Reasoning: Clear justification for the recommendation
   - Key factors: Most important decision factors

2. KEY INVESTMENT THESIS
   - Market opportunity thesis
   - Competitive advantage thesis
   - Team strength thesis
   - Business model thesis
   - Execution capability thesis

3. VALUATION CONSIDERATIONS
   - Comparable company analysis
   - Revenue multiples
   - Growth potential
   - Risk adjustments
   - Valuation range
   - Key value drivers

4. DUE DILIGENCE PRIORITIES
   - Financial verification priorities
   - Market validation priorities
   - Technology assessment priorities
   - Legal and regulatory priorities
   - Team verification priorities

5. EXIT POTENTIAL
   - Potential exit scenarios
   - Exit timeline estimates
   - Exit valuation potential
   - Strategic acquirer analysis
   - IPO potential assessment

6. RISK-RETURN PROFILE
   - Expected return potential
   - Risk level assessment
   - Risk-return ratio
   - Portfolio fit analysis
   - Diversification benefits

7. INVESTMENT TERMS CONSIDERATIONS
   - Preferred investment structure
   - Key terms to negotiate
   - Board representation
   - Liquidation preferences
   - Anti-dilution provisions

8. MONITORING AND SUPPORT
   - Key metrics to track
   - Support requirements
   - Milestone expectations
   - Follow-on investment considerations
   - Value-add opportunities

Provide specific, actionable insights with clear reasoning and supporting evidence.
"""
