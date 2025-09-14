"""
Vertex AI Orchestrator with Google ADK
Advanced workflow orchestration for startup analysis agents
"""
import asyncio
import time
import logging
from typing import Dict, Any, Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import firebase_admin
from firebase_admin import firestore
from .vertex_ai_agents import (
    DataCollectionAgent,
    BusinessAnalysisAgent,
    RiskAssessmentAgent,
    InvestmentInsightsAgent,
    ReportGenerationAgent
)
from ..config.settings import settings

logger = logging.getLogger(__name__)

class VertexAIOrchestrator:
    """Advanced orchestrator using Vertex AI and Google ADK principles"""
    
    def __init__(self):
        """Initialize the orchestrator with all agents"""
        self.agents = {
            "data_collection": DataCollectionAgent(),
            "business_analysis": BusinessAnalysisAgent(),
            "risk_assessment": RiskAssessmentAgent(),
            "investment_insights": InvestmentInsightsAgent(),
            "report_generation": ReportGenerationAgent()
        }
        
        # Initialize Firebase for real-time updates
        self._init_firebase()
        
        # Workflow configuration
        self.workflow_config = {
            "parallel_agents": ["business_analysis", "risk_assessment"],
            "sequential_agents": ["data_collection", "investment_insights", "report_generation"],
            "max_retries": 3,
            "timeout": 300  # 5 minutes per agent
        }
        
        logger.info("✅ Vertex AI Orchestrator initialized with all agents")
    
    def _init_firebase(self):
        """Initialize Firebase for real-time updates"""
        try:
            if not firebase_admin._apps:
                firebase_admin.initialize_app()
            
            self.db = firestore.client()
            logger.info("✅ Firebase initialized for real-time updates")
            
        except Exception as e:
            logger.warning(f"⚠️ Firebase initialization failed: {str(e)}")
            self.db = None
    
    async def analyze_startup(self, startup_data: Dict[str, Any], user_id: str = None) -> Dict[str, Any]:
        """Execute complete startup analysis workflow"""
        try:
            startup_id = f"{startup_data.get('company_name', 'startup')}_{int(time.time())}"
            
            # Update progress: Started
            await self._update_progress(startup_id, {
                "status": "started",
                "progress": 0,
                "user_id": user_id,
                "startup_name": startup_data.get('company_name', 'Unknown'),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Execute workflow
            results = await self._execute_workflow(startup_data, startup_id)
            
            # Store results in Firebase
            if self.db:
                await self._store_results(startup_id, results, user_id)
            
            # Update progress: Completed
            await self._update_progress(startup_id, {
                "status": "completed",
                "progress": 100,
                "results_available": True,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Workflow execution failed: {str(e)}")
            await self._update_progress(startup_id, {
                "status": "error",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            raise Exception(f"Workflow execution failed: {str(e)}")
    
    async def _execute_workflow(self, startup_data: Dict[str, Any], startup_id: str) -> Dict[str, Any]:
        """Execute the complete analysis workflow"""
        results = {}
        
        # Step 1: Data Collection (Sequential)
        await self._update_progress(startup_id, {
            "status": "running",
            "progress": 20,
            "current_agent": "Data Collection",
            "message": "Collecting and synthesizing startup information..."
        })
        
        data_results = await self._run_agent_with_retry(
            "data_collection", 
            startup_data, 
            startup_id
        )
        results["data_collection"] = data_results
        
        # Step 2: Parallel Analysis (Business Analysis & Risk Assessment)
        await self._update_progress(startup_id, {
            "status": "running",
            "progress": 40,
            "current_agent": "Business Analysis & Risk Assessment",
            "message": "Analyzing business model and assessing risks..."
        })
        
        # Run parallel agents
        parallel_tasks = [
            self._run_agent_with_retry("business_analysis", data_results, startup_id),
            self._run_agent_with_retry("risk_assessment", data_results, startup_id)
        ]
        
        parallel_results = await asyncio.gather(*parallel_tasks)
        results["business_analysis"] = parallel_results[0]
        results["risk_assessment"] = parallel_results[1]
        
        # Step 3: Investment Insights (Sequential)
        await self._update_progress(startup_id, {
            "status": "running",
            "progress": 70,
            "current_agent": "Investment Insights",
            "message": "Generating investment recommendations..."
        })
        
        investment_data = {
            "data": data_results,
            "business": parallel_results[0],
            "risks": parallel_results[1]
        }
        
        investment_results = await self._run_agent_with_retry(
            "investment_insights", 
            investment_data, 
            startup_id
        )
        results["investment_insights"] = investment_results
        
        # Step 4: Report Generation (Sequential)
        await self._update_progress(startup_id, {
            "status": "running",
            "progress": 90,
            "current_agent": "Report Generation",
            "message": "Creating comprehensive investment report..."
        })
        
        report_data = {
            "data": data_results,
            "business": parallel_results[0],
            "risks": parallel_results[1],
            "investment": investment_results
        }
        
        report_results = await self._run_agent_with_retry(
            "report_generation", 
            report_data, 
            startup_id
        )
        results["report_generation"] = report_results
        
        return results
    
    async def _run_agent_with_retry(self, agent_name: str, data: Dict[str, Any], startup_id: str) -> Dict[str, Any]:
        """Run agent with retry logic and error handling"""
        max_retries = self.workflow_config["max_retries"]
        
        for attempt in range(max_retries):
            try:
                # Run agent in thread pool to avoid blocking
                loop = asyncio.get_event_loop()
                with ThreadPoolExecutor() as executor:
                    result = await loop.run_in_executor(
                        executor, 
                        self.agents[agent_name].analyze, 
                        data
                    )
                
                if result.get("status") == "completed":
                    return result
                else:
                    raise Exception(f"Agent {agent_name} returned error: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                logger.warning(f"⚠️ Attempt {attempt + 1} failed for {agent_name}: {str(e)}")
                
                if attempt == max_retries - 1:
                    # Final attempt failed
                    return {
                        "agent_name": agent_name,
                        "status": "error",
                        "error": f"Failed after {max_retries} attempts: {str(e)}",
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                
                # Wait before retry
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        return {
            "agent_name": agent_name,
            "status": "error",
            "error": "Max retries exceeded",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    async def _update_progress(self, startup_id: str, progress_data: Dict[str, Any]):
        """Update analysis progress in Firebase"""
        if not self.db:
            return
        
        try:
            doc_ref = self.db.collection('analysis_progress').document(startup_id)
            doc_ref.set(progress_data, merge=True)
            logger.info(f"📊 Progress updated for {startup_id}: {progress_data.get('progress', 0)}%")
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to update progress: {str(e)}")
    
    async def _store_results(self, startup_id: str, results: Dict[str, Any], user_id: str = None):
        """Store analysis results in Firebase"""
        if not self.db:
            return
        
        try:
            doc_ref = self.db.collection('startup_analyses').document(startup_id)
            doc_ref.set({
                "startup_id": startup_id,
                "results": results,
                "user_id": user_id,
                "timestamp": time.time(),
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "completed"
            })
            logger.info(f"💾 Results stored for {startup_id}")
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to store results: {str(e)}")
    
    async def get_analysis_progress(self, startup_id: str) -> Dict[str, Any]:
        """Get current analysis progress"""
        if not self.db:
            return {"status": "firebase_not_available"}
        
        try:
            doc_ref = self.db.collection('analysis_progress').document(startup_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            else:
                return {"status": "not_found"}
                
        except Exception as e:
            logger.error(f"❌ Failed to get progress: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def get_analysis_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get analysis history for a user"""
        if not self.db:
            return []
        
        try:
            docs = self.db.collection('startup_analyses').where('user_id', '==', user_id).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(20).stream()
            
            history = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                history.append(data)
            
            return history
            
        except Exception as e:
            logger.error(f"❌ Failed to get analysis history: {str(e)}")
            return []
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {}
        
        for agent_name, agent in self.agents.items():
            try:
                # Test agent with simple data
                test_data = {"test": "data"}
                result = agent.analyze(test_data)
                
                status[agent_name] = {
                    "status": "healthy" if result.get("status") == "completed" else "error",
                    "model": agent.model_name,
                    "last_test": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
            except Exception as e:
                status[agent_name] = {
                    "status": "error",
                    "error": str(e),
                    "last_test": time.strftime("%Y-%m-%d %H:%M:%S")
                }
        
        return status
    
    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check of the system"""
        health_status = {
            "overall_status": "healthy",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "components": {}
        }
        
        # Check agents
        health_status["components"]["agents"] = self.get_agent_status()
        
        # Check Firebase
        if self.db:
            try:
                # Test Firebase connection
                test_doc = self.db.collection('health_check').document('test')
                test_doc.set({"test": "data"})
                test_doc.delete()
                
                health_status["components"]["firebase"] = {
                    "status": "healthy",
                    "message": "Firebase connection successful"
                }
            except Exception as e:
                health_status["components"]["firebase"] = {
                    "status": "error",
                    "error": str(e)
                }
                health_status["overall_status"] = "degraded"
        else:
            health_status["components"]["firebase"] = {
                "status": "not_configured",
                "message": "Firebase not initialized"
            }
        
        # Check Vertex AI
        try:
            # Test Vertex AI connection
            test_agent = self.agents["data_collection"]
            test_result = test_agent.analyze({"test": "data"})
            
            health_status["components"]["vertex_ai"] = {
                "status": "healthy" if test_result.get("status") == "completed" else "error",
                "message": "Vertex AI connection successful"
            }
        except Exception as e:
            health_status["components"]["vertex_ai"] = {
                "status": "error",
                "error": str(e)
            }
            health_status["overall_status"] = "degraded"
        
        return health_status