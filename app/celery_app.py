from celery import Celery
from celery.schedules import crontab
import os

def make_celery(app_name=__name__):
    return Celery(
        app_name,
        broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),

        include=["app.tasks.email_tasks"]
    )

celery = make_celery()


celery.conf.beat_schedule = {
    "send-daily-overdue-summary": {
        "task": "app.tasks.email_tasks.daily_overdue_summary",
        "schedule": crontab(hour=20, minute=0),  # every day at 8:00 PM
    },
}
celery.conf.timezone = "UTC"