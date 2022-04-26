import os
from pathlib import Path

from django.conf import settings

settings.configure()

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
AS_TEST = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Дополнительный функционал
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'channels',
    'django_dump_load_utf8',

    # Наши приложения
    'adminapp',
    'questapp',
    'emailapp',
    'authapp',
    'workroomsapp',
    'chatapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'authapp.utils.authapp_middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'https://dev.lectonic.ru',
    'https://lectonic.ru',
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r'^http://(localhost|192\.168\.1\.[0-9][0-9]|127\.0\.0\.1):[\d]+$',
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'speakers.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

ASGI_APPLICATION = "speakers.asgi.application"
WSGI_APPLICATION = 'speakers.wsgi.application'

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'authapp.utils.authapp_token.TokenAuthentication',
    ]
}

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authapp.User'


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'standart': {
#             'format': '{asctime} {levelname} {message}',
#             'style': '{',
#         },
#         'forwarning': {
#             'format': '{asctime} {levelname} {pathname} {message}',
#             'style': '{',
#         },
#         'forerror': {
#             'format': '{asctime} {levelname} {pathname} {exc_info} {message}',
#             'style': '{',
#         }
#     },
#     'handlers': {
#         'general': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'log/general.log',
#             'formatter': 'standart'
#         },
#         'errors': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': 'log/errors.log',
#             'formatter': 'forerror'
#         },
#         'console': {
#             'level': 'INFO',
#             'class': 'logging.StreamHandler',
#             'formatter': 'standart',
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'general'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['errors'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }


try:
    from .local_settings import *
except ImportError:
    from .prod_settings import *
