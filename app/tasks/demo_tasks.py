from app.extensions import celery

@celery.task()
def add_numbers(x, y):
    return x + y
