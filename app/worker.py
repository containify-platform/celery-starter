import os

from celery import Celery

# Valkey is the broker (the task queue) and the result backend.
# On Containify both apps get REDIS_URL from the Valkey app.
redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

celery = Celery("app", broker=redis_url, backend=redis_url, include=["app.tasks"])
celery.conf.update(
    broker_connection_retry_on_startup=True,
    result_expires=3600,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)
