"""
Enhanced Firebase client with real-time collaboration and fixed authentication
"""
import firebase_admin
from firebase_admin import credentials, firestore, auth
from typing import Dict, Any, Optional, List, Callable
import json
import time
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class EnhancedFirebaseClient:
    """Enhanced Firebase client with real-time collaboration features"""
    
    def __init__(self):
        """Initialize Firebase client with proper authentication"""
        self.db = None
        self.auth = None
        self.initialized = False
        
        try:
            # Initialize Firebase Admin SDK with service account
            if not firebase_admin._apps:
                # Try to use service account key file
                service_account_paths = [
                    "service-account-key.json",
                    "service-account.json",
                    "../service-account-key.json",
                    "../service-account.json"
                ]
                
                cred = None
                for path in service_account_paths:
                    if os.path.exists(path):
                        logger.info(f"Using service account file: {path}")
                        cred = credentials.Certificate(path)
                        break
                
                if not cred:
                    # Fallback to application default credentials
                    logger.info("Using application default credentials")
                    cred = credentials.ApplicationDefault()
                
                # Initialize with database URL if available
                config = {
                    'databaseURL': f'https://startup-analyst-platform-default-rtdb.firebaseio.com/'
                }
                
                firebase_admin.initialize_app(cred, config)
            
            self.db = firestore.client()
            self.auth = auth
            self.initialized = True
            
            logger.info("✅ Enhanced Firebase client initialized successfully")
            
            # Test connection
            self._test_connection()
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Firebase: {str(e)}")
            logger.info("🔄 Continuing without Firebase for development")
            self.db = None
            self.auth = None
            self.initialized = False
    
    def _test_connection(self):
        """Test Firebase connection"""
        try:
            if self.db:
                # Try to read from a test collection
                test_ref = self.db.collection('connection_test').document('test')
                test_ref.set({
                    'timestamp': time.time(),
                    'status': 'connected'
                })
                logger.info("✅ Firebase connection test successful")
        except Exception as e:
            logger.warning(f"⚠️ Firebase connection test failed: {str(e)}")
    
    def create_analysis_session(self, startup_id: str, user_id: str = "demo_user") -> bool:
        """Create a new collaborative analysis session"""
        try:
            if not self.initialized:
                logger.warning("Firebase not available, skipping session creation")
                return False
            
            session_data = {
                'startup_id': startup_id,
                'user_id': user_id,
                'status': 'initiated',
                'progress': 0,
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP,
                'agents_completed': [],
                'current_agent': None,
                'results': {},
                'collaboration': {
                    'active_users': [user_id],
                    'session_start': time.time()
                }
            }
            
            doc_ref = self.db.collection('analysis_sessions').document(startup_id)
            doc_ref.set(session_data)
            
            logger.info(f"✅ Analysis session created for startup: {startup_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create analysis session: {str(e)}")
            return False
    
    def update_real_time_progress(self, startup_id: str, agent_name: str, progress: int, results: Dict[str, Any] = None) -> bool:
        """Update analysis progress in real-time"""
        try:
            if not self.initialized:
                logger.warning("Firebase not available, skipping progress update")
                return False
            
            update_data = {
                'progress': progress,
                'current_agent': agent_name,
                'updated_at': firestore.SERVER_TIMESTAMP,
                'last_activity': time.time()
            }
            
            # Add agent to completed list if progress indicates completion
            if progress >= 100:
                update_data['status'] = 'completed'
                update_data['current_agent'] = None
            elif agent_name:
                update_data[f'agents_completed'] = firestore.ArrayUnion([agent_name])
            
            # Add results if provided
            if results:
                update_data[f'results.{agent_name}'] = results
            
            doc_ref = self.db.collection('analysis_sessions').document(startup_id)
            doc_ref.update(update_data)
            
            logger.info(f"✅ Progress updated: {startup_id} - {agent_name} ({progress}%)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update progress: {str(e)}")
            return False
    
    def get_analysis_session(self, startup_id: str) -> Optional[Dict[str, Any]]:
        """Get current analysis session data"""
        try:
            if not self.initialized:
                return None
            
            doc_ref = self.db.collection('analysis_sessions').document(startup_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            else:
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to get analysis session: {str(e)}")
            return None
    
    def listen_to_progress_updates(self, startup_id: str, callback: Callable[[Dict[str, Any]], None]) -> Optional[Callable]:
        """Set up real-time listener for progress updates"""
        try:
            if not self.initialized:
                logger.warning("Firebase not available, cannot set up listener")
                return None
            
            def on_snapshot(doc_snapshot, changes, read_time):
                """Handle real-time updates"""
                for doc in doc_snapshot:
                    if doc.exists:
                        data = doc.to_dict()
                        callback(data)
            
            doc_ref = self.db.collection('analysis_sessions').document(startup_id)
            return doc_ref.on_snapshot(on_snapshot)
            
        except Exception as e:
            logger.error(f"❌ Failed to set up real-time listener: {str(e)}")
            return None
    
    def store_final_analysis_result(self, startup_id: str, complete_analysis: Dict[str, Any], user_id: str = "demo_user") -> bool:
        """Store the complete analysis result"""
        try:
            if not self.initialized:
                logger.warning("Firebase not available, skipping analysis storage")
                return False
            
            analysis_data = {
                "startup_id": startup_id,
                "user_id": user_id,
                "analysis_data": complete_analysis,
                "timestamp": time.time(),
                "created_at": firestore.SERVER_TIMESTAMP,
                "processing_time": complete_analysis.get("processing_time", 0),
                "agents_used": complete_analysis.get("agents_used", []),
                "status": "completed"
            }
            
            # Store in permanent collection
            doc_ref = self.db.collection('completed_analyses').document(startup_id)
            doc_ref.set(analysis_data)
            
            # Update session status
            session_ref = self.db.collection('analysis_sessions').document(startup_id)
            session_ref.update({
                'status': 'completed',
                'completed_at': firestore.SERVER_TIMESTAMP,
                'final_results': complete_analysis
            })
            
            logger.info(f"✅ Final analysis stored for startup: {startup_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to store final analysis: {str(e)}")
            return False
    
    def get_user_analysis_history(self, user_id: str = "demo_user") -> List[Dict[str, Any]]:
        """Get analysis history for a user"""
        try:
            if not self.initialized:
                logger.warning("Firebase not available, returning empty history")
                return []
            
            analyses = self.db.collection('completed_analyses')\
                             .where('user_id', '==', user_id)\
                             .order_by('timestamp', direction=firestore.Query.DESCENDING)\
                             .limit(10)\
                             .stream()
            
            history = []
            for doc in analyses:
                data = doc.to_dict()
                # Sanitize data for frontend
                history.append({
                    'startup_id': data.get('startup_id'),
                    'timestamp': data.get('timestamp'),
                    'processing_time': data.get('processing_time'),
                    'status': data.get('status'),
                    'company_name': data.get('analysis_data', {}).get('company_name', 'Unknown'),
                    'industry': data.get('analysis_data', {}).get('industry', 'Unknown')
                })
            
            return history
            
        except Exception as e:
            logger.error(f"❌ Failed to get analysis history: {str(e)}")
            return []
    
    def add_user_to_session(self, startup_id: str, user_id: str) -> bool:
        """Add user to collaborative session"""
        try:
            if not self.initialized:
                return False
            
            doc_ref = self.db.collection('analysis_sessions').document(startup_id)
            doc_ref.update({
                'collaboration.active_users': firestore.ArrayUnion([user_id]),
                'collaboration.last_joined': time.time()
            })
            
            logger.info(f"✅ User {user_id} added to session {startup_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to add user to session: {str(e)}")
            return False
    
    def get_demo_scenarios(self) -> List[Dict[str, Any]]:
        """Get demo scenarios from Firebase or return defaults"""
        try:
            if not self.initialized:
                return self._get_default_scenarios()
            
            scenarios = self.db.collection('demo_scenarios')\
                              .where('is_active', '==', True)\
                              .stream()
            
            firebase_scenarios = [doc.to_dict() for doc in scenarios]
            
            if firebase_scenarios:
                return firebase_scenarios
            else:
                # Return defaults if no scenarios in Firebase
                return self._get_default_scenarios()
            
        except Exception as e:
            logger.error(f"❌ Failed to get demo scenarios: {str(e)}")
            return self._get_default_scenarios()
    
    def _get_default_scenarios(self) -> List[Dict[str, Any]]:
        """Return default demo scenarios"""
        return [
            {
                "company_name": "MedAI Solutions",
                "industry": "Healthcare Technology",
                "stage": "Series A",
                "description": "AI-powered diagnostic platform for radiology",
                "funding_request": "$5M",
                "key_metrics": "200+ hospitals using platform, 95% accuracy rate"
            },
            {
                "company_name": "EcoTransport",
                "industry": "Clean Technology",
                "stage": "Seed",
                "description": "Electric vehicle charging network with renewable energy",
                "funding_request": "$2.5M",
                "key_metrics": "50 charging stations deployed, partnerships with 3 cities"
            },
            {
                "company_name": "FinanceFlow",
                "industry": "Financial Technology",
                "stage": "Series B",
                "description": "Automated financial planning for small businesses",
                "funding_request": "$15M",
                "key_metrics": "10,000+ SMB customers, $500K monthly recurring revenue"
            }
        ]
    
    def is_available(self) -> bool:
        """Check if Firebase is available and initialized"""
        return self.initialized and self.db is not None

# Global instance
enhanced_firebase_client = EnhancedFirebaseClient()
