from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.timezone = 'Europe/Moscow'

app.conf.beat_schedule = {
    'rate-prediction-daily-9-AM': {
        'task': 'task_update_rate_prediction',
        'schedule': crontab(minute="0", hour="9"),
        'args': (7,)
    },
}