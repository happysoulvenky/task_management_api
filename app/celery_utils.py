# app/celery_utils.py
from celery import Celery
from flask import Flask
from config import Config
from celery.schedules import crontab # Import crontab

def make_celery(app_name=__name__):
    celery = Celery(app_name) # Initialize without broker/backend directly here

    # --- THIS LINE IS CRUCIAL FOR LOADING YOUR CONFIG ---
    celery.config_from_object(Config)
    # ---------------------------------------------------
    print("Celery configuration loaded from Config")
    # The beat_schedule update can stay as it is

    # Configure Celery Beat schedule here
    celery.conf.update(
        beat_schedule = {
            'send-daily-overdue-summary': {
                'task': 'app.tasks.send_daily_overdue_summary',
                'schedule': crontab(hour=0, minute=0), # Run daily at midnight UTC
                # 'schedule': timedelta(seconds=60), # For testing: run every minute
                'args': (),
            },
        }
    )
    return celery

celery_app = make_celery()