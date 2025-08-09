# celeryconfig.py
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
timezone = 'Asia/Kolkata' # Set to your local timezone (e.g., 'UTC', 'America/New_York')

# Optional: Define a periodic task to run automatically (for future reference) # type: ignore
# beat_schedule = {
#     'print-hello-every-10-seconds': {
#         'task': 'celery_app.hello_world_task',
#         'schedule': 10.0, # Run every 10 seconds
#         'args': (),
#     },
# }