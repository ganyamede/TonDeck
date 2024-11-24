import os

from flask import Flask
from .routes import auth_bp

def create_app():
    app = Flask(__name__, template_folder='/Users/getapple/PycharmProjects/TONDeck/server/App/templates')

    app.register_blueprint(auth_bp, url_prefix='/')

    return app