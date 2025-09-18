#!/usr/bin/env python3
"""
Pitch Deck Processor for ML Training
Extracts structured data from PDF pitch decks to improve ML model accuracy
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import pandas as pd
import numpy as np

# PDF processing
try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ pdfplumber not available. Install with: pip install pdfplumber")

# AI processing
try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️ Google AI not available")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ExtractedStartupData:
    """Structured data extracted from pitch deck"""
    company_name: str
    industry: str
    stage: str
    team_size: int
    funding_total: float
    funding_rounds: int
    revenue: float
    growth_rate: float
    burn_rate: float
    market_size: float
    competition_level: int  # 1-5 scale
    product_readiness: int  # 1-5 scale
    team_experience: int    # 1-5 scale
    business_model: str
    location: str
    founded_year: int
    success_outcome: str    # "Success", "Failure", "Unknown"
    confidence_score: float # 0-1

class PitchDeckProcessor:
    """
    Processes PDF pitch decks to extract structured data for ML training
    """
    
    def __init__(self):
        self.ai_model = None
        if AI_AVAILABLE:
            try:
                genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
                self.ai_model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("✅ AI model initialized for pitch deck processing")
            except Exception as e:
                logger.warning(f"⚠️ AI model initialization failed: {e}")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        if not PDF_AVAILABLE:
            raise ImportError("pdfplumber not available")
        
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            logger.info(f"✅ Extracted {len(text)} characters from {pdf_path}")
            return text
        except Exception as e:
            logger.error(f"❌ Failed to extract text from {pdf_path}: {e}")
            raise
    
    def extract_data_with_ai(self, text: str, company_name: str = "Unknown") -> ExtractedStartupData:
        """Use AI to extract structured data from pitch deck text"""
        if not self.ai_model:
            raise RuntimeError("AI model not available")
        
        prompt = f"""
        Analyze this startup pitch deck text and extract structured data. Return ONLY a JSON object with the following fields:

        {{
            "company_name": "string",
            "industry": "string (e.g., Technology, Healthcare, Finance)",
            "stage": "string (Pre-Seed, Seed, Series A, Series B, Series C+)",
            "team_size": number,
            "funding_total": number (total funding raised in USD),
            "funding_rounds": number,
            "revenue": number (annual revenue in USD, 0 if pre-revenue),
            "growth_rate": number (monthly growth rate percentage),
            "burn_rate": number (monthly burn rate in USD),
            "market_size": number (TAM in USD),
            "competition_level": number (1-5 scale, 5 being most competitive),
            "product_readiness": number (1-5 scale, 5 being production ready),
            "team_experience": number (1-5 scale, 5 being very experienced),
            "business_model": "string (B2B, B2C, B2B2C, Marketplace, etc.)",
            "location": "string (city, state/country)",
            "founded_year": number,
            "success_outcome": "string (Success, Failure, Unknown - based on known outcomes)",
            "confidence_score": number (0-1, how confident you are in the extraction)
        }}

        Pitch deck text:
        {text[:4000]}  # Limit to first 4000 characters

        Return ONLY the JSON object, no other text.
        """
        
        try:
            response = self.ai_model.generate_content(
                prompt,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
            )
            
            # Parse JSON response
            json_text = response.text.strip()
            if json_text.startswith('```json'):
                json_text = json_text[7:]
            if json_text.endswith('```'):
                json_text = json_text[:-3]
            
            data = json.loads(json_text)
            
            # Convert to dataclass
            return ExtractedStartupData(
                company_name=data.get('company_name', company_name),
                industry=data.get('industry', 'Technology'),
                stage=data.get('stage', 'Seed'),
                team_size=int(data.get('team_size', 5)),
                funding_total=float(data.get('funding_total', 0)),
                funding_rounds=int(data.get('funding_rounds', 0)),
                revenue=float(data.get('revenue', 0)),
                growth_rate=float(data.get('growth_rate', 0)),
                burn_rate=float(data.get('burn_rate', 0)),
                market_size=float(data.get('market_size', 0)),
                competition_level=int(data.get('competition_level', 3)),
                product_readiness=int(data.get('product_readiness', 3)),
                team_experience=int(data.get('team_experience', 3)),
                business_model=data.get('business_model', 'B2B'),
                location=data.get('location', 'Unknown'),
                founded_year=int(data.get('founded_year', 2020)),
                success_outcome=data.get('success_outcome', 'Unknown'),
                confidence_score=float(data.get('confidence_score', 0.5))
            )
            
        except Exception as e:
            logger.error(f"❌ AI extraction failed: {e}")
            # Return default data
            return ExtractedStartupData(
                company_name=company_name,
                industry='Technology',
                stage='Seed',
                team_size=5,
                funding_total=0,
                funding_rounds=0,
                revenue=0,
                growth_rate=0,
                burn_rate=0,
                market_size=0,
                competition_level=3,
                product_readiness=3,
                team_experience=3,
                business_model='B2B',
                location='Unknown',
                founded_year=2020,
                success_outcome='Unknown',
                confidence_score=0.0
            )
    
    def process_pitch_deck(self, pdf_path: str, company_name: str = None) -> ExtractedStartupData:
        """Process a single pitch deck PDF"""
        logger.info(f"🔄 Processing pitch deck: {pdf_path}")
        
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        
        # Extract data with AI
        extracted_data = self.extract_data_with_ai(text, company_name or "Unknown")
        
        logger.info(f"✅ Processed {extracted_data.company_name}: {extracted_data.success_outcome}")
        return extracted_data
    
    def process_directory(self, directory_path: str) -> List[ExtractedStartupData]:
        """Process all PDF files in a directory"""
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
        logger.info(f"📁 Found {len(pdf_files)} PDF files in {directory_path}")
        
        results = []
        for pdf_file in pdf_files:
            try:
                pdf_path = os.path.join(directory_path, pdf_file)
                company_name = os.path.splitext(pdf_file)[0]  # Use filename as company name
                extracted_data = self.process_pitch_deck(pdf_path, company_name)
                results.append(extracted_data)
            except Exception as e:
                logger.error(f"❌ Failed to process {pdf_file}: {e}")
                continue
        
        logger.info(f"✅ Successfully processed {len(results)} pitch decks")
        return results
    
    def save_training_data(self, extracted_data: List[ExtractedStartupData], output_path: str):
        """Save extracted data as training dataset"""
        # Convert to DataFrame
        data_dicts = [asdict(item) for item in extracted_data]
        df = pd.DataFrame(data_dicts)
        
        # Add success label for ML training
        df['is_success'] = df['success_outcome'].map({
            'Success': 1,
            'Failure': 0,
            'Unknown': 0  # Treat unknown as failure for conservative training
        })
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        logger.info(f"💾 Saved training data to {output_path}")
        
        # Print summary
        print(f"\n📊 Training Data Summary:")
        print(f"Total companies: {len(df)}")
        print(f"Success cases: {df['is_success'].sum()}")
        print(f"Failure cases: {len(df) - df['is_success'].sum()}")
        print(f"Success rate: {df['is_success'].mean():.1%}")
        
        return df

def create_training_directory():
    """Create directory structure for training data"""
    training_dir = "training_data"
    pitch_decks_dir = os.path.join(training_dir, "pitch_decks")
    
    os.makedirs(training_dir, exist_ok=True)
    os.makedirs(pitch_decks_dir, exist_ok=True)
    
    print(f"📁 Created training directories:")
    print(f"   - {training_dir}/")
    print(f"   - {pitch_decks_dir}/")
    print(f"\n📋 Instructions:")
    print(f"1. Place PDF pitch decks in: {pitch_decks_dir}/")
    print(f"2. Run: python -m src.ml.pitch_deck_processor")
    print(f"3. Training data will be saved to: {training_dir}/startup_training_data.csv")
    
    return training_dir, pitch_decks_dir

if __name__ == "__main__":
    # Create training directory structure
    training_dir, pitch_decks_dir = create_training_directory()
    
    # Check if pitch decks are available
    pdf_files = [f for f in os.listdir(pitch_decks_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"\n⚠️ No PDF files found in {pitch_decks_dir}")
        print("Please add PDF pitch decks to the directory and run again.")
    else:
        print(f"\n🚀 Processing {len(pdf_files)} pitch decks...")
        
        # Initialize processor
        processor = PitchDeckProcessor()
        
        # Process all pitch decks
        extracted_data = processor.process_directory(pitch_decks_dir)
        
        # Save training data
        output_path = os.path.join(training_dir, "startup_training_data.csv")
        df = processor.save_training_data(extracted_data, output_path)
        
        print(f"\n✅ Training data ready! Use this file to retrain the ML model.")
