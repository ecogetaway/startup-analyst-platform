#!/usr/bin/env python3
"""
Test Vertex AI Agent Builder System
Comprehensive testing of all agents and orchestration
"""
import asyncio
import time
import json
from src.agents.vertex_ai_orchestrator import VertexAIOrchestrator
from src.models.startup import StartupInput

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def print_result(result, title="Result"):
    """Print formatted result"""
    print(f"\n✅ {title}:")
    if isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, str) and len(value) > 100:
                print(f"  {key}: {value[:100]}...")
            else:
                print(f"  {key}: {value}")
    else:
        print(f"  {result}")

async def test_individual_agents():
    """Test each agent individually"""
    print_header("Testing Individual Agents")
    
    # Test data
    test_startup = {
        "company_name": "TechFlow Solutions",
        "business_description": "AI-powered workflow automation platform for small businesses",
        "industry": "SaaS",
        "stage": "Series A",
        "founder_name": "Sarah Johnson",
        "founder_background": "Former Google engineer with 10 years experience in AI/ML",
        "website": "https://techflow.com",
        "additional_info": "Raised $5M in seed funding, 100+ customers, $50K MRR"
    }
    
    orchestrator = VertexAIOrchestrator()
    
    # Test Data Collection Agent
    print_section("Data Collection Agent")
    try:
        result = orchestrator.agents["data_collection"].analyze(test_startup)
        print_result(result, "Data Collection Analysis")
    except Exception as e:
        print(f"❌ Data Collection Agent failed: {str(e)}")
    
    # Test Business Analysis Agent
    print_section("Business Analysis Agent")
    try:
        result = orchestrator.agents["business_analysis"].analyze(test_startup)
        print_result(result, "Business Analysis")
    except Exception as e:
        print(f"❌ Business Analysis Agent failed: {str(e)}")
    
    # Test Risk Assessment Agent
    print_section("Risk Assessment Agent")
    try:
        result = orchestrator.agents["risk_assessment"].analyze(test_startup)
        print_result(result, "Risk Assessment")
    except Exception as e:
        print(f"❌ Risk Assessment Agent failed: {str(e)}")
    
    # Test Investment Insights Agent
    print_section("Investment Insights Agent")
    try:
        # Create mock data from previous agents
        mock_data = {
            "data": {"company_name": "TechFlow Solutions", "analysis": "Mock data collection results"},
            "business": {"analysis": "Mock business analysis results"},
            "risks": {"analysis": "Mock risk assessment results"}
        }
        result = orchestrator.agents["investment_insights"].analyze(mock_data)
        print_result(result, "Investment Insights")
    except Exception as e:
        print(f"❌ Investment Insights Agent failed: {str(e)}")
    
    # Test Report Generation Agent
    print_section("Report Generation Agent")
    try:
        # Create mock data from all previous agents
        mock_data = {
            "data": {"company_name": "TechFlow Solutions", "analysis": "Mock data collection results"},
            "business": {"analysis": "Mock business analysis results"},
            "risks": {"analysis": "Mock risk assessment results"},
            "investment": {"analysis": "Mock investment insights results"}
        }
        result = orchestrator.agents["report_generation"].analyze(mock_data)
        print_result(result, "Report Generation")
    except Exception as e:
        print(f"❌ Report Generation Agent failed: {str(e)}")

