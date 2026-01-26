import firebase_admin
from firebase_admin import credentials, firestore, auth
import os

# Path to serviceAccountKey.json in the nested folder
SERVICE_KEY_PATH = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json", "serviceAccountKey.json.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_KEY_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()
auth_client = auth