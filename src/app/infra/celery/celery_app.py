from celery import Celery

app = Celery(
    "worker",
    broker="redis://redis:6380/0",
    backend="redis://redis:6380/0",
)

app.conf.update(
    result_expires=3600,
)
