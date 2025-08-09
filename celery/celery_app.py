# celery_app.py
from celery import Celery

# Initialize Celery and configure it using the celeryconfig.py file
celery_app = Celery(__name__)
celery_app.config_from_object('celery_config')

@celery_app.task
def hello_world_task():
    """
    A simple Celery task that prints "Hello, World!"
    """
    print("Hello, World! from Celery task!")
    return "Hello, World! task completed."