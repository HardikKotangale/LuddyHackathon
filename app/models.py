import firebase_admin
from firebase_admin import credentials, db

def initialize_firebase():
    cred = credentials.Certificate("firebase_credentials.json")  # Replace with your key path
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://pointofcontact-dc059-default-rtdb.firebaseio.com/'  # Replace with your DB URL
    })
