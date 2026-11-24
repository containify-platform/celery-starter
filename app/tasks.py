import time

from app.worker import celery


@celery.task
def add(x: float, y: float) -> float:
    time.sleep(1)  # Stand-in for slow work: sending email, resizing images, calling an API.
    return x + y
