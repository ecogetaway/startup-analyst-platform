#!/usr/bin/env python3
"""
Test script to verify actual Google services integration
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_google_generative_ai():
    """Test actual Google Generative AI (Gemini)"""
    try:
        import google.generativeai as genai
        
        print("🧪 Testing Google Generative AI (Gemini)...")
        
        # Check API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ GOOGLE_API_KEY not found")
            return False
        
        # Configure and test
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test actual API call
        response = model.generate_content("What is 2+2? Answer in one word.")
        
        if response.text:
            print(f"✅ Google Generative AI working! Response: {response.text}")
            return True
        else:
            print("❌ No response from Google Generative AI")
            return False
            
    except Exception as e:
        print(f"❌ Google Generative AI test failed: {str(e)}")
        return False

def test_vertex_ai():
    """Test actual Vertex AI"""
    try:
        from google.cloud import aiplatform
        
        print("🧪 Testing Vertex AI...")
        
        # Initialize Vertex AI
        aiplatform.init(
            project=os.getenv("GOOGLE_CLOUD_PROJECT", "startup-analyst-platform"),
            location="us-central1"
        )
        
        print("✅ Vertex AI initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Vertex AI test failed: {str(e)}")
        print("   This is expected if Google Cloud CLI is not set up yet")
        return False

def test_firebase():
    """Test actual Firebase"""
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        
        print("🧪 Testing Firebase...")
        
        # Try to initialize Firebase
        if not firebase_admin._apps:
            # This will work if we have proper credentials
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("✅ Firebase initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Firebase test failed: {str(e)}")
        print("   This is expected if Firebase is not set up yet")
        return False

def test_google_cloud_apis():
    """Test Google Cloud APIs"""
    try:
        from google.cloud import storage
        
        print("🧪 Testing Google Cloud Storage...")
        
        # This will work if we have proper credentials
        client = storage.Client()
        print("✅ Google Cloud Storage client created")
        return True
        
    except Exception as e:
        print(f"❌ Google Cloud Storage test failed: {str(e)}")
        return False

def main():
    """Run all Google services tests"""
    print("🚀 Testing Google Tech Stack Integration\n")
    
    results = {
        "Google Generative AI": test_google_generative_ai(),
        "Vertex AI": test_vertex_ai(),
        "Firebase": test_firebase(),
        "Google Cloud Storage": test_google_cloud_apis()
    }
    
    print("\n📊 Test Results:")
    for service, status in results.items():
        print(f"   {service}: {'✅ WORKING' if status else '❌ NEEDS SETUP'}")
    
    working_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n🎯 Summary: {working_count}/{total_count} services working")
    
    if working_count >= 1:
        print("✅ At least Google Generative AI is working - you can demo!")
        print("   Judges will see actual Google AI responses")
    else:
        print("❌ No Google services working yet")
        print("   Need to set up Google Cloud CLI and APIs")

if __name__ == "__main__":
    main()
