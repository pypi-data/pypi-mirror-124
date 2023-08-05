from __future__ import absolute_import

import environ
from celery import Celery
from common.environ import MrEnv

PREFIX_ENVVARS = "DJANGO"

env = MrEnv(PREFIX_ENVVARS)

django_celery_broker = env('CELERY_BROKER', default='amqp://guest@localhost://')

app = Celery('app', broker=django_celery_broker)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
