from .common import *

# Databases

DATABASES = {
    'default': env.db("DATABASE_URL_TEST", default="psql://bbtest:bbtest@127.0.0.1:5432/bbtest"),
}

DATABASES['default']['ATOMIC_REQUESTS'] = True

# Custom config

EMAIL_NOTIFICATIONS_ENABLED = False
