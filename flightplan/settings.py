"""
Django settings for flightplan project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd2n&4i1inyw#bmf_$efysfbr28*)2p+f=zt!u47-=ip1$4w(+q'

ON_HEROKU = True if 'DATABASE_URL' in os.environ else False

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if ON_HEROKU else True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'diverts.herokuapp.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'diverts',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'flightplan.urls'

WSGI_APPLICATION = 'flightplan.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# This if/else prevents loading the .gitignored private file if on Heroku.

LOCAL_DB = 'postgres://postgres:test@localhost:5433/flightplan'
DATABASES = {'default': dj_database_url.config(default=LOCAL_DB)}

# For connecting to Heroku's database from a local machine.
# if ON_HEROKU:
#     DATABASES = {'default': dj_database_url.config()}
# else:
#     import squadron.private as private
#     DATABASES = {'default': dj_database_url.config(default=private.HEROKU_DB_URL)}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

ADMINS = (('David', 'david.alan.oconnor@gmail.com'),)
MANAGERS = ADMINS
