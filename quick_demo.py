#!/usr/bin/env python3
"""
Quick web demo for judges - shows Google AI in action
"""
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Startup Analyst - Google AI Demo",
    page_icon="🚀",
    layout="wide"
)

# Configure Google AI
@st.cache_resource
def setup_google_ai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Google API key not found. Please set GOOGLE_API_KEY in .env file")
        return None
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def analyze_startup(startup_data):
    """Analyze startup using Google AI"""
    model = setup_google_ai()
    if not model:
        return None
    
    prompt = f"""
    As an expert startup investment analyst using Google's advanced AI, analyze this startup:

    COMPANY: {startup_data['company_name']}
    BUSINESS: {startup_data['business_description']}
    INDUSTRY: {startup_data.get('industry', 'Not specified')}
    STAGE: {startup_data.get('stage', 'Not specified')}
    FOUNDER: {startup_data.get('founder_name', 'Not specified')}

    Provide a comprehensive analysis including:
    1. Market Analysis (size, growth, competition)
    2. Business Model Assessment (viability, scalability)
    3. Risk Assessment (market, technology, team risks)
    4. Investment Recommendation (INVEST/PASS/WATCH with confidence score 1-10)
    5. Key Investment Thesis (3-5 bullet points)
    6. Due Diligence Priorities

    Be specific and actionable for investment decision-making.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Analysis failed: {str(e)}"

# Main app
def main():
    st.title("🚀 Startup Analyst Platform")
    st.subheader("Powered by Google's Gemini AI")
    
    # Google AI status
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**🤖 Using Google's Gemini 1.5 Flash model for real-time analysis**")
    with col2:
        if os.getenv("GOOGLE_API_KEY"):
            st.success("✅ Google AI Connected")
        else:
            st.error("❌ Google AI Not Connected")
    
    st.markdown("---")
    
    # Demo scenarios
    st.subheader("🎯 Demo Scenarios")
    
    scenarios = {
        "High-Potential AI Startup": {
            "company_name": "MedAI Solutions",
            "business_description": "AI-powered diagnostic platform that helps doctors identify diseases from medical images with 95% accuracy. Our platform reduces diagnosis time by 70% and improves patient outcomes.",
            "industry": "Healthcare AI",
            "stage": "Series A",
            "founder_name": "Dr. Sarah Chen"
        },
        "Risky Consumer App": {
            "company_name": "SocialSnap",
            "business_description": "Social media app for sharing photos with friends. Features include filters, stories, and group chats. Targeting Gen Z users.",
            "industry": "Social Media",
            "stage": "Seed",
            "founder_name": "Mike Johnson"
        },
        "Watch List B2B SaaS": {
            "company_name": "WorkflowAI",
            "business_description": "AI-powered workflow automation platform for small businesses. Automates repetitive tasks and improves productivity by 40%.",
            "industry": "B2B SaaS",
            "stage": "Seed",
            "founder_name": "Alex Rodriguez"
        }
    }
    
    # Scenario selection
    selected_scenario = st.selectbox("Choose a demo scenario:", list(scenarios.keys()))
    
    if st.button("🚀 Analyze with Google AI", type="primary"):
        startup_data = scenarios[selected_scenario]
        
        # Show analysis progress
        with st.spinner("🤖 Running Google AI analysis..."):
            start_time = time.time()
            analysis = analyze_startup(startup_data)
            end_time = time.time()
        
        if analysis:
            st.success(f"✅ Analysis completed in {end_time - start_time:.2f} seconds")
            
            # Display results
            st.markdown("---")
            st.subheader("📊 Google AI Analysis Results")
            
            # Show startup info
            st.markdown("**Startup Information:**")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Company:** {startup_data['company_name']}")
                st.write(f"**Industry:** {startup_data['industry']}")
            with col2:
                st.write(f"**Stage:** {startup_data['stage']}")
                st.write(f"**Founder:** {startup_data['founder_name']}")
            
            st.write(f"**Business:** {startup_data['business_description']}")
            
            # Show analysis
            st.markdown("**AI Analysis:**")
            st.markdown(analysis)
            
            # Show Google AI branding
            st.markdown("---")
            st.markdown("**🎯 This analysis was generated by Google's Gemini AI in real-time!**")
            st.markdown("- Using Google's latest AI model")
            st.markdown("- Professional investment analysis")
            st.markdown("- Ready for hackathon demo")
        else:
            st.error("Analysis failed. Please check your Google API key.")

if __name__ == "__main__":
    main()
