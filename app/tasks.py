from app.celery_utils import celery_app
from app.extensions import db
from app.models import User, Task
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
from datetime import datetime, timedelta

@celery_app.task
def send_email_notification(recipient_email, subject, body):
    """
    Celery task to send an email notification.
    """
    sender_email = Config.MAIL_USERNAME
    sender_password = Config.MAIL_PASSWORD
    smtp_server = Config.MAIL_SERVER
    smtp_port = Config.MAIL_PORT
    use_tls = Config.MAIL_USE_TLS

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            if use_tls:
                server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
        return False

@celery_app.task
def send_daily_overdue_summary():
    """
    Celery task to send a daily summary of overdue tasks to users.
    This task should be scheduled to run once daily.
    """
    print("Running daily overdue task summary...")
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    # Fetch users with overdue tasks
    # This query finds users who have tasks that were due yesterday or earlier
    # and are not yet 'done'
    users_with_overdue_tasks = db.session.query(User).join(Task).filter(
        Task.assigned_to_id == User.id,
        Task.due_date <= yesterday,
        Task.status != 'done'
    ).distinct().all()

    for user in users_with_overdue_tasks:
        overdue_tasks = Task.query.filter(
            Task.assigned_to_id == user.id,
            Task.due_date <= yesterday,
            Task.status != 'done'
        ).all()

        if overdue_tasks:
            subject = "Daily Overdue Task Summary"
            body_lines = [f"Hello {user.email},", "", "Here are your overdue tasks:"]
            for task in overdue_tasks:
                body_lines.append(f"- Project: {task.project.name}, Task: {task.title} (Due: {task.due_date.strftime('%Y-%m-%d')})")
            body_lines.append("\nPlease prioritize completing these tasks.")
            body = "\n".join(body_lines)

            # Enqueue the email sending task
            send_email_notification.delay(user.email, subject, body)
            print(f"Enqueued overdue summary email for {user.email}")
    print("Finished daily overdue task summary.")