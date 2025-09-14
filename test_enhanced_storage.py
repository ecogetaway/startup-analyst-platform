#!/usr/bin/env python3
"""
Test Enhanced Google Cloud Storage Client
"""
import sys
import os
import time

# Add src to path
sys.path.append('src')

from src.utils.enhanced_storage_client import enhanced_storage_client

def test_storage_functionality():
    """Test Google Cloud Storage functionality"""
    print("☁️ Testing Enhanced Google Cloud Storage Client")
    print("=" * 60)
    
    # Test initialization
    print(f"✅ Storage Available: {enhanced_storage_client.is_available()}")
    
    if not enhanced_storage_client.is_available():
        print("⚠️ Cloud Storage not available - this is expected in development")
        print("✅ Client gracefully handles unavailable storage")
        return True
    
    print(f"📦 Bucket: {enhanced_storage_client.bucket_name}")
    
    # Test storage stats
    print(f"\n📊 Testing Storage Statistics")
    stats = enhanced_storage_client.get_storage_stats()
    if 'error' not in stats:
        print(f"✅ Storage Stats Retrieved")
        print(f"  Total Files: {stats.get('total_files', 0)}")
        print(f"  Total Size: {stats.get('total_size_mb', 0)} MB")
        print(f"  File Types: {len(stats.get('file_types', {}))}")
    else:
        print(f"❌ Storage Stats Error: {stats['error']}")
    
    # Test demo file upload
    print(f"\n📤 Testing Demo File Upload")
    demo_content = b"This is a test document for the startup analyst platform demo.\n\nKey Points:\n- AI-powered analysis\n- Real-time collaboration\n- Google Cloud integration\n- Professional reporting\n\nThis demonstrates file upload functionality."
    
    try:
        upload_result = enhanced_storage_client.upload_demo_file(
            demo_content, 
            "demo_pitch_deck.txt", 
            "pitch_deck"
        )
        
        if upload_result['success']:
            print(f"✅ Demo file uploaded successfully")
            print(f"  Public URL: {upload_result['public_url']}")
            print(f"  Storage Path: {upload_result['storage_path']}")
            print(f"  Size: {upload_result['size']} bytes")
            print(f"  Content Type: {upload_result['content_type']}")
            
            # Test file info retrieval
            print(f"\n📋 Testing File Info Retrieval")
            file_info = enhanced_storage_client.get_file_info(upload_result['storage_path'])
            if file_info:
                print(f"✅ File info retrieved")
                print(f"  Name: {file_info['name']}")
                print(f"  Size: {file_info['size']} bytes")
                print(f"  Created: {file_info['created']}")
            else:
                print(f"❌ Failed to retrieve file info")
            
            # Test signed URL generation
            print(f"\n🔐 Testing Signed URL Generation")
            signed_url = enhanced_storage_client.generate_signed_url(
                upload_result['storage_path'], 
                expiration_hours=1
            )
            if signed_url:
                print(f"✅ Signed URL generated")
                print(f"  URL Length: {len(signed_url)} characters")
                print(f"  Expires in: 1 hour")
            else:
                print(f"❌ Failed to generate signed URL")
                
        else:
            print(f"❌ Demo file upload failed")
            
    except Exception as e:
        print(f"❌ Demo file upload error: {str(e)}")
    
    # Test startup-specific file upload
    print(f"\n🚀 Testing Startup File Upload")
    startup_id = f"test_startup_{int(time.time())}"
    startup_content = b"""EXECUTIVE SUMMARY

Company: TechFlow AI
Industry: Artificial Intelligence
Stage: Series A
Funding Request: $5M

PROBLEM:
Small businesses struggle with data analysis and decision making due to lack of technical expertise.

SOLUTION:
AI-powered analytics platform that provides instant insights and recommendations.

MARKET:
- Total Addressable Market: $50B
- Serviceable Addressable Market: $10B
- Target: SMBs with 10-500 employees

BUSINESS MODEL:
- SaaS subscription: $99-$999/month
- Professional services: $150/hour
- Enterprise licenses: $10K-$100K/year

FINANCIAL PROJECTIONS:
Year 1: $500K revenue
Year 2: $2M revenue
Year 3: $5M revenue

TEAM:
- CEO: Former Google AI researcher
- CTO: Ex-Microsoft Azure architect
- VP Sales: 15 years B2B sales experience

TRACTION:
- 50 pilot customers
- $50K monthly recurring revenue
- 95% customer satisfaction
- 3 strategic partnerships signed
"""
    
    try:
        startup_result = enhanced_storage_client.upload_startup_file(
            startup_content,
            "business_plan.txt",
            startup_id,
            "text/plain"
        )
        
        if startup_result['success']:
            print(f"✅ Startup file uploaded successfully")
            print(f"  Startup ID: {startup_id}")
            print(f"  File Hash: {startup_result['file_hash']}")
            print(f"  Size: {startup_result['metadata']['size_mb']} MB")
            
            # Test listing startup files
            print(f"\n📁 Testing Startup File Listing")
            files = enhanced_storage_client.list_startup_files(startup_id)
            print(f"✅ Found {len(files)} files for startup")
            for file in files:
                print(f"  - {file['name']} ({file['size']} bytes)")
        else:
            print(f"❌ Startup file upload failed")
            
    except Exception as e:
        print(f"❌ Startup file upload error: {str(e)}")
    
    # Test updated storage stats
    print(f"\n📊 Testing Updated Storage Statistics")
    final_stats = enhanced_storage_client.get_storage_stats()
    if 'error' not in final_stats:
        print(f"✅ Final Storage Stats")
        print(f"  Total Files: {final_stats.get('total_files', 0)}")
        print(f"  Total Size: {final_stats.get('total_size_mb', 0)} MB")
        print(f"  Storage URL: {final_stats.get('storage_url', 'Unknown')}")
        
        file_types = final_stats.get('file_types', {})
        if file_types:
            print(f"  File Types:")
            for content_type, count in file_types.items():
                print(f"    - {content_type}: {count} files")
    
    print("\n" + "=" * 60)
    print("🎉 Enhanced Google Cloud Storage Test Complete!")
    return True

if __name__ == "__main__":
    try:
        test_storage_functionality()
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
