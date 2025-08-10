from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import register_routes
from app.extensions import db, jwt # celery, init_celery
from config import Config
from flask import Flask
from app.utils.email_utils import init_mail
from celery import Celery
from app.celery_app import celery

def create_app(register_routes=True):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    jwt.init_app(app)
    init_mail(app)
    

    init_celery(app)
    # Initialize Celery with Flask app
    # init_celery(app)

    # with app.app_context():
    #     from . import models
    #     db.create_all()

    if register_routes:
        from app.routes import register_routes
        register_routes(app)
        
    return app


def init_celery(app):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask