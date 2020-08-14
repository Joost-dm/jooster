"""
Django settings for forum project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

import dj_database_url

import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WSGI_APPLICATION = 'main.wsgi.application'
SECRET_KEY = config('SECRET_KEY')
ROOT_URLCONF = 'main.urls'
DEBUG = config('DEBUG', cast=bool)

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'authorization',
    'rest_framework.authtoken',
    'forum',
    'djoser',
    'storages',
]

# Middleware

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'main.middleware.ResponseTimeCounter',
    'main.middleware.UsersOnlineChecker'
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', '127.0.0.1'),
        'PORT': config('DB_PORT', '5432'),
    }
}

# Redis settings

REDIS_SETTINGS = {
    'users_online': {
        'HOST': config('REDIS_HOST', '127.0.0.1'),
        'PORT': config('REDIS_PORT', '6379'),
        'DB': config('REDIS_USERS_ONLINE_BD', 2),
        'PASSWORD': config('REDIS_PASSWORD'),
        'SESSION_LENGTH': 120  # seconds
    }
}

#db_from_env = dj_database_url.config()
#DATABASES['default'].update(db_from_env)

# CORS settings

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# AWS settings

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN')
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

# Staticfiles settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Mediafiles settings

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'main.storage_backends.MediaStorage'

# User settings

AUTH_USER_MODEL = 'authorization.CustomUser'
USER_SETTINGS = {
    'USER_AVATAR_SETTINGS': {
        'AVATAR_IMAGE_NAME': 'avatar',
        'MAX_WIDTH': 2000,
        'MAX_HEIGHT': 2000,
        'MAX_SIZE': 500000,
        'COMPRESSED_WIDTH': 100,
        'COMPRESSED_HEIGHT': 100
    }
}
# Djoser settings https://djoser.readthedocs.io/en/latest/settings.html

DJOSER = {
    'HIDE_USERS': False,
    'SERIALIZERS': {
        'user': 'authorization.serializers.UserDetailSerializer',
        'current_user': 'authorization.serializers.UserDetailSerializer',
    },
}

# Sentry integration
sentry_sdk.init(
    dsn="https://046746da485d4936be201e4c5d4ba4e7@o385638.ingest.sentry.io/5218745",
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)


# Templates

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]


# Rest framework settings

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],

    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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



