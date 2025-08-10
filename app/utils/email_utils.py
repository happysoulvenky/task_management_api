import threading
from flask_mail import Mail, Message
from config import Config

mail = Mail()  # Will be initialized in app factory

def init_mail(app):
    """Initialize Flask-Mail with existing app config."""
    mail.init_app(app)

# This function sends an email in a background thread to avoid blocking the request.
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
        html=f"<h3>New Task Created</h3><p>{task_title}</p>",
        sender=current_app.config["MAIL_USERNAME"]
    )
    threading.Thread(
        target=_send_async_email, 
        args=(current_app._get_current_object(), msg)
    ).start()

def send_status_update_email(task_title, old_status, new_status, recipient_email):
    """Send an email notifying that a task's status has been updated."""
    from flask import current_app
    msg = Message(
        subject=f"Task '{task_title}' Status Updated",
        recipients=[recipient_email],
        body=f"The status of task '{task_title}' has been changed from '{old_status}' to '{new_status}'.",
        html=f"<h3>Task Status Updated</h3><p>Task: {task_title}</p><p>Old Status: {old_status}</p><p>New Status: {new_status}</p>",
        sender=current_app.config["MAIL_USERNAME"]
    )
    threading.Thread(
        target=_send_async_email, 
        args=(current_app._get_current_object(), msg)
    ).start()   

def send_assignment_email(task_title, recipient_email):
    """Send an email notifying that a task has been assigned to a user."""
    from flask import current_app
    msg = Message(
        subject=f"You have been assigned to task '{task_title}'",
        recipients=[recipient_email],
        body=f"You have been assigned to the task '{task_title}'. Please check your task list.",
        html=f"<h3>Task Assignment</h3><p>You have been assigned to the task: {task_title}</p>",
        sender=current_app.config["MAIL_USERNAME"]
    )
    threading.Thread(
        target=_send_async_email, 
        args=(current_app._get_current_object(), msg)
    ).start()

def send_priority_change_email(task_title, new_priority, recipient_email):
    """Send an email notifying that a task's priority has been changed."""
    from flask import current_app
    msg = Message(
        subject=f"Task '{task_title}' Priority Changed",
        recipients=[recipient_email],
        body=f"The priority of task '{task_title}' has been changed to {new_priority}.",
        html=f"<h3>Task Priority Changed</h3><p>Task: {task_title}</p><p>New Priority: {new_priority}</p>",
        sender=current_app.config["MAIL_USERNAME"]
    )
    threading.Thread(
        target=_send_async_email, 
        args=(current_app._get_current_object(), msg)
    ).start()    

def send_overdue_task_email(task_title, recipient_email):
    """Send an email notifying that a task is overdue."""
    from flask import current_app
    msg = Message(
        subject=f"Overdue Task: '{task_title}'",
        recipients=[recipient_email],
        body=f"The task '{task_title}' is overdue. Please take action.",
        html=f"<h3>Overdue Task</h3><p>The task '{task_title}' is overdue. Please take action.</p>",
        sender=current_app.config["MAIL_USERNAME"]
    )
    threading.Thread(
        target=_send_async_email, 
        args=(current_app._get_current_object(), msg)
    ).start()
    