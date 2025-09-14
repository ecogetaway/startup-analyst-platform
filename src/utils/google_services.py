"""
Comprehensive Google Services Integration
"""
import os
import json
import time
from typing import Dict, Any, Optional, List
import logging

# Google Cloud imports
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False

try:
    import firebase_admin
    from firebase_admin import credentials, firestore, auth
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

try:
    from google.cloud import storage
    STORAGE_AVAILABLE = True
except ImportError:
    STORAGE_AVAILABLE = False

import google.generativeai as genai

logger = logging.getLogger(__name__)

class GoogleServicesManager:
    """Manages all Google Cloud services integration"""
    
    def __init__(self):
        """Initialize all Google services"""
        self.vertex_ai_initialized = False
        self.firebase_initialized = False
        self.storage_initialized = False
        self.gemini_initialized = False
        
        # Initialize services
        self._init_gemini()
        self._init_vertex_ai()
        self._init_firebase()
        self._init_storage()
    
    def _init_gemini(self):
        """Initialize Google Generative AI (Gemini)"""
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                self.gemini_initialized = True
                logger.info("✅ Google Generative AI (Gemini) initialized")
            else:
                logger.warning("⚠️ Google API key not found")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini: {str(e)}")
    
    def _init_vertex_ai(self):
        """Initialize Vertex AI"""
        try:
            if not VERTEX_AI_AVAILABLE:
                logger.warning("⚠️ Vertex AI not available - install google-cloud-aiplatform")
                return
            
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "startup-analyst-platform")
            
            # Try to initialize with service account
            service_account_path = "service-account-key.json"
            if os.path.exists(service_account_path):
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path
            
            vertexai.init(
                project=project_id,
                location="us-central1"
            )
            
            self.vertex_ai_model = GenerativeModel("gemini-1.5-pro")
            self.vertex_ai_initialized = True
            logger.info("✅ Vertex AI initialized")
            
        except Exception as e:
            logger.warning(f"⚠️ Vertex AI initialization failed: {str(e)}")
    
    def _init_firebase(self):
        """Initialize Firebase"""
        try:
            if not FIREBASE_AVAILABLE:
                logger.warning("⚠️ Firebase not available - install firebase-admin")
                return
            
            # Initialize Firebase Admin SDK
            if not firebase_admin._apps:
                service_account_path = "service-account-key.json"
                if os.path.exists(service_account_path):
                    cred = credentials.Certificate(service_account_path)
                    firebase_admin.initialize_app(cred)
                else:
                    # Try default credentials
                    cred = credentials.ApplicationDefault()
                    firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            self.firebase_initialized = True
            logger.info("✅ Firebase initialized")
            
        except Exception as e:
            logger.warning(f"⚠️ Firebase initialization failed: {str(e)}")
    
    def _init_storage(self):
        """Initialize Google Cloud Storage"""
        try:
            if not STORAGE_AVAILABLE:
                logger.warning("⚠️ Cloud Storage not available - install google-cloud-storage")
                return
            
            self.storage_client = storage.Client()
            self.bucket_name = f"{os.getenv('GOOGLE_CLOUD_PROJECT', 'startup-analyst-platform')}-startup-analyst-data"
            
            # Try to get or create bucket
            try:
                self.bucket = self.storage_client.bucket(self.bucket_name)
                self.bucket.reload()
            except:
                # Create bucket if it doesn't exist
                self.bucket = self.storage_client.create_bucket(self.bucket_name)
            
            self.storage_initialized = True
            logger.info("✅ Google Cloud Storage initialized")
            
        except Exception as e:
            logger.warning(f"⚠️ Cloud Storage initialization failed: {str(e)}")
    
    def get_status(self) -> Dict[str, bool]:
        """Get status of all Google services"""
        return {
            "gemini": self.gemini_initialized,
            "vertex_ai": self.vertex_ai_initialized,
            "firebase": self.firebase_initialized,
            "storage": self.storage_initialized
        }
    
    def analyze_with_gemini(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Analyze using Google Generative AI (Gemini)"""
        if not self.gemini_initialized:
            raise Exception("Gemini not initialized")
        
        try:
            if system_instruction:
                response = self.gemini_model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=8192,
                        temperature=0.7
                    ),
                    system_instruction=system_instruction
                )
            else:
                response = self.gemini_model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=8192,
                        temperature=0.7
                    )
                )
            
            return response.text if response.text else "No response generated"
            
        except Exception as e:
            logger.error(f"Gemini analysis failed: {str(e)}")
            raise Exception(f"Gemini analysis failed: {str(e)}")
    
    def analyze_with_vertex_ai(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Analyze using Vertex AI"""
        if not self.vertex_ai_initialized:
            raise Exception("Vertex AI not initialized")
        
        try:
            generation_config = {
                "max_output_tokens": 8192,
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40
            }
            
            if system_instruction:
                response = self.vertex_ai_model.generate_content(
                    prompt,
                    generation_config=generation_config,
                    system_instruction=system_instruction
                )
            else:
                response = self.vertex_ai_model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
            
            return response.text if response.text else "No response generated"
            
        except Exception as e:
            logger.error(f"Vertex AI analysis failed: {str(e)}")
            raise Exception(f"Vertex AI analysis failed: {str(e)}")
    
    def store_analysis_result(self, startup_id: str, analysis_data: Dict[str, Any], user_id: Optional[str] = None) -> bool:
        """Store analysis result in Firebase"""
        if not self.firebase_initialized:
            logger.warning("Firebase not available, skipping storage")
            return False
        
        try:
            doc_data = {
                "startup_id": startup_id,
                "analysis_data": analysis_data,
                "user_id": user_id,
                "timestamp": time.time(),
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            doc_ref = self.db.collection('startup_analyses').document(startup_id)
            doc_ref.set(doc_data)
            
            logger.info(f"Analysis result stored for startup: {startup_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store analysis result: {str(e)}")
            return False
    
    def get_analysis_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get analysis history from Firebase"""
        if not self.firebase_initialized:
            logger.warning("Firebase not available, returning empty history")
            return []
        
        try:
            analyses = self.db.collection('startup_analyses').where('user_id', '==', user_id).stream()
            return [doc.to_dict() for doc in analyses]
        except Exception as e:
            logger.error(f"Failed to get analysis history: {str(e)}")
            return []
    
    def upload_file(self, file_data: bytes, filename: str) -> str:
        """Upload file to Google Cloud Storage"""
        if not self.storage_initialized:
            raise Exception("Cloud Storage not initialized")
        
        try:
            blob = self.bucket.blob(filename)
            blob.upload_from_string(file_data)
            return blob.public_url
        except Exception as e:
            logger.error(f"File upload failed: {str(e)}")
            raise Exception(f"File upload failed: {str(e)}")
    
    def update_analysis_progress(self, startup_id: str, progress: Dict[str, Any]) -> bool:
        """Update analysis progress in Firebase"""
        if not self.firebase_initialized:
            logger.warning("Firebase not available, skipping progress update")
            return False
        
        try:
            doc_data = {
                "startup_id": startup_id,
                "progress": progress,
                "updated_at": time.time()
            }
            
            doc_ref = self.db.collection('analysis_progress').document(startup_id)
            doc_ref.set(doc_data)
            
            return True
        except Exception as e:
            logger.error(f"Failed to update analysis progress: {str(e)}")
            return False

# Global instance
google_services = GoogleServicesManager()
