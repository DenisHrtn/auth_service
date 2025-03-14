import logging

from celery import Celery

logger = logging.getLogger(__name__)

app = Celery(
    "worker",
    broker="redis://redis_fastapi:6379/0",
    backend="redis://redis_fastapi:6379/0",
)

app.conf.update(
    result_expires=3600,
    include=["app.infra.celery.tasks"],
)

logger.info("Celery worker started")
