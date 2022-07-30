###
# В целях демонстрации данные для запуска проекта загружены в репозиторий.
###

SECRET_KEY = '3j4k5jn34kr34n9oka;mldsanmekj345njd:&&^&*322988hdsdlkemw:::#289dj'

DEFAULT_HOST = 'http://127.0.0.1:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lectonic_test',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

