import firebase_admin
from firebase_admin import credentials, firestore, auth
import json
from app.core.config import settings

class FirebaseService:
    def __init__(self):
        if not firebase_admin._apps:
            # If FIREBASE_CREDENTIALS is a JSON string, parse it
            if settings.FIREBASE_CREDENTIALS.startswith('{'):
                cred_dict = json.loads(settings.FIREBASE_CREDENTIALS)
                cred = credentials.Certificate(cred_dict)
            else:
                # Otherwise, treat it as a path to a JSON file
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
                
            firebase_admin.initialize_app(cred)
            
        self.db = firestore.client()
        
    async def get_user_data(self, user_id):
        """Get user data from Firestore"""
        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            return user_doc.to_dict()
        return None
        
    async def update_user_data(self, user_id, data):
        """Update user data in Firestore"""
        user_ref = self.db.collection('users').document(user_id)
        user_ref.set(data, merge=True)
        return {"status": "success"}
        
    async def store_trip(self, user_id, trip_data):
        """Store a new trip in Firestore"""
        trip_ref = self.db.collection('users').document(user_id).collection('trips').document()
        trip_ref.set(trip_data)
        return {"id": trip_ref.id, **trip_data}
        
    async def get_user_trips(self, user_id):
        """Get all trips for a user"""
        trips_ref = self.db.collection('users').document(user_id).collection('trips')
        trips = [doc.to_dict() for doc in trips_ref.stream()]
        return trips
        
    async def verify_token(self, token):
        """Verify a Firebase ID token"""
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except Exception as e:
            return None

firebase_service = FirebaseService()