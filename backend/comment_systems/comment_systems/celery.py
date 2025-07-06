import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comment_systems.settings")
app = Celery("comment_systems")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
