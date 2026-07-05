from celery import Celery
from config import REDIS_BROKER_URL, REDIS_RESULT_BACKEND

celery = Celery(
    "url_shortener",
    broker=REDIS_BROKER_URL,
    backend=REDIS_RESULT_BACKEND,
    include=["tasks"]     
)