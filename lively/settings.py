import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f#qiorpa9id!n$v#1*(ne16j9%hpa3zqo)u#)jtu=jqge#t%g!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['*']

ADMINS = (
  ('Zaman', 'zamanafzal@gmail.com'),
  ('Aamish', 'aamish.iftikhar@arbisoft.com'),
)
PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'rest_framework_swagger',
    'djcelery',
    'haystack',
    'dbbackup',
]

PROJECT_APPS = [
    'apps.area',
    'apps.region',
    'apps.city',
    'apps.branch',
    'apps.person',
    'apps.question',
    'apps.option',
    'apps.promotion',
    'apps.review',
    'apps.questionnaire',
    'apps.report',
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'lively.urls'

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

WSGI_APPLICATION = 'lively.wsgi.application'

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_L10N = True
USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False

CORS_ALLOW_HEADERS = (
        'x-requested-with',
        'content-type',
        'accept',
        'origin',
        'authorization',
        'x-csrftoken',
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = "%s%s" % (BASE_DIR, "/static/")
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(os.path.dirname(__file__), 'static'),)

# TEMPLATE_DIRS = (
#     os.path.join(BASE_DIR, 'templates'),
# )

DIRS = [os.path.join(BASE_DIR,'templates')]

EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mclivefeed@gmail.com'
EMAIL_HOST_PASSWORD = 'Arbisoft123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'LiveFeed Support <no-reply@livefeed.com>'

WEBSOCKET_ADDRESS = '172.16.11.113'
WEBSOCKET_PORT = '5678'

#CELERY Settings
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

#------------------------- Parse Constants --------------------------
#MFS - Staging Keys
APPLICATION_ID = "FMn5KgyYiLRjLxvi1zIh3KQNV6OpOxhZu0CswXCa"
REST_API_KEY = "fIGO4Y5KdvgKM8dsspYQrfO5raxdfmbaDdodeQOb"
MASTER_KEY = "dp1YtF7VkUvRYAhmCtc52hlb5jmjpBZAVFSuYexo"


#------------------------- AWS S3 Keys --------------------------
AWS_ACCESS_KEY_ID = "AKIAIXOMJ2SLOFOJYADQ"
AWS_SECRET_ACCESS_KEY = "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"


#----------------------- mail gun credentials--------------------
api_key = 'key-ae81bf507aa18292f186252f9fdc65ee'
domain = 'sentimeter.io'

try:
    from lively.local_settings import *
except ImportError:
    pass