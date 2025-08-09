from app import create_app
from celery_utils import make_celery

flask_app = create_app()
celery = make_celery()
celery.conf.update(flask_app.config)

# Import all tasks so Celery can register them
import app.tasks.demo_tasks

