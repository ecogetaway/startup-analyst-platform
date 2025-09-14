#!/usr/bin/env python3
"""
Comprehensive Google Tech Stack Test
Tests all Google services integration
"""
import os
import sys
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append('src')

def test_google_services_integration():
    """Test comprehensive Google services integration"""
    print("🚀 COMPREHENSIVE GOOGLE TECH STACK TEST")
    print("=" * 60)
    
    try:
        from src.utils.google_services import google_services
        
        # Get status of all services
        status = google_services.get_status()
        
        print("📊 Google Services Status:")
        print(f"   Google Generative AI (Gemini): {'✅ WORKING' if status['gemini'] else '❌ NOT AVAILABLE'}")
        print(f"   Vertex AI: {'✅ WORKING' if status['vertex_ai'] else '❌ NOT AVAILABLE'}")
        print(f"   Firebase: {'✅ WORKING' if status['firebase'] else '❌ NOT AVAILABLE'}")
        print(f"   Google Cloud Storage: {'✅ WORKING' if status['storage'] else '❌ NOT AVAILABLE'}")
        print()
        
        # Test each service
        test_results = {}
        
        # Test 1: Google Generative AI (Gemini)
        if status['gemini']:
            print("🧪 Testing Google Generative AI (Gemini)...")
            try:
                test_prompt = "What is 2+2? Answer in one word."
                response = google_services.analyze_with_gemini(test_prompt)
                print(f"✅ Gemini Response: {response}")
                test_results['gemini'] = True
            except Exception as e:
                print(f"❌ Gemini test failed: {str(e)}")
                test_results['gemini'] = False
        else:
            print("⚠️ Gemini not available - check GOOGLE_API_KEY")
            test_results['gemini'] = False
        
        # Test 2: Vertex AI
        if status['vertex_ai']:
            print("\n🧪 Testing Vertex AI...")
            try:
                test_prompt = "Analyze this startup: TechFlow Solutions, AI-powered workflow automation. Provide investment recommendation."
                response = google_services.analyze_with_vertex_ai(test_prompt)
                print(f"✅ Vertex AI Response: {response[:200]}...")
                test_results['vertex_ai'] = True
            except Exception as e:
                print(f"❌ Vertex AI test failed: {str(e)}")
                test_results['vertex_ai'] = False
        else:
            print("⚠️ Vertex AI not available - check service account and APIs")
            test_results['vertex_ai'] = False
        
        # Test 3: Firebase
        if status['firebase']:
            print("\n🧪 Testing Firebase...")
            try:
                # Test storing data
                test_data = {
                    "test": True,
                    "timestamp": time.time(),
                    "message": "Firebase test data"
                }
                success = google_services.store_analysis_result("test_startup", test_data, "test_user")
                if success:
                    print("✅ Firebase storage test passed")
                    test_results['firebase'] = True
                else:
                    print("❌ Firebase storage test failed")
                    test_results['firebase'] = False
            except Exception as e:
                print(f"❌ Firebase test failed: {str(e)}")
                test_results['firebase'] = False
        else:
            print("⚠️ Firebase not available - check service account and Firestore setup")
            test_results['firebase'] = False
        
        # Test 4: Google Cloud Storage
        if status['storage']:
            print("\n🧪 Testing Google Cloud Storage...")
            try:
                # Test file upload
                test_data = b"Test file content for Google Cloud Storage"
                public_url = google_services.upload_file(test_data, "test_file.txt")
                print(f"✅ Cloud Storage test passed: {public_url}")
                test_results['storage'] = True
            except Exception as e:
                print(f"❌ Cloud Storage test failed: {str(e)}")
                test_results['storage'] = False
        else:
            print("⚠️ Cloud Storage not available - check service account and bucket setup")
            test_results['storage'] = False
        
        # Summary
        print("\n📊 COMPREHENSIVE TEST RESULTS:")
        print("=" * 40)
        working_services = sum(test_results.values())
        total_services = len(test_results)
        
        for service, status in test_results.items():
            print(f"   {service.upper()}: {'✅ WORKING' if status else '❌ NEEDS SETUP'}")
        
        print(f"\n🎯 Overall Status: {working_services}/{total_services} services working")
        
        if working_services >= 2:
            print("✅ SUFFICIENT FOR HACKATHON DEMO!")
            print("   You have enough Google services working to impress judges")
        elif working_services >= 1:
            print("⚠️ PARTIAL SETUP - Can demo basic features")
            print("   Consider setting up additional services for full impact")
        else:
            print("❌ NEEDS SETUP - No Google services working")
            print("   Please follow the setup guide to configure services")
        
        return test_results
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return {}

