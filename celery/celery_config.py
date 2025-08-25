# celery/celery_config.py
from celery.schedules import crontab
from app.celery_app import celery
from app.tasks.email_tasks import daily_overdue_summary


beat_schedule = {
    "send-daily-overdue-summary": {
        "task": "app.tasks.email_tasks.daily_overdue_summary",
        "schedule": crontab(minute='*/5'),  # every 5 minutes
    },
}

timezone = "UTC"