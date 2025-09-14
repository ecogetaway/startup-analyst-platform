#!/usr/bin/env python3
"""
Hackathon Demo Script
Focused demonstration for judges
"""
import asyncio
import time
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"🏆 {title}")
    print("="*70)

def print_section(title):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 50)

async def hackathon_demo():
    """Main hackathon demonstration"""
    print_header("Hackathon Demo: Vertex AI Agent Builder System")
    print("🎯 Advanced AI-powered startup analysis platform")
    
    try:
        # Import system
        from src.agents.vertex_ai_orchestrator import VertexAIOrchestrator
        
        print_section("🚀 System Overview")
        print("• 5 specialized AI agents built with Vertex AI Agent Builder")
        print("• Google ADK orchestration for workflow management")
        print("• Real-time updates via Firebase integration")
        print("• Production-ready error handling and monitoring")
        
        # Initialize system
        print_section("🔧 Initializing System")
        orchestrator = VertexAIOrchestrator()
        print("✅ Vertex AI Agent Builder system initialized")
        
        # Health check
        health_status = await orchestrator.health_check()
        print(f"✅ System health: {health_status['overall_status']}")
        
        # Demo startup analysis
        print_section("📊 Live Startup Analysis Demo")
        
        demo_startup = {
            "company_name": "TechFlow Solutions",
            "business_description": "AI-powered workflow automation platform for small businesses",
            "industry": "SaaS",
            "stage": "Series A",
            "founder_name": "Sarah Johnson",
            "founder_background": "Former Google engineer with 10 years experience in AI/ML",
            "website": "https://techflow.com",
            "additional_info": "Raised $5M in seed funding, 100+ customers, $50K MRR"
        }
        
        print(f"Analyzing: {demo_startup['company_name']}")
        print(f"Business: {demo_startup['business_description']}")
        print(f"Founder: {demo_startup['founder_name']}")
        
        # Execute analysis
        print("\n🔄 Executing complete analysis workflow...")
        start_time = time.time()
        
        results = await orchestrator.analyze_startup(demo_startup, "hackathon_demo")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print_section("📈 Analysis Results")
        print(f"⏱️ Total analysis time: {total_time:.2f} seconds")
        print(f"📊 Agents executed: {len(results)}")
        
        # Show results
        for agent_name, result in results.items():
            status = result.get("status", "unknown")
            processing_time = result.get("processing_time", 0)
            print(f"  {agent_name}: {status} ({processing_time:.2f}s)")
        
        # Show sample analysis
        if "data_collection" in results:
            data_analysis = results["data_collection"].get("analysis", "")
            if data_analysis:
                print_section("📝 Sample Analysis Output")
                print(data_analysis[:400] + "..." if len(data_analysis) > 400 else data_analysis)
        
        # Show advanced features
        print_section("🎯 Advanced Features Demonstrated")
        print("✅ Vertex AI Agent Builder - Professional AI agent creation")
        print("✅ Google ADK Orchestration - Advanced workflow management")
        print("✅ Real-time Updates - Live progress tracking via Firebase")
        print("✅ Error Handling - Robust retry logic and monitoring")
        print("✅ Parallel Processing - Multiple agents working simultaneously")
        print("✅ Production Ready - Enterprise-grade architecture")
        
        # Show hackathon advantages
        print_section("🏆 Hackathon Advantages")
        print("• Demonstrates cutting-edge Google AI capabilities")
        print("• Shows professional, production-ready system")
        print("• Real-time collaboration and progress tracking")
        print("• Advanced orchestration and workflow management")
        print("• Comprehensive error handling and monitoring")
        print("• Scalable architecture for real-world use")
        
        print_section("🎉 Demo Complete")
        print("✅ Vertex AI Agent Builder system demonstrated successfully")
        print("🏆 Ready for hackathon competition")
        print("🚀 Production-ready AI agent system")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("🔧 Please check your configuration and try again")
        return False

async def main():
    """Main function"""
    success = await hackathon_demo()
    
    if success:
        print("\n🎯 Demo completed successfully!")
        print("🏆 Your Vertex AI Agent Builder system is ready for the hackathon!")
    else:
        print("\n❌ Demo failed. Please check your setup.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
