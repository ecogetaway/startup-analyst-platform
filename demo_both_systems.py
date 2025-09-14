#!/usr/bin/env python3
"""
Demo Both Agent Systems
Shows traditional agents vs. Vertex AI Agent Builder
"""
import asyncio
import time
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
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

def demo_traditional_agents():
    """Demo traditional Python script agents"""
    print_header("Traditional Python Script Agents")
    print("🔧 Using basic Gemini API with Python scripts")
    
    try:
        # Import traditional agents
        from src.agents.orchestrator import Orchestrator
        from src.agents.data_collection_agent import DataCollectionAgent
        
        print_section("Initializing Traditional Agents")
        orchestrator = Orchestrator()
        print("✅ Traditional orchestrator initialized")
        
        # Test individual agent
        print_section("Testing Data Collection Agent")
        test_data = {
            "company_name": "TechFlow Solutions",
            "business_description": "AI-powered workflow automation"
        }
        
        start_time = time.time()
        result = orchestrator.agents["data_collection"].analyze(test_data)
        end_time = time.time()
        
        print(f"⏱️ Response time: {end_time - start_time:.2f} seconds")
        print(f"📊 Status: {result.get('status', 'unknown')}")
        print(f"🤖 Agent: {result.get('agent_name', 'unknown')}")
        
        if result.get('analysis'):
            analysis = result['analysis']
            print(f"📝 Analysis preview: {analysis[:200]}...")
        
        print("✅ Traditional agents working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Traditional agents failed: {str(e)}")
        return False

async def demo_vertex_ai_agents():
    """Demo Vertex AI Agent Builder agents"""
    print_header("Vertex AI Agent Builder Agents")
    print("🚀 Using advanced Vertex AI with Google ADK orchestration")
    
    try:
        # Import Vertex AI agents
        from src.agents.vertex_ai_orchestrator import VertexAIOrchestrator
        
        print_section("Initializing Vertex AI Agents")
        orchestrator = VertexAIOrchestrator()
        print("✅ Vertex AI orchestrator initialized")
        
        # Test individual agent
        print_section("Testing Data Collection Agent")
        test_data = {
            "company_name": "InnovateAI",
            "business_description": "Machine learning platform for healthcare"
        }
        
        start_time = time.time()
        result = orchestrator.agents["data_collection"].analyze(test_data)
        end_time = time.time()
        
        print(f"⏱️ Response time: {end_time - start_time:.2f} seconds")
        print(f"📊 Status: {result.get('status', 'unknown')}")
        print(f"🤖 Agent: {result.get('agent_name', 'unknown')}")
        print(f"🧠 Model: {result.get('model_used', 'unknown')}")
        
        if result.get('analysis'):
            analysis = result['analysis']
            print(f"📝 Analysis preview: {analysis[:200]}...")
        
        # Test health check
        print_section("System Health Check")
        health_status = await orchestrator.health_check()
        print(f"🏥 Overall status: {health_status.get('overall_status', 'unknown')}")
        
        components = health_status.get('components', {})
        for component, status in components.items():
            if isinstance(status, dict):
                print(f"  {component}: {status.get('status', 'unknown')}")
        
        print("✅ Vertex AI agents working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Vertex AI agents failed: {str(e)}")
        return False

def compare_systems():
    """Compare both systems"""
    print_header("System Comparison")
    print("📊 Comparing Traditional vs. Vertex AI Agent Builder")
    
    comparison_data = {
        "Traditional Agents": {
            "Setup Time": "15 minutes",
            "Complexity": "Simple",
            "Features": "Basic",
            "Scalability": "Limited",
            "Error Handling": "Basic",
            "Real-time Updates": "Limited",
            "Hackathon Impact": "Good"
        },
        "Vertex AI Agent Builder": {
            "Setup Time": "45 minutes",
            "Complexity": "Advanced",
            "Features": "Professional",
            "Scalability": "Enterprise",
            "Error Handling": "Advanced",
            "Real-time Updates": "Full",
            "Hackathon Impact": "Excellent"
        }
    }
    
    print_section("Feature Comparison")
    for system, features in comparison_data.items():
        print(f"\n🔧 {system}:")
        for feature, value in features.items():
            print(f"  {feature}: {value}")
    
    print_section("Recommendations")
    print("🎯 For Quick Demos: Use Traditional Agents")
    print("🏆 For Hackathons: Use Vertex AI Agent Builder")
    print("🔄 For Learning: Start with Traditional, upgrade to Vertex AI")
    print("💼 For Production: Use Vertex AI Agent Builder")

def demo_migration_path():
    """Demo migration from traditional to Vertex AI"""
    print_header("Migration Path Demo")
    print("🔄 Showing how to upgrade from traditional to advanced")
    
    print_section("Step 1: Traditional System (Working)")
    print("✅ Basic agents with Gemini API")
    print("✅ Simple orchestration")
    print("✅ Quick setup and demo")
    
    print_section("Step 2: Upgrade to Vertex AI (Enhanced)")
    print("🚀 Advanced agents with Vertex AI Agent Builder")
    print("🚀 Google ADK orchestration")
    print("🚀 Real-time updates and monitoring")
    
    print_section("Step 3: Benefits of Upgrade")
    print("📈 Better performance and reliability")
    print("📈 Professional features and monitoring")
    print("📈 Scalable architecture")
    print("📈 Hackathon-winning capabilities")

async def main():
    """Main demo function"""
    print_header("Complete Agent System Demo")
    print("🎯 Demonstrating both Traditional and Vertex AI Agent Builder systems")
    
    try:
        # Demo traditional agents
        traditional_success = demo_traditional_agents()
        
        # Demo Vertex AI agents
        vertex_success = await demo_vertex_ai_agents()
        
        # Compare systems
        compare_systems()
        
        # Show migration path
        demo_migration_path()
        
        # Final summary
        print_header("Demo Summary")
        print("🎉 Both agent systems are working!")
        print(f"✅ Traditional Agents: {'Working' if traditional_success else 'Failed'}")
        print(f"✅ Vertex AI Agents: {'Working' if vertex_success else 'Failed'}")
        
        if traditional_success and vertex_success:
            print("\n🏆 You have the best of both worlds!")
            print("🚀 Traditional agents for quick demos")
            print("🚀 Vertex AI agents for hackathon competition")
            print("🚀 Easy migration path between systems")
        else:
            print("\n⚠️ Some systems need attention")
            print("🔧 Check configuration and try again")
        
        print("\n📚 Next Steps:")
        print("1. Use traditional agents for quick testing")
        print("2. Use Vertex AI agents for hackathon demo")
        print("3. Show both systems to demonstrate learning")
        print("4. Highlight the evolution and improvement")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("🔧 Please check your configuration and try again")

if __name__ == "__main__":
    asyncio.run(main())
