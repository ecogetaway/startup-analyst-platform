#!/usr/bin/env python3
"""
Fix PDF processing to extract content and pass to AI agents
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

# Add PDF processing capability
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    try:
        import pdfplumber
        PDF_AVAILABLE = True
    except ImportError:
        PDF_AVAILABLE = False

def extract_pdf_text(pdf_path):
    """Extract text from PDF file"""
    
    if not PDF_AVAILABLE:
        return "PDF processing not available. Please install PyPDF2 or pdfplumber."
    
    try:
        # Try pdfplumber first (better for complex PDFs)
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
        except:
            pass
        
        # Fallback to PyPDF2
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except:
            pass
        
        return "Could not extract text from PDF"
        
    except Exception as e:
        return f"Error extracting PDF text: {str(e)}"

def test_pdf_extraction():
    """Test PDF extraction on existing files"""
    
    print("🧪 Testing PDF Text Extraction")
    print("=" * 40)
    
    # Test with Sia pitch deck
    sia_pdf = "training_data/pitch_decks/Sia - DSA-Pitch deck_V1-INR.pdf"
    
    if os.path.exists(sia_pdf):
        print(f"📄 Testing: {sia_pdf}")
        text = extract_pdf_text(sia_pdf)
        
        if text and len(text) > 100:
            print(f"✅ Successfully extracted {len(text)} characters")
            print(f"📝 Preview: {text[:200]}...")
            return True
        else:
            print(f"❌ Extraction failed or too short: {len(text) if text else 0} characters")
            return False
    else:
        print(f"❌ PDF not found: {sia_pdf}")
        return False

def main():
    """Test and fix PDF processing"""
    
    print("🔧 PDF Processing Fix")
    print("=" * 30)
    
    if not PDF_AVAILABLE:
        print("❌ PDF processing libraries not available")
        print("💡 Install with: pip install PyPDF2 pdfplumber")
        return False
    
    success = test_pdf_extraction()
    
    if success:
        print("\n✅ PDF processing is working!")
        print("🎯 Ready to integrate with AI agents")
    else:
        print("\n❌ PDF processing needs fixing")
    
    return success

if __name__ == "__main__":
    main()
