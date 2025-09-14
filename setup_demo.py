#!/usr/bin/env python3
"""
Quick setup script for hackathon demo
"""
import os
import sys
from dotenv import load_dotenv

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 CHECKING DEMO REQUIREMENTS...")
    print("=" * 50)
    
    # Check .env file
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
        return False
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print("✅ Google API key found")
        print(f"   Key starts with: {api_key[:10]}...")
    else:
        print("❌ Google API key not found in .env file")
        return False
    
    # Check required packages
    try:
        import google.generativeai
        print("✅ google-generativeai package installed")
    except ImportError:
        print("❌ google-generativeai package not installed")
        print("   Run: pip3 install google-generativeai")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv package installed")
    except ImportError:
        print("❌ python-dotenv package not installed")
        print("   Run: pip3 install python-dotenv")
        return False
    
    print("\n🎉 ALL REQUIREMENTS MET!")
    print("   Your demo is ready to run!")
    return True

def show_demo_commands():
    """Show available demo commands"""
    print("\n🚀 AVAILABLE DEMO COMMANDS:")
    print("=" * 50)
    print("1. Enhanced Hackathon Demo:")
    print("   python3 hackathon_demo_enhanced.py")
    print()
    print("2. Original Google AI Demo:")
    print("   python3 demo_google_ai.py")
    print()
    print("3. Quick Demo (if you have Streamlit):")
    print("   python3 quick_demo.py")
    print()
    print("4. Test Google AI Connection:")
    print("   python3 test_gemini.py")
    print()

def main():
    """Main setup function"""
    print("🎯 HACKATHON DEMO SETUP")
    print("=" * 50)
    
    if check_requirements():
        show_demo_commands()
        print("🏆 READY FOR HACKATHON!")
        print("   Run the enhanced demo to impress the judges!")
    else:
        print("\n❌ SETUP INCOMPLETE")
        print("   Please fix the issues above before running the demo")

if __name__ == "__main__":
    main()
