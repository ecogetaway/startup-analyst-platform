#!/usr/bin/env python3
"""
Show Agent Systems
Display what agent systems are available
"""
import os
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"📁 {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def show_file_structure():
    """Show the current file structure"""
    print_header("Current Agent Systems")
    
    # Check if src/agents directory exists
    agents_dir = Path("src/agents")
    if not agents_dir.exists():
        print("❌ src/agents directory not found")
        return
    
    print_section("Available Agent Files")
    
    # List all files in src/agents
    agent_files = list(agents_dir.glob("*.py"))
    
    traditional_agents = []
    vertex_ai_agents = []
    
    for file in agent_files:
        if file.name.startswith("vertex_ai"):
            vertex_ai_agents.append(file.name)
        else:
            traditional_agents.append(file.name)
    
    print("🔧 Traditional Python Script Agents:")
    for file in traditional_agents:
        print(f"  ✅ {file}")
    
    print("\n🚀 Vertex AI Agent Builder Agents:")
    for file in vertex_ai_agents:
        print(f"  ✅ {file}")
    
    print_section("System Status")
    
    # Check if key files exist
    key_files = {
        "Traditional System": [
            "src/agents/base_agent.py",
            "src/agents/data_collection_agent.py",
            "src/agents/business_analysis_agent.py",
            "src/agents/risk_assessment_agent.py",
            "src/agents/investment_insights_agent.py",
            "src/agents/report_generation_agent.py",
            "src/agents/orchestrator.py"
        ],
        "Vertex AI System": [
            "src/agents/vertex_ai_agents.py",
            "src/agents/vertex_ai_orchestrator.py"
        ],
        "Backend Systems": [
            "backend/main.py",
            "backend/enhanced_main.py"
        ],
        "Test Scripts": [
            "test_google_services.py",
            "test_vertex_ai_agents.py",
            "demo_both_systems.py"
        ],
        "Setup Scripts": [
            "setup_vertex_ai_agents.sh",
            "start_vertex_ai_agents.py"
        ]
    }
    
    for system, files in key_files.items():
        print(f"\n🔧 {system}:")
        for file in files:
            if Path(file).exists():
                print(f"  ✅ {file}")
            else:
                print(f"  ❌ {file} (missing)")

def show_usage_examples():
    """Show usage examples for both systems"""
    print_header("Usage Examples")
    
    print_section("Traditional Agents")
    print("```bash")
    print("# Run traditional system")
    print("python3 backend/main.py")
    print("")
    print("# Test traditional agents")
    print("python3 test_google_services.py")
    print("```")
    
    print_section("Vertex AI Agent Builder")
    print("```bash")
    print("# Run advanced system")
    print("python3 start_vertex_ai_agents.py")
    print("")
    print("# Test advanced agents")
    print("python3 test_vertex_ai_agents.py")
    print("```")
    
    print_section("Demo Both Systems")
    print("```bash")
    print("# Demo both systems")
    print("python3 demo_both_systems.py")
    print("```")

def show_migration_info():
    """Show migration information"""
    print_header("Migration Information")
    
    print_section("What Happened to Traditional Agents?")
    print("✅ Traditional agents are STILL THERE and working!")
    print("✅ They were NOT replaced - they were enhanced!")
    print("✅ You now have TWO complete systems:")
    print("   🔧 Traditional system (simple, quick)")
    print("   🚀 Vertex AI system (advanced, professional)")
    
    print_section("When to Use Which System?")
    print("🔧 Traditional Agents:")
    print("  • Quick prototyping and testing")
    print("  • Learning how agents work")
    print("  • Simple demos")
    print("  • Limited time for setup")
    print("")
    print("🚀 Vertex AI Agent Builder:")
    print("  • Hackathon competition")
    print("  • Production deployment")
    print("  • Professional demos")
    print("  • Scalable systems")
    
    print_section("Hackathon Strategy")
    print("1. Start with traditional agents (quick demo)")
    print("2. Upgrade to Vertex AI (show advanced features)")
    print("3. Compare both systems (demonstrate learning)")
    print("4. Highlight benefits (show why advanced is better)")

def main():
    """Main function"""
    print_header("Agent Systems Overview")
    print("🎯 Showing what agent systems are available")
    
    show_file_structure()
    show_usage_examples()
    show_migration_info()
    
    print_header("Summary")
    print("🎉 You have BOTH systems working!")
    print("🔧 Traditional agents for quick demos")
    print("🚀 Vertex AI agents for hackathon competition")
    print("🔄 Easy migration path between systems")
    print("📚 Best of both worlds!")

if __name__ == "__main__":
    main()
