#!/usr/bin/env python3
"""
Startup script for Vertex AI Agent Builder System
Quick start for hackathon demo
"""
import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 40)

async def main():
    """Main startup function"""
    print_header("Vertex AI Agent Builder System")
    print("🎯 Starting advanced AI agent system for hackathon demo")
    
    try:
        # Import and initialize
        from src.config.logging import setup_logging
        from src.agents.vertex_ai_orchestrator import VertexAIOrchestrator
        
        # Set up logging
        logger = setup_logging()
        logger.info("🚀 Starting Vertex AI Agent Builder System")
        
        print_section("Initializing System")
        print("• Loading Vertex AI Agent Builder")
        print("• Setting up Google ADK orchestration")
        print("• Connecting to Firebase")
        
        # Initialize orchestrator
        orchestrator = VertexAIOrchestrator()
        
        print_section("System Health Check")
        # Health check
        health_status = await orchestrator.health_check()
        print(f"Overall Status: {health_status['overall_status']}")
        
        # Display component status
        components = health_status.get('components', {})
        for component, status in components.items():
            if isinstance(status, dict):
                print(f"  {component}: {status.get('status', 'unknown')}")
        
        print_section("Agent Status")
        # Monitor agent status
        agent_status = orchestrator.get_agent_status()
        for agent_name, status in agent_status.items():
            print(f"  {agent_name}: {status.get('status', 'unknown')}")
        
        print_section("System Ready")
        print("✅ Vertex AI Agent Builder System is operational!")
        print("🎯 All agents are ready for startup analysis")
        print("🏆 System ready for hackathon demonstration")
        
        # Keep system running
        print_section("System Running")
        print("🔄 System is now running and ready for requests")
        print("📊 Use demo_vertex_ai_only.py for full demonstration")
        print("⏹️ Press Ctrl+C to stop")
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 System stopped by user")
        
        return True
        
    except Exception as e:
        print(f"❌ Startup failed: {str(e)}")
        print("🔧 Please check your configuration:")
        print("  • .env file with correct values")
        print("  • service-account-key.json file")
        print("  • Google Cloud APIs enabled")
        print("  • Firebase project configured")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("✅ System started successfully!")
    else:
        print("❌ System startup failed!")
        sys.exit(1)
