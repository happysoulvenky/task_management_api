# celery/celery_config.py
from celery.schedules import crontab

beat_schedule = {
    "send-daily-overdue-summary": {
        "task": "app.tasks.task_management.send_daily_overdue_summary",
        "schedule": crontab(hour=9, minute=0),  # every day at 9 AM
    },
}

timezone = "UTC"
