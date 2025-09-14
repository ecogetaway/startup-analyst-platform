"""
Firebase client for real-time data and user management
"""
import firebase_admin
from firebase_admin import credentials, firestore, auth
from typing import Dict, Any, Optional, List
import json
import time
import logging
from ..config.settings import settings

logger = logging.getLogger(__name__)

class FirebaseClient:
    """Firebase client for data storage and user management"""
    
    def __init__(self):
        """Initialize Firebase client"""
        try:
            # Initialize Firebase Admin SDK
            if not firebase_admin._apps:
                # Use default credentials (service account key)
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            self.auth = auth
            
            logger.info("Firebase client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {str(e)}")
            # For development, we'll continue without Firebase
            self.db = None
            self.auth = None
    
    def store_analysis_result(self, startup_id: str, analysis_data: Dict[str, Any], user_id: Optional[str] = None) -> bool:
        """Store analysis result in Firestore"""
        try:
            if not self.db:
                logger.warning("Firebase not available, skipping storage")
                return False
            
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
        """Get analysis history for a user"""
        try:
            if not self.db:
                logger.warning("Firebase not available, returning empty history")
                return []
            
            analyses = self.db.collection('startup_analyses').where('user_id', '==', user_id).stream()
            return [doc.to_dict() for doc in analyses]
            
        except Exception as e:
            logger.error(f"Failed to get analysis history: {str(e)}")
            return []
    
    def get_analysis_by_id(self, startup_id: str) -> Optional[Dict[str, Any]]:
        """Get specific analysis by startup ID"""
        try:
            if not self.db:
                logger.warning("Firebase not available, returning None")
                return None
            
            doc_ref = self.db.collection('startup_analyses').document(startup_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            else:
                return None
                
        except Exception as e:
            logger.error(f"Failed to get analysis by ID: {str(e)}")
            return None
    
    def store_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Store user preferences"""
        try:
            if not self.db:
                logger.warning("Firebase not available, skipping preferences storage")
                return False
            
            doc_data = {
                "user_id": user_id,
                "preferences": preferences,
                "updated_at": time.time()
            }
            
            doc_ref = self.db.collection('user_preferences').document(user_id)
            doc_ref.set(doc_data)
            
            logger.info(f"User preferences stored for user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store user preferences: {str(e)}")
            return False
    
    def get_user_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user preferences"""
        try:
            if not self.db:
                logger.warning("Firebase not available, returning None")
                return None
            
            doc_ref = self.db.collection('user_preferences').document(user_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            else:
                return None
                
        except Exception as e:
            logger.error(f"Failed to get user preferences: {str(e)}")
            return None
    
    def store_demo_scenario(self, scenario_data: Dict[str, Any]) -> bool:
        """Store demo scenario"""
        try:
            if not self.db:
                logger.warning("Firebase not available, skipping demo scenario storage")
                return False
            
            doc_data = {
                "scenario_data": scenario_data,
                "created_at": time.time(),
                "is_active": True
            }
            
            doc_ref = self.db.collection('demo_scenarios').document()
            doc_ref.set(doc_data)
            
            logger.info("Demo scenario stored successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store demo scenario: {str(e)}")
            return False
    
    def get_demo_scenarios(self) -> List[Dict[str, Any]]:
        """Get all demo scenarios"""
        try:
            if not self.db:
                logger.warning("Firebase not available, returning empty scenarios")
                return []
            
            scenarios = self.db.collection('demo_scenarios').where('is_active', '==', True).stream()
            return [doc.to_dict() for doc in scenarios]
            
        except Exception as e:
            logger.error(f"Failed to get demo scenarios: {str(e)}")
            return []
    
    def update_analysis_progress(self, startup_id: str, progress: Dict[str, Any]) -> bool:
        """Update analysis progress in real-time"""
        try:
            if not self.db:
                logger.warning("Firebase not available, skipping progress update")
                return False
            
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
