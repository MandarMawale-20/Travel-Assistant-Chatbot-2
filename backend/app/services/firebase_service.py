import firebase_admin
from firebase_admin import credentials, firestore, auth
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class FirebaseService:
    def __init__(self):
        try:
            if not firebase_admin._apps:
                # If FIREBASE_CREDENTIALS is a JSON string, parse it
                if settings.FIREBASE_CREDENTIALS.startswith('{'):
                    cred_dict = json.loads(settings.FIREBASE_CREDENTIALS)
                    cred = credentials.Certificate(cred_dict)
                else:
                    # Otherwise, treat it as a path to a JSON file
                    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
                    
                firebase_admin.initialize_app(cred)
                logger.info("Firebase initialized successfully")
            
            self.db = firestore.client()
        except Exception as e:
            logger.error(f"Error initializing Firebase: {str(e)}")
            # Initialize as None but don't crash the app
            self.db = None
        
    async def get_user_data(self, user_id):
        """Get user data from Firestore"""
        if not self.db:
            logger.warning("Firestore not initialized, returning empty user data")
            return None
            
        try:
            user_ref = self.db.collection('users').document(user_id)
            user_doc = user_ref.get()
            
            if user_doc.exists:
                return user_doc.to_dict()
            return None
        except Exception as e:
            logger.error(f"Error getting user data: {str(e)}")
            return None
        
    async def update_user_data(self, user_id, data):
        """Update user data in Firestore"""
        if not self.db:
            logger.warning("Firestore not initialized, user data not updated")
            return {"status": "error", "message": "Database not available"}
            
        try:
            user_ref = self.db.collection('users').document(user_id)
            user_ref.set(data, merge=True)
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Error updating user data: {str(e)}")
            return {"status": "error", "message": str(e)}
        
    async def store_trip(self, user_id, trip_data):
        """Store a new trip in Firestore"""
        if not self.db:
            logger.warning("Firestore not initialized, trip not stored")
            return {"status": "error", "message": "Database not available"}
            
        try:
            trip_ref = self.db.collection('users').document(user_id).collection('trips').document()
            trip_ref.set(trip_data)
            return {"id": trip_ref.id, **trip_data}
        except Exception as e:
            logger.error(f"Error storing trip: {str(e)}")
            return {"status": "error", "message": str(e)}
        
    async def get_user_trips(self, user_id):
        """Get all trips for a user"""
        if not self.db:
            logger.warning("Firestore not initialized, returning empty trips")
            return []
            
        try:
            trips_ref = self.db.collection('users').document(user_id).collection('trips')
            trips = [{"id": doc.id, **doc.to_dict()} for doc in trips_ref.stream()]
            return trips
        except Exception as e:
            logger.error(f"Error getting user trips: {str(e)}")
            return []
        
    async def verify_token(self, token):
        """Verify a Firebase ID token"""
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            return None

firebase_service = FirebaseService()