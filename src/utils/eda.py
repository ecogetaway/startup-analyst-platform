# utils/eda.py
# 
# Based on Smart Report Analyzer by Sreeja Bethu
# Original: https://github.com/SreejaBethu/Smart-Report-Analyzer
# License: MIT License
# 
# Modifications:
# - Integrated into startup analysis workflow
# - Enhanced visualizations for investment analysis
# - Added financial metrics visualization

import pandas as pd
import plotly.express as px

def generate_eda_report(df: pd.DataFrame):
    figures = []

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns

    # Histogram for numeric columns
    for col in numeric_cols:
        fig = px.histogram(df, x=col, title=f"Distribution of {col}")
        figures.append(fig)

    # Bar charts for categorical columns (top 10)
    for col in categorical_cols:
        if df[col].nunique() <= 20:
            fig = px.bar(df[col].value_counts().head(10), title=f"Top Categories in {col}")
            figures.append(fig)

    return figures
