import firebase_admin
from firebase_admin import credentials, db
import os
import base64

def initialize_firebase():
    # Check if running in Heroku or local
    firebase_key_base64 = os.environ.get("FIREBASE_KEY")  # Heroku environment variable
    firebase_credentials_path = "firebase_credentials.json"

    # If the Base64 key is found, decode and save it as a file
    if firebase_key_base64:
        with open(firebase_credentials_path, "w") as f:
            f.write(base64.b64decode(firebase_key_base64).decode())
    
    # Initialize Firebase
    cred = credentials.Certificate(firebase_credentials_path)  # Use decoded file path
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://pointofcontact-dc059-default-rtdb.firebaseio.com/'  # Replace with your DB URL
    })
