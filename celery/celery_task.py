# run_task.py
from celery_app import hello_world_task
import time

if __name__ == '__main__':
    print("Calling the hello_world_task...")
    # .delay() sends the task to the broker
    result = hello_world_task.delay()
    print(f"Task ID: {result.id}")

    # You can get the result if needed (blocks until task is done)
    # print(f"Task result: {result.get()}")
    # print("Task finished.")