# Celery Integration for Task Management System

This document explains how to use the Celery integration for background task processing in your Flask application.

## Overview

The Celery integration provides the following functionality:
- **Overdue Task Monitoring**: Daily checks for overdue tasks with email notifications
- **Task Reminders**: Email notifications for tasks due within 24 hours
- **Weekly Summary Reports**: Comprehensive weekly email summaries for all users
- **Task Reports**: Daily summary reports
- **Task Status Updates**: Asynchronous task status changes
- **Cleanup Tasks**: Periodic cleanup of old completed tasks

## Email Features

The system automatically sends the following email notifications:

### 1. Daily Task Reminders (8:00 AM)
- Sent to users with tasks due within 24 hours
- Includes task details: title, project, due date, priority, status
- HTML formatted with clear task listings

### 2. Overdue Task Alerts (9:00 AM)  
- Sent to users with overdue tasks
- Highlights urgency with red color coding
- Shows days overdue for each task
- Includes all overdue task details

### 3. Weekly Summary Reports (Monday 10:00 AM)
- Comprehensive task statistics for each user
- Shows pending, in-progress, completed, and overdue counts
- Lists upcoming tasks due this week
- Highlights overdue tasks requiring attention

### Email Configuration Requirements

Add these settings to your `.env` file:

```env
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your.email@gmail.com
MAIL_PASSWORD=your.app.password
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER=your.email@gmail.com
```

## Installation & Setup

### 1. Install Dependencies
Make sure you have Redis running and the required Python packages:

```bash
pip install celery redis
```

### 2. Start Redis
Celery requires Redis as a message broker:

```bash
# On Windows (if you have Redis installed)
redis-server

# On Docker
docker run -d -p 6379:6379 redis:alpine
```

### 3. Configure Environment
Update your `.env` file or environment variables:

```env
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
CELERY_TIMEZONE=UTC
```

## Running Celery

### Development Mode (Single Process)
For development, you can run both worker and beat scheduler in one process:

```bash
python -m celery -A celery_worker worker --beat --loglevel=info
```

### Production Mode (Separate Processes)

#### Start Worker
```bash
python -m celery -A celery_worker worker --loglevel=info
```

#### Start Beat Scheduler
```bash
python -m celery -A celery_worker beat --loglevel=info
```

#### Monitor Tasks
```bash
python -m celery -A celery_worker flower
```

## Available Tasks

### Scheduled Tasks (Run Automatically)

1. **Generate Daily Report** (`generate_task_report`)
   - **Schedule**: Daily at 7:00 AM
   - **Purpose**: Creates summary reports of task statistics
   - **Output**: Task counts by status

2. **Send Task Reminders** (`send_task_reminders`)
   - **Schedule**: Daily at 8:00 AM  
   - **Purpose**: Sends email reminders for tasks due within 24 hours
   - **Recipients**: Users with tasks due soon
   - **Email Content**: Task details with due dates

3. **Check Overdue Tasks** (`fetch_and_print_overdue_tasks`)
   - **Schedule**: Daily at 9:00 AM
   - **Purpose**: Identifies overdue tasks and sends email alerts
   - **Recipients**: Users with overdue tasks
   - **Email Content**: Overdue task details with urgency indicators

4. **Send Weekly Summary** (`send_weekly_summary_email`)
   - **Schedule**: Weekly on Monday at 10:00 AM
   - **Purpose**: Comprehensive weekly task summary for each user
   - **Recipients**: All users with assigned tasks
   - **Email Content**: Task statistics, overdue alerts, upcoming tasks

5. **Cleanup Completed Tasks** (`cleanup_completed_tasks`)
   - **Schedule**: Weekly on Sunday at 2:00 AM
   - **Purpose**: Archives or cleans up old completed tasks
   - **Default**: Tasks completed more than 30 days ago

### Manual Tasks

1. **Update Task Status** (`update_task_status`)
   ```python
   from app.tasks.task_management import update_task_status
   update_task_status.delay(task_id=123, new_status='in_progress')
   ```

## Testing & Debugging

### Test Celery Setup
```bash
python test_celery.py
```

### Test Email Functionality
```bash
python test_email.py
```

### List Available Tasks
```bash
python celery_utils.py --list-tasks
```

### Run Single Task Manually
```bash
python celery_utils.py --run-task app.tasks.task_management.generate_task_report
```

### Monitor Task Queue
```bash
python -m celery -A celery_worker inspect active
python -m celery -A celery_worker inspect scheduled
```

## Task Configuration

### Beat Schedule
The scheduled tasks are configured in `app/extensions.py`:

```python
beat_schedule={
    'check-overdue-tasks-daily': {
        'task': 'app.tasks.task_management.fetch_and_print_overdue_tasks',
        'schedule': crontab(hour=9, minute=0),
        'args': (),
    },
    # ... more tasks
}
```

### Customizing Schedules
You can modify the schedules by editing the `beat_schedule` in `app/extensions.py`:

```python
from celery.schedules import crontab

# Examples:
crontab(hour=9, minute=0)              # Daily at 9:00 AM
crontab(hour=0, minute=0, day_of_week=1)  # Every Monday at midnight
crontab(minute='*/15')                 # Every 15 minutes
```

## File Structure

```
├── app/
│   ├── tasks/
│   │   ├── demo_tasks.py          # Simple example tasks
│   │   └── task_management.py     # Main task management tasks
│   └── extensions.py              # Celery configuration
├── celery/
│   ├── celery_app.py             # Legacy (deprecated)
│   └── celery_config.py          # Legacy config
├── celery_worker.py              # Main worker entry point
├── celery_utils.py               # Testing utilities
└── test_celery.py               # Setup verification script
```

## Integration with Flask Routes

You can trigger tasks from your Flask routes:

```python
from app.tasks.task_management import update_task_status, send_task_reminders

@app.route('/task/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    # Update status asynchronously
    update_task_status.delay(task_id, 'done')
    return jsonify({'message': 'Task completion queued'})

@app.route('/admin/send-reminders', methods=['POST'])
def send_reminders():
    # Send reminders manually
    send_task_reminders.delay()
    return jsonify({'message': 'Reminder sending queued'})
```

## Troubleshooting

### Common Issues

1. **Redis Connection Error**
   - Ensure Redis is running: `redis-cli ping`
   - Check CELERY_BROKER_URL configuration

2. **Tasks Not Running**
   - Verify worker is running: `celery -A celery_worker inspect ping`
   - Check task imports in `celery_worker.py`

3. **Database Context Errors**
   - Tasks automatically run with Flask app context
   - Check `ContextTask` is properly configured

4. **Email Tasks Failing**
   - Ensure email configuration is set up in Flask app
   - Check `MAIL_*` environment variables

### Logs and Monitoring

- Worker logs: Check console output when running worker
- Task results: Use Flower for web-based monitoring
- Redis monitoring: Use `redis-cli monitor`

## Production Deployment

For production deployment:

1. Use proper Redis configuration (authentication, persistence)
2. Run multiple worker processes
3. Use a process manager (systemd, supervisor)
4. Set up monitoring and alerting
5. Configure log rotation
6. Use Redis Sentinel for high availability

Example systemd service:

```ini
[Unit]
Description=Celery Worker
After=network.target

[Service]
Type=forking
User=your-app-user
Group=your-app-group
WorkingDirectory=/path/to/your/app
ExecStart=/path/to/venv/bin/celery -A celery_worker worker --detach
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
Restart=always

[Install]
WantedBy=multi-user.target
```
