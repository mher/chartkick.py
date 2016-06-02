DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATIC_ROOT = ''
STATIC_URL = '/static/'

import chartkick
STATICFILES_DIRS = (
    chartkick.js(),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '5ry^!i1c6y*$396rb@^ibm1m%eg-aaw8mf0qurk%+a3-r5woo)'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['charts'],
        'APP_DIRS': True,
    },
]

ROOT_URLCONF = 'charts.urls'

WSGI_APPLICATION = 'charts.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'chartkick',
)
