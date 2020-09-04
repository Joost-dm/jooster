""" Celery. """

from celery import Celery
import os

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_activity': {
        'task': 'main.tasks.check_activity',
        'schedule': crontab(minute='*/1')
    }
}


