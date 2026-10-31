"""Example Celery tasks for workers."""


from backend.workers.celery_app import celery_app


@celery_app.task(bind=True, name="workers.ping", autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
def ping(self) -> str:
    """Simple health task that returns 'pong'."""
    return "pong"


@celery_app.task(bind=True, name="workers.add", autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
def add(self, x: int, y: int) -> int:
    """Add two integers and return the sum."""
    return x + y