def test_startup_analysis():
    """Test complete startup analysis workflow"""
    print("\n🚀 TESTING COMPLETE STARTUP ANALYSIS WORKFLOW")
    print("=" * 60)
    
    try:
        from src.utils.google_services import google_services
        from src.models.startup import StartupInput
        
        # Create test startup
        test_startup = StartupInput(
            company_name="TestAI Solutions",
            business_description="AI-powered test automation platform for software development teams. Reduces testing time by 80% and improves code quality.",
            industry="DevTools",
            stage="Series A",
            founder_name="Jane Smith",
            founder_background="Former Google engineer with 10 years in test automation. PhD in Computer Science from MIT."
        )
        
        print(f"📊 Analyzing: {test_startup.company_name}")
        print(f"Business: {test_startup.business_description}")
        print()
        
        # Choose AI service
        if google_services.vertex_ai_initialized:
            print("🤖 Using Vertex AI for analysis...")
            ai_service = "Vertex AI"
            prompt = f"""
            As an expert startup investment analyst using Google's Vertex AI, analyze this startup:

            COMPANY: {test_startup.company_name}
            BUSINESS: {test_startup.business_description}
            INDUSTRY: {test_startup.industry}
            STAGE: {test_startup.stage}
            FOUNDER: {test_startup.founder_name}
            FOUNDER BACKGROUND: {test_startup.founder_background}

            Provide a comprehensive investment analysis including:
            1. Market Analysis
            2. Business Model Assessment
            3. Risk Assessment
            4. Investment Recommendation (INVEST/PASS/WATCH)
            5. Key Investment Thesis
            6. Due Diligence Priorities

            Be specific and actionable.
            """
            
            try:
                analysis = google_services.analyze_with_vertex_ai(prompt)
                print("✅ Vertex AI analysis completed")
            except Exception as e:
                print(f"❌ Vertex AI analysis failed: {str(e)}")
                return False
                
        elif google_services.gemini_initialized:
            print("🤖 Using Google Generative AI (Gemini) for analysis...")
            ai_service = "Google Generative AI (Gemini)"
            prompt = f"""
            As an expert startup investment analyst using Google's Gemini AI, analyze this startup:

            COMPANY: {test_startup.company_name}
            BUSINESS: {test_startup.business_description}
            INDUSTRY: {test_startup.industry}
            STAGE: {test_startup.stage}
            FOUNDER: {test_startup.founder_name}

            Provide a comprehensive investment analysis with clear recommendations.
            """
            
            try:
                analysis = google_services.analyze_with_gemini(prompt)
                print("✅ Gemini analysis completed")
            except Exception as e:
                print(f"❌ Gemini analysis failed: {str(e)}")
                return False
        else:
            print("❌ No AI services available")
            return False
        
        # Store results in Firebase if available
        if google_services.firebase_initialized:
            print("💾 Storing results in Firebase...")
            try:
                google_services.store_analysis_result("test_startup", {
                    "analysis": analysis,
                    "ai_service": ai_service,
                    "startup_data": test_startup.dict()
                }, "test_user")
                print("✅ Results stored in Firebase")
            except Exception as e:
                print(f"⚠️ Firebase storage failed: {str(e)}")
        
        # Display analysis
        print(f"\n📋 {ai_service} ANALYSIS RESULTS:")
        print("=" * 50)
        print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
        
        print(f"\n🎉 COMPLETE WORKFLOW TEST SUCCESSFUL!")
        print(f"   AI Service: {ai_service}")
        print(f"   Firebase: {'✅ Connected' if google_services.firebase_initialized else '❌ Not available'}")
        print(f"   Storage: {'✅ Connected' if google_services.storage_initialized else '❌ Not available'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow test failed: {str(e)}")
        return False

def main():
    """Run comprehensive tests"""
    print("🎯 HACKATHON READINESS TEST - GOOGLE TECH STACK")
    print("=" * 60)
    print("This test verifies your prototype is ready for hackathon judges!")
    print()
    
    # Test 1: Google Services Integration
    test_results = test_google_services_integration()
    
    # Test 2: Complete Workflow
    if any(test_results.values()):
        workflow_success = test_startup_analysis()
    else:
        print("\n⚠️ Skipping workflow test - no Google services available")
        workflow_success = False
    
    # Final assessment
    print("\n🏆 HACKATHON READINESS ASSESSMENT")
    print("=" * 50)
    
    working_services = sum(test_results.values())
    total_services = len(test_results)
    
    if working_services >= 3 and workflow_success:
        print("🎉 EXCELLENT! Ready for hackathon!")
        print("   ✅ Multiple Google services working")
        print("   ✅ Complete workflow functional")
        print("   ✅ Judges will be impressed")
    elif working_services >= 2 and workflow_success:
        print("✅ GOOD! Ready for hackathon demo!")
        print("   ✅ Core Google services working")
        print("   ✅ Basic workflow functional")
        print("   ✅ Sufficient for judges")
    elif working_services >= 1:
        print("⚠️ PARTIAL - Can demo basic features")
        print("   ⚠️ Limited Google services")
        print("   ⚠️ Consider setting up more services")
    else:
        print("❌ NEEDS WORK - Not ready for hackathon")
        print("   ❌ No Google services working")
        print("   ❌ Please follow setup guide")
    
    print(f"\n📊 Final Score: {working_services}/{total_services} services + {'✅' if workflow_success else '❌'} workflow")
    
    return working_services >= 2 and workflow_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
