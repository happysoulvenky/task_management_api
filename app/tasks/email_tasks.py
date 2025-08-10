from app.celery_app import celery
from app.utils.email_utils import send_email
import datetime

@celery.task
def send_async_email(subject, recipients, body):
    send_email(subject=subject, recipients=recipients, body=body)

@celery.task
def daily_overdue_summary():
    # Your logic to get overdue tasks from DB
    from app.models import Task, User
    overdue_tasks = Task.query.filter(Task.due_date < datetime.utcnow(), Task.status != "completed").all()
    # Send summary email per user
    for user in User.query.all():
        user_tasks = [t for t in overdue_tasks if t.user_id == user.id]
        if user_tasks:
            body = f"Overdue tasks:\n" + "\n".join(t.title for t in user_tasks)
            send_email(subject="Daily Overdue Tasks", recipients=[user.email], body=body)
