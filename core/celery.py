from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('django_settings_module', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
