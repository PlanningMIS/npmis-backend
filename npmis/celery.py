import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "npmis.settings.dev")

app = Celery("npmis")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()