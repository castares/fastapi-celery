from celery import current_app as current_celery_app
from celery.result import AsyncResult

from app.config import settings
from app.users.tasks import divide


def create_celery():

    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")

    return celery_app


def get_task_info(task_id):
    task = AsyncResult(task_id)
    state = task.state

    response = {
        "state": task.state,
    }
    if state == "FAILURE":
        error = str(task.result)
        response.update(error=error)

    return response
