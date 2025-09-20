#!/usr/bin/env python3
"""
Production PDF Financial Data Extractor
Combines Smart Report Analyzer with financial metrics extraction for startup analysis
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
import pandas as pd
import numpy as np
from datetime import datetime
import json

# PDF Processing
import pdfplumber
import PyPDF2

# AI/ML for text analysis
from transformers import pipeline
import torch

# Smart Report Analyzer integration
try:
    from src.utils.file_handler import load_file
    from src.utils.llm_agent import summarize_report, ask_question
    SMART_ANALYZER_AVAILABLE = True
except ImportError:
    SMART_ANALYZER_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ExtractedFinancialData:
    """Structured financial data extracted from PDFs"""
    # Revenue Data
    current_revenue: Optional[float] = None
    projected_revenue_y1: Optional[float] = None
    projected_revenue_y2: Optional[float] = None
    projected_revenue_y3: Optional[float] = None
    revenue_growth_rate: Optional[float] = None
    
    # Funding Data
    funding_requested: Optional[float] = None
    funding_to_date: Optional[float] = None
    valuation: Optional[float] = None
    use_of_funds: List[str] = None
    
    # Financial Metrics
    gross_margin: Optional[float] = None
    burn_rate: Optional[float] = None
    runway_months: Optional[float] = None
    cac: Optional[float] = None  # Customer Acquisition Cost
    ltv: Optional[float] = None  # Lifetime Value
    
    # Market Data
    market_size_tam: Optional[float] = None
    market_size_sam: Optional[float] = None
    market_size_som: Optional[float] = None
    market_growth_rate: Optional[float] = None
    
    # Business Metrics
    team_size: Optional[int] = None
    customers: Optional[int] = None
    retention_rate: Optional[float] = None
    
    # Text Analysis Results
    business_model: Optional[str] = None
    competitive_advantages: List[str] = None
    key_risks: List[str] = None
    
    # Confidence Scores
    extraction_confidence: float = 0.0
    completeness_score: float = 0.0
    
    def __post_init__(self):
        if self.use_of_funds is None:
            self.use_of_funds = []
        if self.competitive_advantages is None:
            self.competitive_advantages = []
        if self.key_risks is None:
            self.key_risks = []

class ProductionPDFExtractor:
    """
    Production-ready PDF financial data extractor
    Integrates Smart Report Analyzer for advanced document processing
    """
    
    def __init__(self):
        self.financial_patterns = self._initialize_patterns()
        self.qa_pipeline = None
        self.summarizer = None
        self._initialize_ai_models()
        
    def _initialize_patterns(self) -> Dict[str, List[str]]:
        """Initialize regex patterns for financial data extraction"""
        return {
            'revenue': [
                r'revenue.*?(\$?[\d,]+\.?\d*[KMB]?)',
                r'sales.*?(\$?[\d,]+\.?\d*[KMB]?)',
                r'income.*?(\$?[\d,]+\.?\d*[KMB]?)',
                r'(\$?[\d,]+\.?\d*[KMB]?)\s*revenue',
                r'annual\s+revenue.*?(\$?[\d,]+\.?\d*[KMB]?)'
            ],
            'funding': [
                r'raising.*?(\$?[\d,]+\.?\d*[KMB]?)',
                r'funding.*?(\$?[\d,]+\.?\d*[KMB]?)',
                r'investment.*?(\$?[\d,]+\.?\d*[KMB]?)',
                r'(\$?[\d,]+\.?\d*[KMB]?)\s*raise',
                r'seeking.*?(\$?[\d,]+\.?\d*[KMB]?)'
            ],
            'valuation': [
                r'valuation.*?(\$?[\d,]+\.?\d*[KMB]?)',
                r'valued\s+at.*?(\$?[\d,]+\.?\d*[KMB]?)',
                r'worth.*?(\$?[\d,]+\.?\d*[KMB]?)',
                r'(\$?[\d,]+\.?\d*[KMB]?)\s*valuation'
            ],
            'market_size': [
                r'market\s+size.*?(\$?[\d,]+\.?\d*[KMB]?)',
                r'TAM.*?(\$?[\d,]+\.?\d*[KMB]?)',
                r'SAM.*?(\$?[\d,]+\.?\d*[KMB]?)',
                r'SOM.*?(\$?[\d,]+\.?\d*[KMB]?)',
                r'total\s+addressable\s+market.*?(\$?[\d,]+\.?\d*[KMB]?)'
            ],
            'customers': [
                r'(\d+[,\d]*)\s*customers',
                r'(\d+[,\d]*)\s*users',
                r'(\d+[,\d]*)\s*clients',
                r'user\s+base.*?(\d+[,\d]*)'
            ],
            'team_size': [
                r'team.*?(\d+)\s*people',
                r'(\d+)\s*employees',
                r'(\d+)\s*team\s+members',
                r'founded\s+by.*?(\d+)'
            ],
            'growth_rate': [
                r'(\d+\.?\d*)%\s*growth',
                r'growing.*?(\d+\.?\d*)%',
                r'(\d+\.?\d*)%\s*increase',
                r'growth\s+rate.*?(\d+\.?\d*)%'
            ]
        }
    
    def _initialize_ai_models(self):
        """Initialize AI models for text analysis"""
        try:
            # Initialize Q&A pipeline for financial questions
            self.qa_pipeline = pipeline(
                "text2text-generation",
                model="google/flan-t5-small",
                device=-1
            )
            
            # Initialize summarizer
            self.summarizer = pipeline(
                "summarization",
                model="knkarthick/MEETING_SUMMARY",
                device=-1
            )
            
            logger.info("✅ AI models initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize AI models: {e}")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF using multiple methods"""
        text_content = ""
        
        # Method 1: PDFplumber (better for structured content)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"
            logger.info(f"✅ Extracted {len(text_content)} characters using PDFplumber")
        except Exception as e:
            logger.warning(f"PDFplumber extraction failed: {e}")
        
        # Method 2: PyPDF2 (fallback)
        if not text_content:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text_content += page.extract_text() + "\n"
                logger.info(f"✅ Extracted {len(text_content)} characters using PyPDF2")
            except Exception as e:
                logger.error(f"PyPDF2 extraction failed: {e}")
        
        return text_content
    
    def parse_financial_value(self, value_str: str) -> Optional[float]:
        """Parse financial values with K/M/B suffixes"""
        if not value_str:
            return None
        
        # Clean the string
        value_str = value_str.replace('$', '').replace(',', '').strip()
        
        # Handle K/M/B suffixes
        multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
        
        for suffix, multiplier in multipliers.items():
            if value_str.upper().endswith(suffix):
                try:
                    number = float(value_str[:-1])
                    return number * multiplier
                except ValueError:
                    continue
        
        # Try to parse as regular number
        try:
            return float(value_str)
        except ValueError:
            return None
    
    def extract_financial_metrics(self, text: str) -> Dict[str, Any]:
        """Extract financial metrics using regex patterns"""
        metrics = {}
        
        for metric_type, patterns in self.financial_patterns.items():
            values = []
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    parsed_value = self.parse_financial_value(match)
                    if parsed_value:
                        values.append(parsed_value)
            
            if values:
                # Take median value to handle outliers
                metrics[metric_type] = np.median(values)
                logger.debug(f"Found {metric_type}: {metrics[metric_type]}")
        
        return metrics
    
    def extract_tables_from_pdf(self, pdf_path: str) -> List[pd.DataFrame]:
        """Extract tables from PDF for financial analysis"""
        tables = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()
                    for table in page_tables:
                        if table and len(table) > 1:  # At least header + 1 row
                            df = pd.DataFrame(table[1:], columns=table[0])
                            df['source_page'] = page_num + 1
                            tables.append(df)
                            
            logger.info(f"✅ Extracted {len(tables)} tables from PDF")
        except Exception as e:
            logger.warning(f"Table extraction failed: {e}")
        
        return tables
    
    def analyze_financial_tables(self, tables: List[pd.DataFrame]) -> Dict[str, Any]:
        """Analyze extracted tables for financial data"""
        financial_data = {}
        
        for table in tables:
            # Look for revenue projections
            if any('revenue' in str(col).lower() for col in table.columns):
                revenue_cols = [col for col in table.columns if 'revenue' in str(col).lower()]
                for col in revenue_cols:
                    try:
                        # Extract numeric values
                        numeric_values = pd.to_numeric(table[col].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
                        valid_values = numeric_values.dropna()
                        if not valid_values.empty:
                            financial_data['table_revenue'] = valid_values.tolist()
                    except Exception:
                        continue
            
            # Look for financial metrics
            financial_keywords = ['margin', 'cost', 'profit', 'expense', 'cash', 'burn']
            for keyword in financial_keywords:
                matching_cols = [col for col in table.columns if keyword in str(col).lower()]
                for col in matching_cols:
                    try:
                        numeric_values = pd.to_numeric(table[col].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
                        valid_values = numeric_values.dropna()
                        if not valid_values.empty:
                            financial_data[f'table_{keyword}'] = valid_values.tolist()
                    except Exception:
                        continue
        
        return financial_data
    
    def ai_financial_analysis(self, text: str) -> Dict[str, Any]:
        """Use AI models for advanced financial analysis"""
        ai_results = {}
        
        if not self.qa_pipeline:
            return ai_results
        
        # Define financial questions
        financial_questions = [
            "What is the current annual revenue?",
            "How much funding is the company seeking?",
            "What is the market size?",
            "What are the main revenue streams?",
            "What is the business model?",
            "What are the key risks?",
            "How many customers does the company have?"
        ]
        
        # Truncate text to manageable size
        max_text_length = 2000
        text_chunk = text[:max_text_length]
        
        for question in financial_questions:
            try:
                prompt = f"Context: {text_chunk}\n\nQuestion: {question}\nAnswer:"
                response = self.qa_pipeline(prompt, max_length=50, num_return_sequences=1)
                answer = response[0]['generated_text'].replace(prompt, '').strip()
                
                # Store non-empty answers
                if answer and len(answer) > 3:
                    key = question.lower().replace('what is the ', '').replace('how much ', '').replace('how many ', '').replace('?', '').replace(' ', '_')
                    ai_results[key] = answer
                    
            except Exception as e:
                logger.debug(f"AI question failed: {question} - {e}")
                continue
        
        return ai_results
    
    def smart_analyzer_integration(self, pdf_path: str) -> Dict[str, Any]:
        """Integrate with Smart Report Analyzer for enhanced analysis"""
        smart_results = {}
        
        if not SMART_ANALYZER_AVAILABLE:
            logger.warning("Smart Report Analyzer not available")
            return smart_results
        
        try:
            # Load file using Smart Analyzer
            data = load_file(pdf_path)
            
            if data is not None:
                # Generate summary
                summary = summarize_report(data)
                smart_results['summary'] = summary
                
                # Ask specific questions
                financial_questions = [
                    "What is the business model?",
                    "What are the revenue projections?",
                    "What funding is needed?",
                    "What are the main risks?",
                    "What is the market opportunity?"
                ]
                
                for question in financial_questions:
                    try:
                        answer = ask_question(data, question)
                        if answer:
                            key = question.lower().replace('what is the ', '').replace('what are the ', '').replace('what ', '').replace('?', '').replace(' ', '_')
                            smart_results[key] = answer
                    except Exception as e:
                        logger.debug(f"Smart analyzer question failed: {question} - {e}")
                
                logger.info("✅ Smart Report Analyzer integration successful")
            
        except Exception as e:
            logger.warning(f"Smart Report Analyzer integration failed: {e}")
        
        return smart_results
    
    def calculate_confidence_scores(self, extracted_data: ExtractedFinancialData) -> Tuple[float, float]:
        """Calculate extraction confidence and completeness scores"""
        
        # Key financial fields for completeness check
        key_fields = [
            'current_revenue', 'projected_revenue_y1', 'funding_requested',
            'market_size_tam', 'team_size', 'business_model'
        ]
        
        # Count non-None fields
        completed_fields = sum(1 for field in key_fields if getattr(extracted_data, field) is not None)
        completeness_score = completed_fields / len(key_fields)
        
        # Calculate extraction confidence based on data quality
        confidence_factors = []
        
        # Revenue data confidence
        if extracted_data.current_revenue is not None:
            confidence_factors.append(0.9)
        
        # Market size confidence
        if extracted_data.market_size_tam is not None:
            confidence_factors.append(0.8)
        
        # Funding data confidence
        if extracted_data.funding_requested is not None:
            confidence_factors.append(0.85)
        
        # Business model confidence
        if extracted_data.business_model:
            confidence_factors.append(0.7)
        
        extraction_confidence = np.mean(confidence_factors) if confidence_factors else 0.3
        
        return extraction_confidence, completeness_score
    
    def extract_financial_data(self, pdf_path: str) -> ExtractedFinancialData:
        """
        Main function to extract comprehensive financial data from PDF
        """
        logger.info(f"🚀 Starting financial data extraction from {pdf_path}")
        
        # Extract text content
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            logger.error("No text content extracted from PDF")
            return ExtractedFinancialData()
        
        # Extract tables
        tables = self.extract_tables_from_pdf(pdf_path)
        
        # Pattern-based extraction
        regex_metrics = self.extract_financial_metrics(text)
        
        # Table-based extraction
        table_metrics = self.analyze_financial_tables(tables)
        
        # AI-based extraction
        ai_metrics = self.ai_financial_analysis(text)
        
        # Smart Analyzer integration
        smart_metrics = self.smart_analyzer_integration(pdf_path)
        
        # Combine all extraction methods
        extracted_data = ExtractedFinancialData()
        
        # Revenue data
        extracted_data.current_revenue = (
            regex_metrics.get('revenue') or 
            self._extract_from_table_data(table_metrics, 'revenue') or
            self._parse_ai_financial_value(ai_metrics.get('current_annual_revenue'))
        )
        
        # Funding data
        extracted_data.funding_requested = (
            regex_metrics.get('funding') or
            self._parse_ai_financial_value(ai_metrics.get('funding_is_the_company_seeking'))
        )
        
        # Valuation
        extracted_data.valuation = regex_metrics.get('valuation')
        
        # Market size
        extracted_data.market_size_tam = (
            regex_metrics.get('market_size') or
            self._parse_ai_financial_value(ai_metrics.get('market_size'))
        )
        
        # Team and customers
        extracted_data.team_size = int(regex_metrics.get('team_size', 0)) if regex_metrics.get('team_size') else None
        extracted_data.customers = int(regex_metrics.get('customers', 0)) if regex_metrics.get('customers') else None
        
        # Growth rate
        if regex_metrics.get('growth_rate'):
            extracted_data.revenue_growth_rate = regex_metrics['growth_rate'] / 100  # Convert to decimal
        
        # Business model and qualitative data
        extracted_data.business_model = (
            smart_metrics.get('business_model') or 
            ai_metrics.get('business_model') or
            self._extract_business_model_from_text(text)
        )
        
        # Calculate derived metrics
        if extracted_data.current_revenue and extracted_data.revenue_growth_rate:
            extracted_data.projected_revenue_y1 = extracted_data.current_revenue * (1 + extracted_data.revenue_growth_rate)
            extracted_data.projected_revenue_y3 = extracted_data.current_revenue * ((1 + extracted_data.revenue_growth_rate) ** 3)
        
        # Calculate confidence scores
        confidence, completeness = self.calculate_confidence_scores(extracted_data)
        extracted_data.extraction_confidence = confidence
        extracted_data.completeness_score = completeness
        
        logger.info(f"✅ Financial data extraction completed")
        logger.info(f"📊 Completeness: {completeness:.1%}, Confidence: {confidence:.1%}")
        
        return extracted_data
    
    def _extract_from_table_data(self, table_data: Dict, key: str) -> Optional[float]:
        """Extract values from table analysis results"""
        table_key = f'table_{key}'
        if table_key in table_data and table_data[table_key]:
            values = table_data[table_key]
            return np.median(values) if values else None
        return None
    
    def _parse_ai_financial_value(self, ai_response: str) -> Optional[float]:
        """Parse financial values from AI responses"""
        if not ai_response:
            return None
        
        # Look for monetary values in AI response
        money_pattern = r'\$?[\d,]+\.?\d*[KMB]?'
        matches = re.findall(money_pattern, ai_response)
        
        for match in matches:
            parsed = self.parse_financial_value(match)
            if parsed:
                return parsed
        
        return None
    
    def _extract_business_model_from_text(self, text: str) -> Optional[str]:
        """Extract business model description from text"""
        business_model_patterns = [
            r'business\s+model[:\s]+([^.]{10,100})',
            r'revenue\s+model[:\s]+([^.]{10,100})',
            r'how\s+we\s+make\s+money[:\s]+([^.]{10,100})'
        ]
        
        for pattern in business_model_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        return None

# Global extractor instance
_global_extractor = None

def get_pdf_extractor() -> ProductionPDFExtractor:
    """Get or create global PDF extractor instance"""
    global _global_extractor
    if _global_extractor is None:
        _global_extractor = ProductionPDFExtractor()
    return _global_extractor

def extract_financial_data_from_pdf(pdf_path: str) -> ExtractedFinancialData:
    """
    Main function for extracting financial data from PDF files
    """
    extractor = get_pdf_extractor()
    return extractor.extract_financial_data(pdf_path)

if __name__ == "__main__":
    # Test the PDF extractor
    import sys
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        print(f"🚀 Testing PDF extraction on: {pdf_path}")
        
        extractor = ProductionPDFExtractor()
        result = extractor.extract_financial_data(pdf_path)
        
        print(f"\n📊 Extraction Results:")
        print(f"  Current Revenue: ${result.current_revenue:,.0f}" if result.current_revenue else "  Current Revenue: Not found")
        print(f"  Funding Requested: ${result.funding_requested:,.0f}" if result.funding_requested else "  Funding Requested: Not found")
        print(f"  Market Size (TAM): ${result.market_size_tam:,.0f}" if result.market_size_tam else "  Market Size: Not found")
        print(f"  Team Size: {result.team_size}" if result.team_size else "  Team Size: Not found")
        print(f"  Business Model: {result.business_model}" if result.business_model else "  Business Model: Not found")
        print(f"  Confidence: {result.extraction_confidence:.1%}")
        print(f"  Completeness: {result.completeness_score:.1%}")
    else:
        print("Usage: python pdf_financial_extractor.py <path_to_pdf>")
