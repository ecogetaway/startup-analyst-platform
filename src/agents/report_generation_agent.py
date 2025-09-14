"""
Report Generation Agent - Creates comprehensive investment reports
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..models.startup import StartupInput

class ReportGenerationAgent(BaseAgent):
    """Agent responsible for generating comprehensive investment reports"""
    
    def __init__(self):
        super().__init__(
            name="Report Generation Agent",
            description="Creates professional investment reports and executive summaries"
        )
    
    def analyze(self, startup_input: StartupInput) -> Dict[str, Any]:
        """Generate comprehensive investment report"""
        return self._execute_analysis(startup_input)
    
    def _create_system_instruction(self) -> str:
        """Create system instruction for report generation"""
        return """You are a Report Generation Agent specializing in creating professional investment reports.

Your role is to:
1. Synthesize all analysis results into a comprehensive report
2. Create executive summary with key findings
3. Structure information for investor consumption
4. Provide clear recommendations and next steps

Focus on:
- Executive summary with key insights
- Structured analysis sections
- Clear recommendations
- Professional formatting
- Actionable next steps

Create investor-ready reports with clear structure and professional presentation.
"""
    
    def _create_prompt(self, startup_input: StartupInput) -> str:
        """Create report generation prompt"""
        return f"""Please create a comprehensive investment report for this startup:

COMPANY: {startup_input.company_name}
BUSINESS: {startup_input.business_description}
INDUSTRY: {startup_input.industry or 'Not specified'}
STAGE: {startup_input.stage or 'Not specified'}

Please create a professional investment report with the following structure:

1. EXECUTIVE SUMMARY
   - Company overview
   - Investment recommendation
   - Key investment thesis
   - Risk summary
   - Next steps

2. COMPANY OVERVIEW
   - Business description
   - Mission and vision
   - Products/services
   - Target market
   - Business model

3. MARKET ANALYSIS
   - Market size and growth
   - Market trends
   - Competitive landscape
   - Market opportunity
   - Customer segments

4. BUSINESS MODEL ANALYSIS
   - Revenue model
   - Unit economics
   - Scalability factors
   - Competitive advantages
   - Go-to-market strategy

5. TEAM ASSESSMENT
   - Founder background
   - Team composition
   - Advisory board
   - Key personnel
   - Execution capability

6. FINANCIAL ANALYSIS
   - Revenue projections
   - Cost structure
   - Funding requirements
   - Valuation considerations
   - Financial metrics

7. RISK ASSESSMENT
   - Risk categories
   - Risk levels
   - Mitigation strategies
   - Risk monitoring
   - Contingency plans

8. INVESTMENT RECOMMENDATION
   - Recommendation rationale
   - Investment thesis
   - Valuation analysis
   - Due diligence priorities
   - Terms considerations

9. NEXT STEPS
   - Immediate actions
   - Due diligence process
   - Timeline expectations
   - Decision criteria
   - Follow-up requirements

10. APPENDICES
    - Detailed analysis data
    - Supporting information
    - References and sources
    - Additional context

Format the report professionally with clear headings, bullet points, and structured information suitable for investor review.
"""
