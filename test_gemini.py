#!/usr/bin/env python3
"""
Test script to verify Gemini AI integration
"""
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

# Load environment variables
load_dotenv()

def test_gemini_connection():
    """Test basic Gemini connection"""
    try:
        from src.utils.ai_client import AIClient
        
        print("🧪 Testing Gemini AI Connection...")
        
        # Check if API key is set
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ GOOGLE_API_KEY not found in environment")
            print("   Please set your Google API key in .env file")
            return False
        
        print(f"✅ API Key found: {api_key[:10]}...")
        
        # Initialize AI client
        ai_client = AIClient()
        print("✅ AI Client initialized")
        
        # Test simple generation
        test_prompt = "What is 2+2? Answer in one word."
        print(f"📝 Testing with prompt: {test_prompt}")
        
        response = ai_client.generate_content(test_prompt)
        print(f"🤖 Gemini Response: {response}")
        
        if response and len(response.strip()) > 0:
            print("✅ Gemini AI is working correctly!")
            return True
        else:
            print("❌ Empty response from Gemini")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gemini: {str(e)}")
        return False

def test_agent_structure():
    """Test agent structure without AI calls"""
    try:
        from src.agents.data_collection_agent import DataCollectionAgent
        from src.models.startup import StartupInput
        
        print("\n🧪 Testing Agent Structure...")
        
        # Create test startup input
        test_startup = StartupInput(
            company_name="Test Company",
            business_description="A test business for validation"
        )
        
        # Create agent
        agent = DataCollectionAgent()
        print(f"✅ Created {agent.name}")
        
        # Test prompt creation
        prompt = agent._create_prompt(test_startup)
        print(f"✅ Generated prompt: {len(prompt)} characters")
        
        # Test system instruction
        system_instruction = agent._create_system_instruction()
        print(f"✅ Generated system instruction: {len(system_instruction)} characters")
        
        print("✅ Agent structure is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing agent structure: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Startup Analyst Platform - Gemini Integration Test\n")
    
    # Test 1: Agent Structure
    agent_ok = test_agent_structure()
    
    # Test 2: Gemini Connection (only if API key is available)
    gemini_ok = test_gemini_connection()
    
    print("\n📊 Test Results:")
    print(f"   Agent Structure: {'✅ PASS' if agent_ok else '❌ FAIL'}")
    print(f"   Gemini Connection: {'✅ PASS' if gemini_ok else '❌ FAIL'}")
    
    if agent_ok and gemini_ok:
        print("\n🎉 All tests passed! Ready for deployment.")
        return True
    elif agent_ok:
        print("\n⚠️  Agent structure works, but Gemini needs API key setup.")
        print("   Set GOOGLE_API_KEY in .env file to test AI integration.")
        return True
    else:
        print("\n❌ Tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

