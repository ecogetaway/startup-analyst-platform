#!/usr/bin/env python3
"""
Simple test script for Vertex AI agents - Perfect for beginners!
This script shows how to use the Vertex AI agents step by step.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_individual_agent():
    """Test one agent at a time - easier to understand"""
    print("🧪 TESTING INDIVIDUAL AGENT")
    print("=" * 50)
    
    try:
        # Import the agent
        from src.agents.vertex_ai_agents import DataCollectionAgent
        
        # Create the agent
        print("Creating Data Collection Agent...")
        agent = DataCollectionAgent()
        
        # Test data
        startup_data = {
            "company_name": "TechFlow Solutions",
            "business_description": "AI-powered workflow automation for small businesses",
            "industry": "SaaS",
            "stage": "Seed",
            "founder_name": "Sarah Johnson"
        }
        
        print(f"Testing with startup: {startup_data['company_name']}")
        print("Running analysis...")
        
        # Run the analysis
        result = agent.analyze(startup_data)
        
        # Show results
        print("\n📊 ANALYSIS RESULTS:")
        print("-" * 30)
        if result["status"] == "success":
            print("✅ Analysis successful!")
            print(f"Agent: {result['agent']}")
            print(f"Analysis: {result['analysis'][:200]}...")
        else:
            print("❌ Analysis failed!")
            print(f"Error: {result['error']}")
            
    except Exception as e:
        print(f"❌ Error testing agent: {e}")
        print("Make sure you have the required packages installed:")
        print("pip3 install google-cloud-aiplatform vertexai")

def test_all_agents():
    """Test all agents together"""
    print("\n🧪 TESTING ALL AGENTS TOGETHER")
    print("=" * 50)
    
    try:
        # Import the orchestrator
        from src.agents.vertex_ai_orchestrator import VertexAIOrchestrator
        
        # Create orchestrator (this creates all agents)
        print("Creating orchestrator with all agents...")
        orchestrator = VertexAIOrchestrator()
        
        # Test data
        startup_data = {
            "company_name": "MedAI Solutions",
            "business_description": "AI-powered medical diagnosis platform",
            "industry": "Healthcare AI",
            "stage": "Series A",
            "founder_name": "Dr. Sarah Chen",
            "funding": "$15M Series A"
        }
        
        print(f"Testing with startup: {startup_data['company_name']}")
        print("Running comprehensive analysis...")
        
        # Run analysis
        results = orchestrator.analyze_startup(startup_data)
        
        # Show results
        print("\n📊 COMPREHENSIVE ANALYSIS RESULTS:")
        print("-" * 40)
        
        for agent_name, result in results.items():
            print(f"\n🤖 {agent_name.upper()} AGENT:")
            if result["status"] == "success":
                print("✅ Success!")
                print(f"Analysis: {result['analysis'][:150]}...")
            else:
                print("❌ Failed!")
                print(f"Error: {result['error']}")
                
    except Exception as e:
        print(f"❌ Error testing orchestrator: {e}")
        print("Make sure you have the required packages installed:")
        print("pip3 install google-cloud-aiplatform vertexai")

def show_agent_explanations():
    """Explain what each agent does"""
    print("\n📚 AGENT EXPLANATIONS")
    print("=" * 50)
    
    agents = {
        "Data Collection Agent": "Gathers and validates startup information",
        "Business Analysis Agent": "Analyzes business model and market opportunity",
        "Risk Assessment Agent": "Identifies and evaluates potential risks",
        "Investment Insights Agent": "Provides investment recommendations",
        "Report Generation Agent": "Creates professional reports"
    }
    
    for agent_name, description in agents.items():
        print(f"🤖 {agent_name}:")
        print(f"   {description}")
        print()

def main():
    """Main function to run all tests"""
    print("🎯 VERTEX AI AGENTS - SIMPLE TEST")
    print("=" * 60)
    print("This script helps you understand how Vertex AI agents work!")
    print()
    
    # Check if API key is available
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("❌ Google Cloud credentials not found!")
        print("Make sure you have:")
        print("1. Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
        print("2. Downloaded service account key file")
        print("3. Enabled Vertex AI API in Google Cloud Console")
        return
    
    # Show explanations
    show_agent_explanations()
    
    # Test individual agent
    test_individual_agent()
    
    # Test all agents
    test_all_agents()
    
    print("\n🎉 TESTING COMPLETE!")
    print("=" * 30)
    print("You've seen how Vertex AI agents work!")
    print("Each agent has a specific role in analyzing startups.")
    print("The orchestrator coordinates them to work together.")

if __name__ == "__main__":
    main()
