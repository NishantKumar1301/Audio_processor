# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
# from celery.schedules import crontab

# # Set the default Django settings module for Celery
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# app = Celery('project')

# # Load settings from Django's settings.py using the 'CELERY' namespace
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Auto-discover tasks from all installed apps
# app.autodiscover_tasks()

# # Define a simple debug task (optional)
# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

# # Celery Beat schedule for periodic tasks
# app.conf.beat_schedule = {
#     'run-daily-audio-openai-requests': {
#         'task': 'app.tasks.process_audio_and_openai_requests_task',
#         'schedule': crontab(hour=21, minute=0),  # Runs daily at 9 PM IST
#     },
# }

# # Set the timezone for the task schedule
# app.conf.timezone = 'Asia/Kolkata'
