from flask import Flask
from app.models import initialize_firebase


def create_app():
    app = Flask(__name__)

    # Initialize Firebase
    initialize_firebase()

    # Register API blueprint
    from app.apis.contact_api import contact_api
    app.register_blueprint(contact_api, url_prefix='/point-of-contact')

    # Register routes blueprint
    from app.routes import routes
    app.register_blueprint(routes)

    return app
