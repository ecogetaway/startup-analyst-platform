"""
Google Agent Development Kit (ADK) Orchestrator
Advanced multi-agent system using Google's Vertex AI Agent Builder
"""
import asyncio
import time
import logging
from typing import Dict, Any, List, Optional
import json
import os

# Google Cloud imports
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part
    from google.cloud import aiplatform
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False

# Fallback to regular Google AI
import google.generativeai as genai

from ..utils.enhanced_firebase_client import enhanced_firebase_client
from ..utils.enhanced_storage_client import enhanced_storage_client

logger = logging.getLogger(__name__)

class GoogleADKAgent:
    """Individual agent using Google ADK principles"""
    
    def __init__(self, agent_type: str, agent_config: Dict[str, Any]):
        """Initialize agent with specific configuration"""
        self.agent_type = agent_type
        self.agent_config = agent_config
        self.model = None
        self.initialized = False
        
        # Initialize the appropriate model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the AI model (Vertex AI or Gemini fallback)"""
        try:
            # Try direct Gemini API first (more reliable for development)
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    self.model = genai.GenerativeModel('gemini-1.5-flash')
                    self.model_type = "gemini_direct"
                    self.initialized = True
                    logger.info(f"✅ {self.agent_type} initialized with Gemini (direct API)")
                    return
                except Exception as e:
                    logger.warning(f"⚠️ Direct Gemini API initialization failed for {self.agent_type}: {str(e)}")
            
            # Try Vertex AI as fallback
            if VERTEX_AI_AVAILABLE:
                try:
                    vertexai.init(
                        project=os.getenv('GOOGLE_CLOUD_PROJECT', 'startup-analyst-platform'),
                        location="us-central1"
                    )
                    
                    # Use Gemini through Vertex AI
                    self.model = GenerativeModel("gemini-1.5-flash")
                    self.model_type = "vertex_ai"
                    self.initialized = True
                    logger.info(f"✅ {self.agent_type} initialized with Vertex AI")
                    return
                    
                except Exception as e:
                    logger.warning(f"⚠️ Vertex AI initialization failed for {self.agent_type}: {str(e)}")
            
            # If both fail
            logger.error(f"❌ No working AI model found for {self.agent_type}")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize {self.agent_type}: {str(e)}")
    
    async def analyze(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform analysis using the agent's specialized capabilities"""
        if not self.initialized:
            raise Exception(f"Agent {self.agent_type} not initialized")
        
        start_time = time.time()
        
        try:
            # Create specialized prompt based on agent type
            prompt = self._create_specialized_prompt(input_data, context)
            system_instruction = self._get_system_instruction()
            
            # Generate response
            if self.model_type == "vertex_ai":
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": 4096,
                        "temperature": 0.7,
                        "top_p": 0.8
                    }
                )
                result_text = response.text
            else:
                # Gemini direct API - combine system instruction with prompt
                full_prompt = f"SYSTEM: {system_instruction}\n\nUSER: {prompt}"
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=4096,
                        temperature=0.7
                    )
                )
                result_text = response.text
            
            # Parse and structure the result
            processed_result = self._process_response(result_text, input_data)
            
            processing_time = time.time() - start_time
            
            return {
                "agent_type": self.agent_type,
                "status": "completed",
                "processing_time": processing_time,
                "model_used": self.model_type,
                "input_summary": self._summarize_input(input_data),
                "analysis_result": processed_result,
                "timestamp": time.time(),
                "confidence_score": self._calculate_confidence(processed_result)
            }
            
        except Exception as e:
            logger.error(f"❌ Analysis failed for {self.agent_type}: {str(e)}")
            return {
                "agent_type": self.agent_type,
                "status": "failed",
                "error": str(e),
                "processing_time": time.time() - start_time,
                "timestamp": time.time()
            }
    
    def _create_specialized_prompt(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> str:
        """Create specialized prompt based on agent type"""
        
        base_data = f"""
Company: {input_data.get('company_name', 'Unknown')}
Industry: {input_data.get('industry', 'Unknown')}
Stage: {input_data.get('stage', 'Unknown')}
Description: {input_data.get('description', 'No description provided')}
"""
        
        if self.agent_type == "data_collection":
            return f"""
{base_data}

As a Data Collection Agent, perform comprehensive market and company research:

1. MARKET ANALYSIS:
   - Industry size and growth trends
   - Key market drivers and challenges
   - Competitive landscape overview
   - Market opportunity assessment

2. COMPANY DATA COMPILATION:
   - Business model analysis
   - Revenue streams identification
   - Target customer segments
   - Operational metrics

3. FINANCIAL DATA GATHERING:
   - Funding history research
   - Revenue and growth metrics
   - Cost structure analysis
   - Key financial ratios

4. TECHNOLOGY ASSESSMENT:
   - Technical infrastructure evaluation
   - Innovation and IP analysis
   - Technology competitive advantages
   - Development roadmap insights

Provide structured, data-driven insights in JSON format.
"""
        
        elif self.agent_type == "business_analysis":
            context_data = context.get('data_collection', {}) if context else {}
            return f"""
{base_data}

Previous Research Context:
{json.dumps(context_data, indent=2) if context_data else 'No previous context'}

As a Business Analysis Agent, conduct deep business model evaluation:

1. BUSINESS MODEL VIABILITY:
   - Revenue model sustainability
   - Scalability assessment
   - Unit economics analysis
   - Customer acquisition strategy

2. COMPETITIVE POSITIONING:
   - Unique value proposition
   - Competitive advantages
   - Market differentiation
   - Barriers to entry

3. OPERATIONAL EFFICIENCY:
   - Process optimization opportunities
   - Resource utilization
   - Operational scalability
   - Cost structure optimization

4. STRATEGIC RECOMMENDATIONS:
   - Growth strategy recommendations
   - Market expansion opportunities
   - Partnership possibilities
   - Strategic positioning advice

Provide comprehensive business analysis in structured format.
"""
        
        elif self.agent_type == "risk_assessment":
            return f"""
{base_data}

As a Risk Assessment Agent, evaluate comprehensive risk factors:

1. MARKET RISKS:
   - Market volatility and cyclicality
   - Competitive threats
   - Regulatory changes
   - Economic sensitivity

2. OPERATIONAL RISKS:
   - Execution risks
   - Technology risks
   - Operational scalability challenges
   - Key person dependencies

3. FINANCIAL RISKS:
   - Cash flow risks
   - Funding requirements
   - Financial model assumptions
   - Return on investment risks

4. STRATEGIC RISKS:
   - Business model risks
   - Market timing risks
   - Partnership dependencies
   - Exit strategy challenges

5. RISK MITIGATION:
   - Risk mitigation strategies
   - Contingency planning
   - Risk monitoring frameworks
   - Insurance and protection needs

Provide detailed risk analysis with mitigation recommendations.
"""
        
        elif self.agent_type == "investment_insights":
            business_context = context.get('business_analysis', {}) if context else {}
            risk_context = context.get('risk_assessment', {}) if context else {}
            
            return f"""
{base_data}

Business Analysis Context:
{json.dumps(business_context, indent=2) if business_context else 'No business context'}

Risk Assessment Context:
{json.dumps(risk_context, indent=2) if risk_context else 'No risk context'}

As an Investment Insights Agent, provide investment recommendation:

1. INVESTMENT ATTRACTIVENESS:
   - Investment thesis development
   - Value creation potential
   - Market opportunity sizing
   - Competitive positioning strength

2. VALUATION ANALYSIS:
   - Comparable company analysis
   - DCF valuation framework
   - Multiple-based valuation
   - Risk-adjusted returns

3. INVESTMENT STRUCTURE:
   - Recommended investment amount
   - Equity vs debt considerations
   - Board representation needs
   - Liquidation preferences

4. VALUE-ADD OPPORTUNITIES:
   - Strategic value creation
   - Operational improvements
   - Market expansion support
   - Exit strategy planning

5. INVESTMENT RECOMMENDATION:
   - Clear invest/don't invest decision
   - Investment conditions and terms
   - Due diligence priorities
   - Timeline recommendations

Provide definitive investment recommendation with detailed rationale.
"""
        
        elif self.agent_type == "report_generation":
            all_context = context or {}
            return f"""
{base_data}

Complete Analysis Context:
{json.dumps(all_context, indent=2)}

As a Report Generation Agent, create executive investment summary:

1. EXECUTIVE SUMMARY:
   - Investment recommendation (INVEST/DON'T INVEST/CONDITIONAL)
   - Key investment highlights
   - Critical success factors
   - Primary concerns

2. INVESTMENT THESIS:
   - Market opportunity summary
   - Business model strengths
   - Competitive advantages
   - Growth potential

3. KEY METRICS DASHBOARD:
   - Financial projections summary
   - Market size and TAM
   - Unit economics
   - Growth metrics

4. RISK SUMMARY:
   - Top 3 risks and mitigations
   - Risk rating (Low/Medium/High)
   - Monitoring requirements

5. RECOMMENDATION DETAILS:
   - Investment amount and structure
   - Expected returns
   - Timeline and milestones
   - Next steps

Create a professional, investor-ready report that synthesizes all analysis.
"""
        
        else:
            return f"{base_data}\n\nPerform general analysis for agent type: {self.agent_type}"
    
    def _get_system_instruction(self) -> str:
        """Get system instruction for the agent"""
        instructions = {
            "data_collection": "You are an expert market research and data collection specialist. Provide thorough, accurate, and well-structured market and company data.",
            "business_analysis": "You are a seasoned business strategy consultant. Analyze business models with deep commercial insight and practical recommendations.",
            "risk_assessment": "You are a risk management expert with extensive experience in startup and investment risk evaluation. Be thorough and realistic.",
            "investment_insights": "You are a senior investment professional with 15+ years of venture capital and private equity experience. Provide institutional-quality investment analysis.",
            "report_generation": "You are an executive report writer specializing in investment committee presentations. Create clear, professional, actionable reports."
        }
        
        base_instruction = instructions.get(self.agent_type, "You are an AI analyst.")
        
        return f"{base_instruction} Always provide structured, professional output suitable for executive decision-making. Be specific, data-driven, and actionable in your recommendations."
    
    def _process_response(self, response_text: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and structure the AI response"""
        # Try to extract JSON if present
        try:
            # Look for JSON blocks
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_data = json.loads(json_match.group())
                return {
                    "structured_data": json_data,
                    "raw_analysis": response_text,
                    "format": "json"
                }
        except:
            pass
        
        # If no JSON, structure the text response
        return {
            "analysis": response_text,
            "summary": response_text[:500] + "..." if len(response_text) > 500 else response_text,
            "format": "text",
            "word_count": len(response_text.split()),
            "key_points": self._extract_key_points(response_text)
        }
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from text"""
        # Simple extraction based on numbered lists, bullet points, etc.
        import re
        
        key_points = []
        
        # Look for numbered points
        numbered_points = re.findall(r'\d+\.\s*([^\n]+)', text)
        key_points.extend(numbered_points[:5])  # Top 5
        
        # Look for bullet points
        bullet_points = re.findall(r'[-•]\s*([^\n]+)', text)
        key_points.extend(bullet_points[:3])  # Top 3
        
        return key_points[:5]  # Return max 5 key points
    
    def _summarize_input(self, input_data: Dict[str, Any]) -> str:
        """Create a brief summary of input data"""
        return f"{input_data.get('company_name', 'Unknown')} - {input_data.get('industry', 'Unknown')} ({input_data.get('stage', 'Unknown')})"
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence score for the analysis"""
        # Simple heuristic based on content completeness
        score = 0.5  # Base score
        
        if result.get('format') == 'json':
            score += 0.2
        
        if result.get('word_count', 0) > 200:
            score += 0.2
        
        if len(result.get('key_points', [])) >= 3:
            score += 0.1
        
        return min(score, 1.0)


class GoogleADKOrchestrator:
    """Google Agent Development Kit Orchestrator for multi-agent workflows"""
    
    def __init__(self):
        """Initialize the ADK orchestrator with specialized agents"""
        self.agents = {}
        self.initialized = False
        
        # Agent configurations
        agent_configs = {
            "data_collection": {
                "specialty": "market_research",
                "priority": 1,
                "timeout": 30
            },
            "business_analysis": {
                "specialty": "business_strategy",
                "priority": 2,
                "timeout": 30
            },
            "risk_assessment": {
                "specialty": "risk_management",
                "priority": 2,
                "timeout": 30
            },
            "investment_insights": {
                "specialty": "investment_analysis",
                "priority": 3,
                "timeout": 30
            },
            "report_generation": {
                "specialty": "executive_reporting",
                "priority": 4,
                "timeout": 30
            }
        }
        
        # Initialize agents
        self._initialize_agents(agent_configs)
    
    def _initialize_agents(self, agent_configs: Dict[str, Dict[str, Any]]):
        """Initialize all specialized agents"""
        try:
            for agent_type, config in agent_configs.items():
                agent = GoogleADKAgent(agent_type, config)
                if agent.initialized:
                    self.agents[agent_type] = agent
                    logger.info(f"✅ {agent_type.title()} Agent initialized")
                else:
                    logger.warning(f"⚠️ {agent_type.title()} Agent failed to initialize")
            
            if len(self.agents) >= 3:  # Need at least 3 agents to be functional
                self.initialized = True
                logger.info(f"✅ Google ADK Orchestrator initialized with {len(self.agents)} agents")
            else:
                logger.error(f"❌ Insufficient agents initialized: {len(self.agents)}/5")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize Google ADK Orchestrator: {str(e)}")
    
    async def orchestrate_comprehensive_analysis(self, startup_data: Dict[str, Any], startup_id: str, user_id: str = "demo_user") -> Dict[str, Any]:
        """Orchestrate comprehensive startup analysis using Google ADK workflow"""
        if not self.initialized:
            raise Exception("Google ADK Orchestrator not initialized")
        
        start_time = time.time()
        results = {}
        
        try:
            # Initialize Firebase session for real-time updates
            enhanced_firebase_client.create_analysis_session(startup_id, user_id)
            
            logger.info(f"🚀 Starting Google ADK analysis for {startup_data.get('company_name', 'Unknown')}")
            
            # Phase 1: Data Collection (Sequential)
            if "data_collection" in self.agents:
                logger.info("📊 Phase 1: Data Collection")
                enhanced_firebase_client.update_real_time_progress(
                    startup_id, "Data Collection Agent", 10, {"status": "collecting market data"}
                )
                
                data_result = await self.agents["data_collection"].analyze(startup_data)
                results["data_collection"] = data_result
                
                enhanced_firebase_client.update_real_time_progress(
                    startup_id, "Data Collection Agent", 20, {"status": "data collection completed"}
                )
            
            # Phase 2: Parallel Business & Risk Analysis
            logger.info("⚡ Phase 2: Business Analysis & Risk Assessment (Parallel)")
            enhanced_firebase_client.update_real_time_progress(
                startup_id, "Business & Risk Analysis", 30, {"status": "parallel analysis in progress"}
            )
            
            parallel_tasks = []
            
            if "business_analysis" in self.agents:
                parallel_tasks.append(
                    self.agents["business_analysis"].analyze(startup_data, results)
                )
            
            if "risk_assessment" in self.agents:
                parallel_tasks.append(
                    self.agents["risk_assessment"].analyze(startup_data, results)
                )
            
            if parallel_tasks:
                parallel_results = await asyncio.gather(*parallel_tasks, return_exceptions=True)
                
                for i, result in enumerate(parallel_results):
                    if isinstance(result, Exception):
                        logger.error(f"Parallel analysis {i} failed: {str(result)}")
                    else:
                        agent_type = result.get("agent_type")
                        if agent_type:
                            results[agent_type] = result
            
            enhanced_firebase_client.update_real_time_progress(
                startup_id, "Business & Risk Analysis", 60, {"status": "parallel analysis completed"}
            )
            
            # Phase 3: Investment Insights (Sequential, depends on previous results)
            if "investment_insights" in self.agents:
                logger.info("💰 Phase 3: Investment Insights")
                enhanced_firebase_client.update_real_time_progress(
                    startup_id, "Investment Insights Agent", 70, {"status": "generating investment analysis"}
                )
                
                investment_result = await self.agents["investment_insights"].analyze(startup_data, results)
                results["investment_insights"] = investment_result
                
                enhanced_firebase_client.update_real_time_progress(
                    startup_id, "Investment Insights Agent", 80, {"status": "investment analysis completed"}
                )
            
            # Phase 4: Report Generation (Sequential, synthesizes all results)
            if "report_generation" in self.agents:
                logger.info("📄 Phase 4: Report Generation")
                enhanced_firebase_client.update_real_time_progress(
                    startup_id, "Report Generation Agent", 90, {"status": "generating executive report"}
                )
                
                report_result = await self.agents["report_generation"].analyze(startup_data, results)
                results["report_generation"] = report_result
                
                enhanced_firebase_client.update_real_time_progress(
                    startup_id, "Report Generation Agent", 100, {"status": "analysis completed"}
                )
            
            # Compile final results
            total_time = time.time() - start_time
            
            final_analysis = {
                "startup_id": startup_id,
                "company_name": startup_data.get("company_name", "Unknown"),
                "industry": startup_data.get("industry", "Unknown"),
                "analysis_timestamp": time.time(),
                "processing_time": total_time,
                "orchestrator": "Google ADK",
                "agents_used": list(results.keys()),
                "agent_results": results,
                "summary": self._create_executive_summary(results),
                "recommendation": self._extract_recommendation(results),
                "confidence_score": self._calculate_overall_confidence(results),
                "next_steps": self._generate_next_steps(results)
            }
            
            # Store final results in Firebase
            enhanced_firebase_client.store_final_analysis_result(startup_id, final_analysis, user_id)
            
            logger.info(f"✅ Google ADK analysis completed in {total_time:.2f} seconds")
            return final_analysis
            
        except Exception as e:
            logger.error(f"❌ Google ADK analysis failed: {str(e)}")
            enhanced_firebase_client.update_real_time_progress(
                startup_id, "Error", 0, {"status": "analysis failed", "error": str(e)}
            )
            raise Exception(f"Google ADK analysis failed: {str(e)}")
    
    def _create_executive_summary(self, results: Dict[str, Any]) -> str:
        """Create executive summary from all agent results"""
        report_result = results.get("report_generation", {})
        if report_result and report_result.get("analysis_result", {}).get("analysis"):
            summary = report_result["analysis_result"]["analysis"]
            # Extract first paragraph or first 300 characters
            lines = summary.split('\n')
            for line in lines:
                if len(line.strip()) > 50:
                    return line.strip()[:300] + "..."
        
        # Fallback summary
        company = results.get("data_collection", {}).get("input_summary", "Unknown Company")
        return f"Comprehensive analysis completed for {company} using Google ADK multi-agent system."
    
    def _extract_recommendation(self, results: Dict[str, Any]) -> str:
        """Extract investment recommendation"""
        investment_result = results.get("investment_insights", {})
        if investment_result:
            analysis = investment_result.get("analysis_result", {}).get("analysis", "")
            # Look for recommendation keywords
            if "INVEST" in analysis.upper() and "DON'T" not in analysis.upper():
                return "RECOMMENDED"
            elif "DON'T INVEST" in analysis.upper():
                return "NOT RECOMMENDED"
            elif "CONDITIONAL" in analysis.upper():
                return "CONDITIONAL"
        
        return "REQUIRES FURTHER ANALYSIS"
    
    def _calculate_overall_confidence(self, results: Dict[str, Any]) -> float:
        """Calculate overall confidence score"""
        if not results:
            return 0.0
        
        total_confidence = 0.0
        count = 0
        
        for result in results.values():
            if "confidence_score" in result:
                total_confidence += result["confidence_score"]
                count += 1
        
        return total_confidence / count if count > 0 else 0.5
    
    def _generate_next_steps(self, results: Dict[str, Any]) -> List[str]:
        """Generate recommended next steps"""
        recommendation = self._extract_recommendation(results)
        
        if recommendation == "RECOMMENDED":
            return [
                "Proceed with detailed due diligence",
                "Negotiate term sheet",
                "Conduct management presentations",
                "Finalize investment documentation"
            ]
        elif recommendation == "CONDITIONAL":
            return [
                "Address identified risk factors",
                "Obtain additional financial data",
                "Schedule follow-up management meeting",
                "Re-evaluate after improvements"
            ]
        else:
            return [
                "Decline investment opportunity",
                "Provide feedback to management",
                "Monitor for future improvements",
                "Consider partnership alternatives"
            ]
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            "orchestrator_initialized": self.initialized,
            "total_agents": len(self.agents),
            "available_agents": list(self.agents.keys()),
            "agent_details": {
                agent_type: {
                    "initialized": agent.initialized,
                    "model_type": getattr(agent, 'model_type', 'unknown')
                }
                for agent_type, agent in self.agents.items()
            }
        }

# Global instance
google_adk_orchestrator = GoogleADKOrchestrator()
