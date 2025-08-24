from app.tasks.email_tasks import send_async_email

def send_task_created_email(task_title, recipient_email):
    """Send an email notifying that a new task was created."""
    subject = "New Task Created"
    body = f"A new task '{task_title}' has been created."
    html = f"<h3>New Task Created</h3><p>A new task '{task_title}' has been created.</p>"
    try:
        send_async_email(subject, [recipient_email], body, html)
    except Exception as e:
        print(f"Error sending email: {e}")
        # Handle the exception (e.g., log it)
        pass

def send_status_update_email(task_title, old_status, new_status, recipient_email):
    """Send an email notifying that a task's status has been updated."""
    subject = f"Task '{task_title}' Status Updated"
    body = f"The status of task '{task_title}' has been changed from '{old_status}' to '{new_status}'."
    html = f"<h3>Task Status Updated</h3><p>Task: {task_title}</p><p>Old Status: {old_status}</p><p>New Status: {new_status}</p>"
    send_async_email(subject, [recipient_email], body, html)

def send_assignment_email(task_title, recipient_email):
    """Send an email notifying that a task has been assigned to a user."""
    subject = f"You have been assigned to task '{task_title}'"
    body = f"You have been assigned to the task '{task_title}'. Please check your task list."
    html = f"<h3>Task Assignment</h3><p>You have been assigned to the task: {task_title}</p>"
    send_async_email(subject, [recipient_email], body, html)

def send_priority_change_email(task_title, new_priority, recipient_email):
    """Send an email notifying that a task's priority has been changed."""
    subject = f"Task '{task_title}' Priority Changed"
    body = f"The priority of task '{task_title}' has been changed to {new_priority}."
    html = f"<h3>Task Priority Changed</h3><p>Task: {task_title}</p><p>New Priority: {new_priority}</p>"
    send_async_email(subject, [recipient_email], body, html)

def send_overdue_task_email(task_title, recipient_email):
    """Send an email notifying that a task is overdue."""
    subject = f"Overdue Task: '{task_title}'"
    body = f"The task '{task_title}' is overdue. Please take action."
    html = f"<h3>Overdue Task</h3><p>The task '{task_title}' is overdue. Please take action.</p>"
    send_async_email(subject, [recipient_email], body, html)