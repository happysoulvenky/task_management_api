from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import register_routes
from app.extensions import db, jwt
from config import Config
from flask import Flask
from .extensions import celery, init_celery

def create_app(register_routes=True):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    if register_routes:
        from app.routes import register_routes
        register_routes(app)

    # Initialize Celery
    app = Flask(__name__)
    app.config.from_object(Config)
    init_celery(app)
        
    return app

