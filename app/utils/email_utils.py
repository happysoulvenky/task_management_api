import threading
from flask_mail import Mail, Message

mail = Mail()  # Will be initialized in app factory

def init_mail(app):
    """Initialize Flask-Mail with existing app config."""
    mail.init_app(app)

def _send_async_email(app, msg):
    """Send email in a background thread."""
    with app.app_context():
        mail.send(msg)

def send_task_created_email(task_title, recipient_email):
    """Send an email notifying that a new task was created."""
    from flask import current_app
    msg = Message(
        subject="New Task Created",
        recipients=[recipient_email],
        body=f"A new task '{task_title}' has been created.",
        html=f"<h3>New Task Created</h3><p>{task_title}</p>"
    )
    threading.Thread(
        target=_send_async_email, 
        args=(current_app._get_current_object(), msg)
    ).start()
