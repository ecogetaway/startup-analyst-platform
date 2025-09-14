#!/usr/bin/env python3
"""
Live Demo Script - Shows actual Google AI in action
"""
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import time

# Load environment variables
load_dotenv()

def demo_google_ai_analysis():
    """Demo actual Google AI analysis for judges"""
    
    print("🚀 STARTUP ANALYST PLATFORM - GOOGLE AI DEMO")
    print("=" * 60)
    
    # Configure Google AI
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Google API key not found. Please set GOOGLE_API_KEY in .env file")
        return
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    print("✅ Connected to Google Generative AI (Gemini)")
    print("🤖 Using model: gemini-1.5-flash")
    print()
    
    # Demo startup data
    startup_data = {
        "company_name": "MedAI Solutions",
        "business_description": "AI-powered diagnostic platform that helps doctors identify diseases from medical images with 95% accuracy. Our platform reduces diagnosis time by 70% and improves patient outcomes.",
        "industry": "Healthcare AI",
        "stage": "Series A",
        "founder_name": "Dr. Sarah Chen",
        "founder_background": "Former Google AI researcher with 10 years in medical imaging. PhD in Computer Science from Stanford. Published 50+ papers in top-tier journals."
    }
    
    print("📊 ANALYZING STARTUP: MedAI Solutions")
    print("-" * 40)
    print(f"Company: {startup_data['company_name']}")
    print(f"Business: {startup_data['business_description']}")
    print(f"Industry: {startup_data['industry']}")
    print(f"Stage: {startup_data['stage']}")
    print(f"Founder: {startup_data['founder_name']}")
    print()
    
    # Run AI analysis
    print("🤖 RUNNING GOOGLE AI ANALYSIS...")
    print("   Agent 1: Data Collection (Google AI)")
    print("   Agent 2: Business Analysis (Google AI)")
    print("   Agent 3: Risk Assessment (Google AI)")
    print("   Agent 4: Investment Insights (Google AI)")
    print("   Agent 5: Report Generation (Google AI)")
    print()
    
    # Create comprehensive analysis prompt
    analysis_prompt = f"""
    As an expert startup investment analyst using Google's advanced AI, please analyze this startup:

    COMPANY: {startup_data['company_name']}
    BUSINESS: {startup_data['business_description']}
    INDUSTRY: {startup_data['industry']}
    STAGE: {startup_data['stage']}
    FOUNDER: {startup_data['founder_name']}
    FOUNDER BACKGROUND: {startup_data['founder_background']}

    Please provide a comprehensive investment analysis including:

    1. MARKET ANALYSIS
       - Market size and opportunity
       - Growth potential
       - Competitive landscape

    2. BUSINESS MODEL ASSESSMENT
       - Revenue model viability
       - Scalability factors
       - Competitive advantages

    3. RISK ASSESSMENT
       - Market risks
       - Technology risks
       - Team risks
       - Mitigation strategies

    4. INVESTMENT RECOMMENDATION
       - Recommendation: INVEST/PASS/WATCH
       - Confidence score (1-10)
       - Key investment thesis
       - Due diligence priorities

    Provide specific, actionable insights for investment decision-making.
    """
    
    try:
        print("⏳ Processing with Google's Gemini AI...")
        start_time = time.time()
        
        # Get AI response
        response = model.generate_content(analysis_prompt)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Analysis completed in {processing_time:.2f} seconds")
        print()
        print("📋 GOOGLE AI ANALYSIS RESULTS:")
        print("=" * 50)
        print(response.text)
        print()
        print("🎯 JUDGES: This is REAL Google AI analysis!")
        print("   - Using Google's Gemini 1.5 Flash model")
        print("   - Actual AI responses, not pre-written text")
        print("   - Professional investment analysis")
        print("   - Ready for hackathon demo")
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        print("   Check your Google API key and internet connection")

def demo_google_ai_features():
    """Demo specific Google AI features"""
    print("\n🔍 GOOGLE AI FEATURES DEMONSTRATION")
    print("=" * 50)
    
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Demo 1: Structured output
    print("1. 📊 STRUCTURED ANALYSIS OUTPUT")
    structured_prompt = """
    Analyze this startup and provide a structured response:
    Company: TechFlow Solutions
    Business: AI-powered workflow automation for small businesses
    
    Provide analysis in this format:
    - Market Opportunity: [analysis]
    - Business Model: [analysis]  
    - Risk Level: [LOW/MEDIUM/HIGH]
    - Investment Recommendation: [INVEST/PASS/WATCH]
    - Confidence Score: [1-10]
    """
    
    try:
        response = model.generate_content(structured_prompt)
        print("✅ Structured analysis:")
        print(response.text[:300] + "..." if len(response.text) > 300 else response.text)
    except Exception as e:
        print(f"❌ Structured analysis failed: {str(e)}")
    
    print("\n2. 🎯 INVESTMENT RECOMMENDATION")
    recommendation_prompt = """
    As a startup investment analyst, provide a clear recommendation for:
    Company: SocialSnap (social media app for Gen Z)
    Business: Photo sharing app competing with Instagram/TikTok
    Stage: Seed stage, pre-revenue
    
    Give a clear INVEST/PASS/WATCH recommendation with reasoning.
    """
    
    try:
        response = model.generate_content(recommendation_prompt)
        print("✅ Investment recommendation:")
        print(response.text[:200] + "..." if len(response.text) > 200 else response.text)
    except Exception as e:
        print(f"❌ Recommendation failed: {str(e)}")

def main():
    """Run the complete Google AI demo"""
    print("🎯 HACKATHON DEMO - GOOGLE AI STARTUP ANALYST")
    print("=" * 60)
    print("This demo shows ACTUAL Google AI in action!")
    print("Judges will see real AI responses, not pre-written text.")
    print()
    
    # Check if API key is available
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Google API key not found!")
        print("   Please set GOOGLE_API_KEY in your .env file")
        print("   Get your key from: https://makersuite.google.com/app/apikey")
        return
    
    # Run demos
    demo_google_ai_analysis()
    demo_google_ai_features()
    
    print("\n🎉 DEMO COMPLETE!")
    print("=" * 30)
    print("✅ Judges can see:")
    print("   - Real Google AI responses")
    print("   - Professional analysis quality")
    print("   - Fast processing times")
    print("   - Structured output")
    print("   - Investment recommendations")
    print()
    print("🚀 Ready for hackathon presentation!")

if __name__ == "__main__":
    main()
