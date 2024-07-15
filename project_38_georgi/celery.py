import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_38_georgi.settings")

app = Celery("project_38_georgi")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(
    worker_concurrency=2,
)

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
