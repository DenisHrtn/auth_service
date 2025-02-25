from celery_app import app


@app.task
def debug_task(arg1, arg2):
    return f"{arg1} {arg2}"
