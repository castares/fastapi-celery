import random

from asgiref.sync import async_to_sync
from celery import shared_task
from celery.signals import task_postrun
from celery.utils.log import get_task_logger
import requests


logger = get_task_logger(__name__)


@shared_task
def divide(x, y):

    import time

    time.sleep(10)
    return x / y


@shared_task()
def sample_task(email):
    from app.users.views import api_call

    api_call(email)


@shared_task(bind=True)
def task_process_notification(self):
    try:
        if not random.choice([0, 1]):
            # mimic random error
            raise Exception()

        # this would block the I/O
        requests.post("https://httpbin.org/delay/5")
    except Exception as e:
        logger.error("exception raised, it would be retry after 5 seconds")
        raise self.retry(exc=e, countdown=5)


@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    from app.ws.views import update_celery_task_status

    async_to_sync(update_celery_task_status)(task_id)

    from app.ws.views import update_celery_task_status_socketio

    update_celery_task_status_socketio(task_id)


@shared_task(name="task_schedule_work")
def task_schedule_work():
    logger.info("task_schedule_work_run")
