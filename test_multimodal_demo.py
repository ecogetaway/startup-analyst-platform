#!/usr/bin/env python3
"""
Multi-Modal Pitch Processing Demo
Tests document, audio, and video processing capabilities
"""
import sys
import asyncio
import time
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add src to path
sys.path.append('src')

from src.agents.multimodal_ingestion_agent import multimodal_processor, deal_memo_generator

async def test_multimodal_processing():
    """Test multi-modal pitch processing capabilities"""
    print("🎬 Multi-Modal Pitch Processing Demo")
    print("=" * 60)
    
    # Simulate uploaded files for different types
    demo_files = [
        {
            "name": "TechFlow_AI_Pitch_Deck.pdf",
            "type": "document",
            "content_type": "application/pdf",
            "size": 2_500_000,  # 2.5MB
            "public_url": "https://storage.googleapis.com/demo-bucket/pitch_deck.pdf",
            "storage_path": "startups/techflow_ai/pitch_deck.pdf"
        },
        {
            "name": "Founder_Voice_Pitch.mp3",
            "type": "audio",
            "content_type": "audio/mpeg",
            "size": 8_500_000,  # 8.5MB
            "public_url": "https://storage.googleapis.com/demo-bucket/voice_pitch.mp3",
            "storage_path": "startups/techflow_ai/voice_pitch.mp3"
        },
        {
            "name": "Investor_Presentation_Video.mp4",
            "type": "video", 
            "content_type": "video/mp4",
            "size": 45_000_000,  # 45MB
            "public_url": "https://storage.googleapis.com/demo-bucket/presentation.mp4",
            "storage_path": "startups/techflow_ai/presentation.mp4"
        }
    ]
    
    startup_info = {
        "company_name": "TechFlow AI",
        "industry": "Artificial Intelligence",
        "stage": "Series A",
        "founder_name": "Sarah Chen",
        "funding_request": "$5M",
        "business_description": "AI-powered analytics platform for small businesses"
    }
    
    print(f"🚀 Processing Multi-Modal Pitch for: {startup_info['company_name']}")
    print(f"Files to process: {len(demo_files)}")
    
    for file in demo_files:
        print(f"  📄 {file['name']} ({file['type']}) - {file['size'] // 1024 // 1024}MB")
    
    print("\n" + "=" * 60)
    
    try:
        start_time = time.time()
        
        # Process multi-modal content
        print("🔄 Processing multi-modal content...")
        analysis_results = await multimodal_processor.process_pitch_materials(
            demo_files,
            startup_info
        )
        
        processing_time = time.time() - start_time
        
        print(f"✅ Multi-modal processing completed in {processing_time:.2f} seconds")
        print("\n📊 Processing Results:")
        print(f"  Documents processed: {len(analysis_results.get('documents', []))}")
        print(f"  Audio transcripts: {len(analysis_results.get('audio_transcripts', []))}")
        print(f"  Video analyses: {len(analysis_results.get('video_analysis', []))}")
        
        # Show detailed results for each type
        print("\n🔍 Detailed Analysis Results:")
        
        # Document Analysis
        documents = analysis_results.get('documents', [])
        if documents:
            print("\n📄 Document Analysis:")
            for doc in documents:
                print(f"  File: {doc.get('file_name', 'Unknown')}")
                print(f"  Quality Score: {doc.get('quality_score', 'N/A')}")
                print(f"  Key Insights: {len(doc.get('key_insights', []))} insights extracted")
                
                # Show sample insights
                insights = doc.get('key_insights', [])
                for i, insight in enumerate(insights[:3], 1):
                    print(f"    {i}. {insight[:80]}...")
        
        # Audio Analysis
        audio_transcripts = analysis_results.get('audio_transcripts', [])
        if audio_transcripts:
            print("\n🎤 Audio Analysis:")
            for audio in audio_transcripts:
                print(f"  File: {audio.get('file_name', 'Unknown')}")
                print(f"  Duration: {audio.get('duration_estimate', 'Unknown')}")
                print(f"  Quality Score: {audio.get('quality_score', 'N/A')}")
                
                speech_analysis = audio.get('speech_analysis', {})
                if speech_analysis:
                    print(f"  Speech Clarity: {speech_analysis.get('clarity', 'N/A')}")
                    print(f"  Confidence Level: {speech_analysis.get('confidence', 'N/A')}")
                    print(f"  Key Messages: {len(speech_analysis.get('key_messages', []))}")
        
        # Video Analysis
        video_analyses = analysis_results.get('video_analysis', [])
        if video_analyses:
            print("\n🎥 Video Analysis:")
            for video in video_analyses:
                print(f"  File: {video.get('file_name', 'Unknown')}")
                print(f"  Duration: {video.get('duration_estimate', 'Unknown')}")
                print(f"  Video Quality: {video.get('video_quality', 'Unknown')}")
                
                visual_analysis = video.get('visual_analysis', {})
                if visual_analysis:
                    print(f"  Slide Count: {visual_analysis.get('slide_count', 'N/A')}")
                    print(f"  Presentation Quality: {visual_analysis.get('presentation_quality', 'N/A')}")
                
                presenter_analysis = video.get('presenter_analysis', {})
                if presenter_analysis:
                    print(f"  Confidence Level: {presenter_analysis.get('confidence_level', 'N/A')}")
                    print(f"  Presentation Skills: {presenter_analysis.get('presentation_skills', 'N/A')}")
        
        # Combined Insights
        combined_insights = analysis_results.get('combined_insights', '')
        if combined_insights and len(combined_insights) > 100:
            print(f"\n🧠 AI Synthesis:")
            print(f"  {combined_insights[:300]}...")
        
        print("\n" + "=" * 60)
        
        # Generate Deal Memo
        print("📝 Generating Structured Investment Memo...")
        memo_start_time = time.time()
        
        deal_memo = await deal_memo_generator.generate_investment_memo(
            analysis_results,
            startup_info
        )
        
        memo_time = time.time() - memo_start_time
        
        print(f"✅ Investment memo generated in {memo_time:.2f} seconds")
        
        if 'error' not in deal_memo:
            memo_metadata = deal_memo.get('memo_metadata', {})
            print(f"\n📋 Investment Memo Details:")
            print(f"  Memo ID: {memo_metadata.get('memo_id', 'Unknown')}")
            print(f"  Company: {memo_metadata.get('company_name', 'Unknown')}")
            print(f"  Confidence Score: {memo_metadata.get('confidence_score', 'N/A')}")
            print(f"  Sources Analyzed: {memo_metadata.get('total_content_processed', 'Unknown')}")
            
            # Show executive summary
            exec_summary = deal_memo.get('executive_summary', '')
            if exec_summary:
                print(f"\n📄 Executive Summary Preview:")
                print(f"  {exec_summary[:200]}...")
            
            # Show investment recommendation
            recommendation = deal_memo.get('investment_recommendation', 'Unknown')
            print(f"\n💰 Investment Recommendation: {recommendation}")
            
            # Show key metrics
            key_metrics = deal_memo.get('key_metrics', [])
            if key_metrics:
                print(f"\n📊 Key Metrics Identified:")
                for metric in key_metrics[:3]:
                    print(f"  • {metric}")
            
            # Show risk factors
            risk_factors = deal_memo.get('risk_factors', [])
            if risk_factors:
                print(f"\n⚠️ Key Risk Factors:")
                for risk in risk_factors[:3]:
                    print(f"  • {risk}")
            
            # Show next steps
            next_steps = deal_memo.get('next_steps', [])
            if next_steps:
                print(f"\n📋 Recommended Next Steps:")
                for step in next_steps[:3]:
                    print(f"  • {step}")
        
        print("\n" + "=" * 60)
        print("🎉 Multi-Modal Processing Demo Complete!")
        
        print(f"\n📈 Performance Summary:")
        print(f"  Total Processing Time: {processing_time + memo_time:.2f} seconds")
        print(f"  Multi-Modal Analysis: {processing_time:.2f}s")
        print(f"  Deal Memo Generation: {memo_time:.2f}s")
        print(f"  Files Processed: {len(demo_files)}")
        print(f"  Content Types: Document, Audio, Video")
        
        return True
        
    except Exception as e:
        print(f"❌ Multi-modal processing failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def demo_capabilities():
    """Demonstrate capabilities without actual processing"""
    print("🎯 Multi-Modal Capabilities Overview")
    print("=" * 60)
    
    capabilities = {
        "📄 Document Processing": [
            "Extract structured content from pitch decks",
            "Analyze financial projections and metrics", 
            "Identify key business model components",
            "Assess presentation quality and completeness",
            "Parse team information and credentials"
        ],
        "🎤 Audio Processing": [
            "Speech-to-text transcription",
            "Analyze founder presentation skills",
            "Assess message clarity and confidence",
            "Extract key value propositions",
            "Evaluate pitch effectiveness"
        ],
        "🎥 Video Processing": [
            "Visual presentation analysis",
            "Speaker assessment and body language",
            "Slide content extraction and quality",
            "Presentation flow and structure",
            "Overall pitch effectiveness scoring"
        ],
        "📝 Deal Memo Generation": [
            "Professional investment committee format",
            "Executive summary and recommendations",
            "Risk assessment and mitigation strategies",
            "Financial analysis and projections",
            "Next steps and due diligence priorities"
        ]
    }
    
    for category, features in capabilities.items():
        print(f"\n{category}:")
        for feature in features:
            print(f"  ✅ {feature}")
    
    print(f"\n🔧 Technical Integration:")
    print("  • Google Cloud Speech-to-Text API")
    print("  • Google Cloud Video Intelligence API") 
    print("  • Google Document AI")
    print("  • Gemini AI for content synthesis")
    print("  • Firebase for real-time progress")
    print("  • Cloud Storage for file management")
    
    print(f"\n🎯 Business Value:")
    print("  • Comprehensive founder assessment")
    print("  • Multi-format pitch analysis")
    print("  • Automated deal memo generation")
    print("  • Consistent evaluation criteria")
    print("  • Faster investment decisions")

if __name__ == "__main__":
    async def main():
        try:
            # Show capabilities overview
            demo_capabilities()
            
            print("\n" + "=" * 60)
            
            # Run actual processing demo
            await test_multimodal_processing()
            
        except Exception as e:
            print(f"❌ Demo failed: {str(e)}")
            sys.exit(1)
    
    # Install python-dotenv if needed
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("Installing python-dotenv...")
        import os
        os.system("pip3 install python-dotenv")
        from dotenv import load_dotenv
    
    # Run the demo
    asyncio.run(main())
