"""
Configuration settings for the Startup Analyst Platform
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # Google Cloud Configuration
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "startup-analyst-platform")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Application Configuration
    APP_NAME = os.getenv("APP_NAME", "Startup Analyst Platform")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Google Cloud Services
    GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "startup-analyst-data")
    REGION = os.getenv("REGION", "us-central1")
    
    # AI Model Configuration
    GEMINI_MODEL = "gemini-1.5-flash"
    MAX_TOKENS = 8192
    TEMPERATURE = 0.7
    
    # Analysis Configuration
    ANALYSIS_TIMEOUT = 300  # 5 minutes
    MAX_CONCURRENT_ANALYSES = 5
    
    @classmethod
    def validate(cls):
        """Validate required settings"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        return True

# Create global settings instance
settings = Settings()
