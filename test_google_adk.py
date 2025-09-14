#!/usr/bin/env python3
"""
Test Google ADK (Agent Development Kit) Orchestrator
"""
import sys
import asyncio
import time

# Add src to path
sys.path.append('src')

from src.agents.google_adk_orchestrator import google_adk_orchestrator

async def test_google_adk():
    """Test Google ADK orchestrator functionality"""
    print("🤖 Testing Google ADK (Agent Development Kit) Orchestrator")
    print("=" * 70)
    
    # Test agent status
    print("📊 Agent Status Check")
    status = google_adk_orchestrator.get_agent_status()
    
    print(f"✅ Orchestrator Initialized: {status['orchestrator_initialized']}")
    print(f"✅ Total Agents: {status['total_agents']}")
    print(f"✅ Available Agents: {', '.join(status['available_agents'])}")
    
    if status['agent_details']:
        print("\n🔧 Agent Details:")
        for agent_type, details in status['agent_details'].items():
            print(f"  {agent_type.replace('_', ' ').title()}: {details['model_type']} ({'✅' if details['initialized'] else '❌'})")
    
    if not status['orchestrator_initialized']:
        print("\n⚠️ Google ADK Orchestrator not fully initialized")
        print("This is expected if Google Cloud credentials are not set up")
        return True
    
    # Test comprehensive analysis
    print(f"\n🚀 Testing Comprehensive Startup Analysis")
    
    test_startup = {
        "company_name": "TechFlow AI",
        "industry": "Artificial Intelligence",
        "stage": "Series A",
        "description": "AI-powered analytics platform for small businesses providing instant insights and recommendations",
        "funding_request": "$5M",
        "key_metrics": "50 pilot customers, $50K MRR, 95% customer satisfaction"
    }
    
    startup_id = f"adk_test_{int(time.time())}"
    
    print(f"Company: {test_startup['company_name']}")
    print(f"Industry: {test_startup['industry']}")
    print(f"Stage: {test_startup['stage']}")
    print(f"Startup ID: {startup_id}")
    
    try:
        print(f"\n⏱️ Starting Google ADK Analysis...")
        start_time = time.time()
        
        # Run comprehensive analysis
        results = await google_adk_orchestrator.orchestrate_comprehensive_analysis(
            test_startup, 
            startup_id, 
            "test_user"
        )
        
        analysis_time = time.time() - start_time
        
        print(f"\n✅ Analysis Completed in {analysis_time:.2f} seconds")
        print("=" * 70)
        
        # Display results summary
        print("📋 ANALYSIS SUMMARY")
        print(f"Company: {results.get('company_name')}")
        print(f"Processing Time: {results.get('processing_time', 0):.2f} seconds")
        print(f"Agents Used: {len(results.get('agents_used', []))}")
        print(f"Recommendation: {results.get('recommendation', 'Unknown')}")
        print(f"Confidence Score: {results.get('confidence_score', 0):.2f}")
        
        # Executive Summary
        summary = results.get('summary', '')
        if summary:
            print(f"\n📄 Executive Summary:")
            print(f"  {summary[:200]}...")
        
        # Agent Results Overview
        agent_results = results.get('agent_results', {})
        if agent_results:
            print(f"\n🤖 Agent Results Overview:")
            for agent_type, result in agent_results.items():
                status = result.get('status', 'unknown')
                processing_time = result.get('processing_time', 0)
                model_used = result.get('model_used', 'unknown')
                
                print(f"  {agent_type.replace('_', ' ').title()}:")
                print(f"    Status: {status}")
                print(f"    Time: {processing_time:.2f}s")
                print(f"    Model: {model_used}")
                
                # Show key insights
                analysis_result = result.get('analysis_result', {})
                if analysis_result.get('key_points'):
                    print(f"    Key Points: {len(analysis_result['key_points'])} insights")
        
        # Next Steps
        next_steps = results.get('next_steps', [])
        if next_steps:
            print(f"\n📋 Recommended Next Steps:")
            for i, step in enumerate(next_steps, 1):
                print(f"  {i}. {step}")
        
        print("\n" + "=" * 70)
        print("🎉 Google ADK Test Completed Successfully!")
        
        # Test individual agent if we want to see detailed output
        if len(agent_results) > 0:
            print(f"\n🔍 Sample Agent Output (First Agent):")
            first_agent = list(agent_results.values())[0]
            analysis_result = first_agent.get('analysis_result', {})
            
            if analysis_result.get('analysis'):
                sample_output = analysis_result['analysis'][:500]
                print(f"  {sample_output}...")
            elif analysis_result.get('structured_data'):
                print(f"  Structured data with {len(analysis_result['structured_data'])} fields")
        
        return True
        
    except Exception as e:
        print(f"❌ Google ADK test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_individual_agent():
    """Test individual agent functionality"""
    print(f"\n🔬 Testing Individual Agent Functionality")
    
    if not google_adk_orchestrator.initialized:
        print("⚠️ Orchestrator not initialized, skipping individual agent test")
        return
    
    # Test data collection agent
    if "data_collection" in google_adk_orchestrator.agents:
        print(f"\n📊 Testing Data Collection Agent")
        
        test_data = {
            "company_name": "QuickStart SaaS",
            "industry": "Software",
            "stage": "Seed",
            "description": "Project management tool for remote teams"
        }
        
        try:
            agent = google_adk_orchestrator.agents["data_collection"]
            result = await agent.analyze(test_data)
            
            print(f"✅ Agent Status: {result.get('status')}")
            print(f"✅ Processing Time: {result.get('processing_time', 0):.2f}s")
            print(f"✅ Model Used: {result.get('model_used')}")
            print(f"✅ Confidence: {result.get('confidence_score', 0):.2f}")
            
            # Show sample output
            analysis = result.get('analysis_result', {})
            if analysis.get('summary'):
                print(f"✅ Analysis Summary: {analysis['summary'][:100]}...")
                
        except Exception as e:
            print(f"❌ Individual agent test failed: {str(e)}")

if __name__ == "__main__":
    async def main():
        try:
            await test_google_adk()
            await test_individual_agent()
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            sys.exit(1)
    
    # Run the async test
    asyncio.run(main())
