# utils/file_handler.py
# 
# Based on Smart Report Analyzer by Sreeja Bethu
# Original: https://github.com/SreejaBethu/Smart-Report-Analyzer
# License: MIT License
# 
# Modifications:
# - Adapted for FastAPI file handling
# - Enhanced for startup pitch deck processing
# - Added additional file type support

import pandas as pd
import pdfplumber
import io

def load_file(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()
    
    if file_type in ["csv"]:
        df = pd.read_csv(uploaded_file)
        return df, None

    elif file_type in ["xlsx", "xls"]:
        df = pd.read_excel(uploaded_file)
        return df, None

    elif file_type == "pdf":
        raw_text = extract_text_from_pdf(uploaded_file)
        return None, raw_text

    else:
        return None, "Unsupported file type."


def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()
