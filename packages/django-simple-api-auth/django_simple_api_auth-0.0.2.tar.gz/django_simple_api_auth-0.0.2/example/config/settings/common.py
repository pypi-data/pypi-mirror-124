# -*- coding: utf-8 -*-
"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import environ
from pathlib import Path

from common.environ import MrEnv

PREFIX_ENVVARS = "DJANGO"
env = MrEnv(PREFIX_ENVVARS)
# If you want override the envvar "DJANGO_SETTINGS_MODULE" put the
# following code into manage.py and wsgi.py:
# os.environ["DJANGO_SETTINGS_MODULE"] = os.environ.get("CUSTOMPREFIX_SETTINGS_MODULE")

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 2 = /)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Admins: Will receive emails when something breaks: django.request, sentry.errors...

ADMINS = []

# Django conf
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='').replace(' ', ',').split(',')

SECRET_KEY = env('SECRET_KEY', default='CHANGE ME!!!')

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    # FOR EXAMPLE THIS ONES
    # 'rest_framework',
    # 'django_extensions',
    'rest_framework',
    'graphene_django',
    'social_django',
    'django_simple_api_auth',
]

LOCAL_APPS = [
    # YOUR APPS
    'common',
    'users',
    'graphqls',
]

AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            ROOT_DIR('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': env.db("DATABASE_URL"),
}

"""
Use SQLite database for testing django base
"""
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'mydatabase',
#     }
# }


DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = 500

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = False

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = env('STATIC_ROOT', default=str(ROOT_DIR('staticfiles')))
STATIC_URL = env('STATIC_URL', default='/s/static/')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Media configuration

MEDIA_ROOT = env('MEDIA_ROOT', default=str(ROOT_DIR('media')))
MEDIA_URL = env('MEDIA_URL', default='/s/media/')

FILE_UPLOAD_PERMISSIONS = 0o664

# Logging configuration

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        # 'logfile': {
        #     'level':'DEBUG',
        #     'class':'logging.FileHandler',
        #     'filename': "/src/logs/logfile",
        # },
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s] [%(pathname)s:%(lineno)s] %(message)s",
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': '[%(asctime)s] %(name)s %(levelname)s %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'ERROR'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Fixture configuration

FIXTURE_DIRS = (
    ROOT_DIR('fixtures'),
)

# Email configuration

SERVER_EMAIL = env('SERVER_EMAIL', default='root@localhost')

# Debug configuration

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

    INTERNAL_IPS = ['127.0.0.1']

    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# Sentry configuration

SENTRY_ENABLED = env.bool('SENTRY_ENABLED', default=False)

if SENTRY_ENABLED:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        environment=env('SENTRY_ENVIRONMENT', default='production'),

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

    LOGGING['loggers']['sentry.errors'] = {
        'level': 'DEBUG',
        'handlers': ['console', 'mail_admins'],
        'propagate': False,
    }

# Load data configuration

CREATE_SUPER_USER = env.bool('CREATE_SUPER_USER', default=False)
DEFAULT_SUPER_USER_EMAIL = env('DEFAULT_SUPER_USER_EMAIL', default="info@mrmilu.com")
DEFAULT_SUPER_USER_PASSWORD = env('DEFAULT_SUPER_USER_PASSWORD', default='Pa$$ssw0ord')

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.api.exceptions.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ]
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

GRAPHENE = {
    "SCHEMA": "graphqls.schema.schema"
}

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Google configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "968504544267-b1p11th2jocqh3cg6vnhj3b1rmnak5s8.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "WkH_K78NmgepaQnYQ4pKeCTm"

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

ME_FIELDS = ("id", "email",)
