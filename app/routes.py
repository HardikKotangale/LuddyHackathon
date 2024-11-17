from flask import Blueprint, render_template

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    """
    Homepage of the application.
    """
    return render_template('index.html', title="Home")
