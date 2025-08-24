import datetime
from itertools import groupby
from operator import attrgetter

from sqlalchemy.orm import joinedload

from app.extensions import mail
from flask_mail import Message


@celery.task
def send_async_email(subject, recipients, body, html=None):
    """Celery task to send an email asynchronously."""
    from flask import current_app
    msg = Message(
        subject=subject,
        recipients=recipients,
        body=body,
        html=html,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER")
    )
    mail.send(msg)


@celery.task
def daily_overdue_summary():
    """
    Sends a daily summary of overdue tasks to each user.
    This task is optimized to perform a single DB query.
    """
    from app.models import Task, User

    overdue_tasks_q = Task.query.options(
        joinedload(Task.assignee)
    ).filter(
        Task.due_date < datetime.datetime.utcnow(),
        Task.status != "completed",
        Task.assigned_to_id.isnot(None)
    ).order_by(Task.assigned_to_id)

    for user, tasks_for_user in groupby(overdue_tasks_q, key=attrgetter('assignee')):
        if user and user.email:
            task_titles = [t.title for t in tasks_for_user]
            body = f"Hi {user.email},\n\nYou have the following overdue tasks:\n" + "\n".join(f"- {title}" for title in task_titles)
            html_body = f"<h3>Daily Overdue Tasks</h3><p>Hi {user.email},</p><p>You have the following overdue tasks:</p><ul>"
            html_body += "".join(f"<li>{title}</li>" for title in task_titles)
            html_body += "</ul>"
            send_async_email.delay(
                subject="Daily Overdue Tasks Summary",
                recipients=[user.email],
                body=body,
                html=html_body
            )
