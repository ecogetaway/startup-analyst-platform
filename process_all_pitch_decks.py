#!/usr/bin/env python3
"""
Batch process all pitch decks for hackathon demo
"""

import sys
import os
import json
import time
from datetime import datetime

sys.path.append('.')
sys.path.append('src')

from working_backend import app
from fastapi.testclient import TestClient

def process_pitch_deck(client, company_name, industry, stage, description, pitch_deck_path):
    """Process a single pitch deck"""
    
    print(f"\n🚀 Processing {company_name}...")
    print("=" * 50)
    
    startup_input = {
        "company_name": company_name,
        "business_description": description,
        "industry": industry,
        "stage": stage,
        "founder_name": f"{company_name} Team",
        "founder_background": "Experienced entrepreneurs and industry experts",
        "website": f"https://{company_name.lower().replace(' ', '').replace('.', '')}.com",
        "additional_info": f"Pitch deck analysis for {company_name}",
        "uploaded_files": [
            {
                "name": os.path.basename(pitch_deck_path),
                "url": pitch_deck_path,
                "size": os.path.getsize(pitch_deck_path),
                "type": "document"
            }
        ]
    }
    
    try:
        response = client.post("/api/analyze", json=startup_input)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {company_name} analysis completed!")
            
            # Save results
            filename = f"{company_name.lower().replace(' ', '_').replace('.', '')}_analysis.json"
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"💾 Results saved to: {filename}")
            
            return result
        else:
            print(f"❌ {company_name} analysis failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error processing {company_name}: {str(e)}")
        return None

def main():
    """Process all pitch decks"""
    
    print("🎯 Starting Batch Pitch Deck Analysis")
    print("=" * 60)
    
    # Create test client
    client = TestClient(app)
    
    # Define pitch decks to process
    pitch_decks = [
        {
            "name": "Sia",
            "industry": "Data Science & Analytics",
            "stage": "Seed",
            "description": "Data Science and Analytics platform for businesses",
            "path": "training_data/pitch_decks/Sia - DSA-Pitch deck_V1-INR.pdf"
        },
        {
            "name": "Ctruh",
            "industry": "XR/VR Technology",
            "stage": "Series A",
            "description": "XR Commerce Studio - Virtual reality commerce platform",
            "path": "training_data/pitch_decks/Pitch Deck-Ctruh-XR-Commerce-Studio.pdf"
        },
        {
            "name": "Dr. Doodley",
            "industry": "Healthcare Technology",
            "stage": "Seed",
            "description": "AI-powered healthcare platform for patient care",
            "path": "training_data/pitch_decks/Dr. Doodley Investor Deck Aug 2025.pdf"
        },
        {
            "name": "Ziniosa",
            "industry": "Consumer Technology",
            "stage": "Pre-Seed",
            "description": "Consumer technology platform for lifestyle enhancement",
            "path": "training_data/pitch_decks/Ziniosa Pitch Deck.pdf"
        },
        {
            "name": "Hexafun",
            "industry": "Gaming & Entertainment",
            "stage": "Seed",
            "description": "Gaming and entertainment platform for user engagement",
            "path": "training_data/pitch_decks/01. Hexafun Detailed Pitch Deck.pdf"
        },
        {
            "name": "Naario",
            "industry": "Technology",
            "stage": "Series A",
            "description": "Technology platform for business solutions",
            "path": "training_data/pitch_decks/NaarioDeck2025.pdf"
        }
    ]
    
    results = {}
    
    # Process each pitch deck
    for deck in pitch_decks:
        if os.path.exists(deck["path"]):
            result = process_pitch_deck(
                client, 
                deck["name"], 
                deck["industry"], 
                deck["stage"], 
                deck["description"], 
                deck["path"]
            )
            if result:
                results[deck["name"]] = result
        else:
            print(f"⚠️ File not found: {deck['path']}")
    
    # Create summary report
    print("\n📊 ANALYSIS SUMMARY")
    print("=" * 60)
    
    summary = {
        "total_analyzed": len(results),
        "timestamp": datetime.now().isoformat(),
        "companies": {}
    }
    
    for company, result in results.items():
        if 'results' in result:
            res = result['results']
            summary["companies"][company] = {
                "recommendation": res.get('recommendation', 'N/A'),
                "confidence": res.get('confidence_score', 0),
                "ml_success_probability": res.get('ml_prediction', {}).get('success_probability', 0),
                "ml_prediction": res.get('ml_prediction', {}).get('prediction', 'N/A')
            }
            
            print(f"🏢 {company}:")
            print(f"   Recommendation: {res.get('recommendation', 'N/A')}")
            print(f"   Confidence: {res.get('confidence_score', 0):.1%}")
            if 'ml_prediction' in res:
                ml = res['ml_prediction']
                print(f"   ML Success: {ml.get('success_probability', 0):.1%}")
                print(f"   ML Prediction: {ml.get('prediction', 'N/A')}")
            print()
    
    # Save summary
    with open('hackathon_demo_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"💾 Summary saved to: hackathon_demo_summary.json")
    print(f"🎉 Batch analysis complete! {len(results)} companies analyzed.")

if __name__ == "__main__":
    main()
