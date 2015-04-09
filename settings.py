from unipath import Path

PROJECT_DIR = Path(__file__).parent

from decouple import config

import dj_database_url

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'))
}

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'grappelli',
    'django.contrib.admin',
    'south',
    'eztables',
    'djangojs',
    'vulnDB.vulns',
    'vulnDB.projects',
    'vulnDB.search',
    'vulnDB.activities',
    'vulnDB.auth',
    'vulnDB.core',
    'vulnDB.feeds',
    'vulnDB.messages',
    'vulnDB.reports',
    'ckeditor',
    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'vulnDB.urls'

WSGI_APPLICATION = 'vulnDB.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = "Europe/Paris"

USE_TZ = True

LANGUAGES = (
    ('fr', 'French'),
    ('en', 'English'),
)

# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SESSION_COOKIES_AGE = 60*15


LOCALE_PATHS = (PROJECT_DIR.child('locale'), )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = PROJECT_DIR.parent.child('staticfiles')
STATIC_URL = '/static/'


STATICFILES_DIRS = (
    PROJECT_DIR.child('static'),
)
STATIC_DIRS = STATICFILES_DIRS

REPORTS_ROOT = PROJECT_DIR.parent.child('media') + '/reports/'

ROOT = PROJECT_DIR.parent.child('')


MEDIA_ROOT = PROJECT_DIR.parent.child('media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

#CRISPY_TEMPLATE_PACK = 'foundation'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/feeds/'

ALLOWED_SIGNUP_DOMAINS = ['*']

FILE_UPLOAD_TEMP_DIR = '/tmp/'
FILE_UPLOAD_PERMISSIONS = 0644


#Django dubug toolbar IP LIST
INTERNAL_IPS = ('192.168.1.200')

#CKEDITOR
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = 'pillow'

#CKEDITOR CONFIG PROFILE

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'width': '100%',
    },

    'vuln_description': {
        'width': '100%',
        'toolbar': 'Advanced',
    },
    'vuln_recommendation': {
        'width': '100%',
        'height': '80',
        'toolbar': 'Basic',
    },
}


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)


