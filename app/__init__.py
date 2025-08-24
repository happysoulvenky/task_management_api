from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import register_routes
from app.extensions import db, jwt, mail
from config import Config
from flask import Flask

def create_app(register_routes=True):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    if register_routes:
        from app.routes import register_routes
        register_routes(app)
        
    return app


