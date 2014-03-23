# Django settings for local project.

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = False

ADMINS = ()

ALLOWED_HOSTS = []

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite'),
    }
}

SITE_ID = 1
USE_TZ = True
USE_I18N = True
USE_L10N = True

TIME_ZONE = 'Australia/Sydney'
LANGUAGE_CODE = 'en-us'

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = os.path.join(BASE_DIR, 'static_dist')
STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/stats'
LOGIN_URL = '/login'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Important! Make sure you change this.
# Generate a new one at http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = 'rostergenius%h2yv!bc)7hrl(^=+$86fq=44_o5t1c$0s8bd8*_1jf_!@ri3!'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'middleware.AllowOriginMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'geoposition',
    'rostr',
    'storages',
    'gunicorn',
    'django.contrib.admin',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

APPEND_SLASH = True

try:
    from localsettings import *
    print "Using local settings"
except:
    _DEBUG = DEBUG
    print "Using prod settings"
