import os
from celery import Celery
from dotenv import load_dotenv
load_dotenv()

celery = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL"),
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    include=["app.celery_workers.webhook_worker"],  # Tell Celery where tasks are defined
)


