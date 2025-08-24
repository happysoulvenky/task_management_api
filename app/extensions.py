# app/extensions.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from celery import Celery
from celery import Celery
from celery.schedules import crontab
celery = Celery(
	__name__,
	broker='redis://localhost:6379/0',
	backend='redis://localhost:6379/0'
)
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()

# def init_celery(app):
#     """Initialize Celery with Flask app configuration."""
#     celery.conf.update(
#         broker_url=app.config.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
#         result_backend=app.config.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
#         timezone=app.config.get("CELERY_TIMEZONE", "UTC"),
#         task_serializer='json',
#         accept_content=['json'],
#         result_serializer='json',
#         task_track_started=True,
#         task_time_limit=30 * 60,  # 30 minutes
#         worker_prefetch_multiplier=1,
#         beat_schedule={
#             'check-overdue-tasks-daily': {
#                 'task': 'app.tasks.task_management.fetch_and_print_overdue_tasks',
#                 'schedule': crontab(hour=9, minute=0),  # Every day at 9:00 AM
#                 'args': (),
#             },
#             'send-task-reminders': {
#                 'task': 'app.tasks.task_management.send_task_reminders', 
#                 'schedule': crontab(hour=8, minute=0),  # Every day at 8:00 AM
#                 'args': (),
#             },
#             'generate-daily-report': {
#                 'task': 'app.tasks.task_management.generate_task_report',
#                 'schedule': crontab(hour=7, minute=0),  # Every day at 7:00 AM
#                 'args': (),
#             },
#             'send-weekly-summary-email': {
#                 'task': 'app.tasks.task_management.send_weekly_summary_email',
#                 'schedule': crontab(hour=10, minute=0, day_of_week=1),  # Every Monday at 10:00 AM
#                 'args': (),
#             },
#             'cleanup-completed-tasks': {
#                 'task': 'app.tasks.task_management.cleanup_completed_tasks',
#                 'schedule': crontab(hour=2, minute=0, day_of_week=0),  # Every Sunday at 2:00 AM
#                 'args': (),
#             },
#         }
#     )
#     
#     # Set up Flask context for Celery tasks
#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)
#     
#     celery.Task = ContextTask
#     return celery