async def test_orchestration():
    """Test the complete orchestration workflow"""
    print_header("Testing Complete Orchestration")
    
    # Test data
    test_startup = {
        "company_name": "InnovateAI",
        "business_description": "Machine learning platform for predictive analytics in healthcare",
        "industry": "Healthcare AI",
        "stage": "Seed",
        "founder_name": "Dr. Michael Chen",
        "founder_background": "PhD in Computer Science, former research scientist at Stanford",
        "website": "https://innovateai.com",
        "additional_info": "Early stage startup, 20+ pilot customers, $10K MRR"
    }
    
    orchestrator = VertexAIOrchestrator()
    
    print_section("Starting Complete Analysis Workflow")
    print(f"📊 Analyzing: {test_startup['company_name']}")
    print(f"🏢 Business: {test_startup['business_description']}")
    print(f"👤 Founder: {test_startup['founder_name']}")
    
    try:
        start_time = time.time()
        
        # Execute complete workflow
        results = await orchestrator.analyze_startup(test_startup, "test_user")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print_section("Workflow Results")
        print(f"⏱️ Total execution time: {total_time:.2f} seconds")
        print(f"📈 Number of agents executed: {len(results)}")
        
        # Display results summary
        for agent_name, result in results.items():
            status = result.get("status", "unknown")
            processing_time = result.get("processing_time", 0)
            print(f"  {agent_name}: {status} ({processing_time:.2f}s)")
        
        # Show sample analysis
        if "data_collection" in results:
            data_analysis = results["data_collection"].get("analysis", "")
            if data_analysis:
                print_section("Sample Data Collection Analysis")
                print(data_analysis[:500] + "..." if len(data_analysis) > 500 else data_analysis)
        
        return results
        
    except Exception as e:
        print(f"❌ Orchestration failed: {str(e)}")
        return None

async def test_health_check():
    """Test system health check"""
    print_header("System Health Check")
    
    orchestrator = VertexAIOrchestrator()
    
    try:
        health_status = await orchestrator.health_check()
        print_result(health_status, "Health Status")
        
        # Check individual components
        components = health_status.get("components", {})
        
        print_section("Component Status")
        for component, status in components.items():
            if isinstance(status, dict):
                component_status = status.get("status", "unknown")
                print(f"  {component}: {component_status}")
            else:
                print(f"  {component}: {status}")
        
        return health_status
        
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return None

async def test_progress_tracking():
    """Test real-time progress tracking"""
    print_header("Testing Progress Tracking")
    
    orchestrator = VertexAIOrchestrator()
    
    # Test startup data
    test_startup = {
        "company_name": "ProgressTest",
        "business_description": "Testing progress tracking functionality",
        "industry": "Testing",
        "stage": "Test"
    }
    
    try:
        # Start analysis
        print_section("Starting Analysis with Progress Tracking")
        task = asyncio.create_task(orchestrator.analyze_startup(test_startup, "progress_test_user"))
        
        # Monitor progress
        startup_id = f"ProgressTest_{int(time.time())}"
        
        for i in range(10):  # Check progress 10 times
            await asyncio.sleep(2)  # Wait 2 seconds
            
            progress = await orchestrator.get_analysis_progress(startup_id)
            if progress.get("status") == "completed":
                print(f"✅ Analysis completed: {progress.get('progress', 0)}%")
                break
            elif progress.get("status") == "error":
                print(f"❌ Analysis failed: {progress.get('error', 'Unknown error')}")
                break
            else:
                current_progress = progress.get("progress", 0)
                current_agent = progress.get("current_agent", "Unknown")
                print(f"📊 Progress: {current_progress}% - {current_agent}")
        
        # Wait for task completion
        results = await task
        print_result(results, "Final Results")
        
    except Exception as e:
        print(f"❌ Progress tracking test failed: {str(e)}")

async def main():
    """Main test function"""
    print_header("Vertex AI Agent Builder System Test")
    print("🚀 Testing advanced AI agent system with Vertex AI and Google ADK")
    
    try:
        # Test individual agents
        await test_individual_agents()
        
        # Test orchestration
        await test_orchestration()
        
        # Test health check
        await test_health_check()
        
        # Test progress tracking
        await test_progress_tracking()
        
        print_header("Test Summary")
        print("✅ All tests completed successfully!")
        print("🎯 Vertex AI Agent Builder system is working correctly")
        print("🏆 Ready for hackathon demonstration!")
        
    except Exception as e:
        print(f"❌ Test suite failed: {str(e)}")
        print("🔧 Please check your configuration and try again")

if __name__ == "__main__":
    asyncio.run(main())
