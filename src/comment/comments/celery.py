from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comment_service.settings')  # Point to your main settings

app = Celery('comments')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # Automatically finds tasks in tasks.py

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
