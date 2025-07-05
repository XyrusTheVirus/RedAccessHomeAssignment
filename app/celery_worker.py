from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)

celery_app.conf.timezone = 'UTC'
celery_app.conf.beat_schedule = {
    'delete-expired-rules-daily': {
        'task': 'tasks.cleanup.delete_expired_rules',
        'schedule': crontab(minute=0, hour=0),  # every midnight UTC
    }
}
