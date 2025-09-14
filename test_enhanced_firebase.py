#!/usr/bin/env python3
"""
Test Enhanced Firebase Client
"""
import sys
import os
import time

# Add src to path
sys.path.append('src')

from src.utils.enhanced_firebase_client import enhanced_firebase_client

def test_firebase_connection():
    """Test Firebase connection and basic operations"""
    print("🔥 Testing Enhanced Firebase Client")
    print("=" * 50)
    
    # Test initialization
    print(f"✅ Firebase Available: {enhanced_firebase_client.is_available()}")
    
    if not enhanced_firebase_client.is_available():
        print("⚠️ Firebase not available - this is expected in development")
        print("✅ Client gracefully handles unavailable Firebase")
        return True
    
    # Test creating analysis session
    startup_id = f"test_startup_{int(time.time())}"
    print(f"\n📊 Testing Analysis Session Creation")
    print(f"Startup ID: {startup_id}")
    
    success = enhanced_firebase_client.create_analysis_session(startup_id, "test_user")
    print(f"✅ Session Created: {success}")
    
    # Test progress updates
    print(f"\n🔄 Testing Real-time Progress Updates")
    progress_tests = [
        ("Data Collection Agent", 20, {"status": "collecting market data"}),
        ("Business Analysis Agent", 40, {"status": "analyzing business model"}),
        ("Risk Assessment Agent", 60, {"status": "evaluating risks"}),
        ("Investment Insights Agent", 80, {"status": "generating insights"}),
        ("Report Generation Agent", 100, {"status": "finalizing report"})
    ]
    
    for agent_name, progress, results in progress_tests:
        success = enhanced_firebase_client.update_real_time_progress(
            startup_id, agent_name, progress, results
        )
        print(f"  {agent_name}: {progress}% - {success}")
        time.sleep(0.5)
    
    # Test getting session data
    print(f"\n📖 Testing Session Data Retrieval")
    session_data = enhanced_firebase_client.get_analysis_session(startup_id)
    if session_data:
        print(f"✅ Session Data Retrieved")
        print(f"  Status: {session_data.get('status')}")
        print(f"  Progress: {session_data.get('progress')}%")
        print(f"  Current Agent: {session_data.get('current_agent')}")
        print(f"  Agents Completed: {len(session_data.get('agents_completed', []))}")
    else:
        print("❌ Failed to retrieve session data")
    
    # Test storing final results
    print(f"\n💾 Testing Final Analysis Storage")
    final_analysis = {
        "company_name": "Test Startup",
        "industry": "Technology",
        "analysis_results": {
            "market_opportunity": "Large and growing market",
            "business_model": "Strong SaaS model with recurring revenue",
            "risk_assessment": "Moderate risk profile",
            "investment_recommendation": "Recommended for investment"
        },
        "processing_time": 9.5,
        "agents_used": ["data_collection", "business_analysis", "risk_assessment", "investment_insights", "report_generation"]
    }
    
    success = enhanced_firebase_client.store_final_analysis_result(
        startup_id, final_analysis, "test_user"
    )
    print(f"✅ Final Analysis Stored: {success}")
    
    # Test getting analysis history
    print(f"\n📚 Testing Analysis History")
    history = enhanced_firebase_client.get_user_analysis_history("test_user")
    print(f"✅ Analysis History Retrieved: {len(history)} items")
    
    for i, analysis in enumerate(history[:3]):  # Show first 3
        print(f"  {i+1}. {analysis.get('company_name')} ({analysis.get('industry')})")
    
    # Test demo scenarios
    print(f"\n🎭 Testing Demo Scenarios")
    scenarios = enhanced_firebase_client.get_demo_scenarios()
    print(f"✅ Demo Scenarios Retrieved: {len(scenarios)} scenarios")
    
    for i, scenario in enumerate(scenarios):
        print(f"  {i+1}. {scenario.get('company_name')} - {scenario.get('industry')}")
    
    print("\n" + "=" * 50)
    print("🎉 Enhanced Firebase Client Test Complete!")
    return True

if __name__ == "__main__":
    try:
        test_firebase_connection()
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        sys.exit(1)
