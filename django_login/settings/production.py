#
#   Production settings
#

from .base import *

import os
import dj_database_url

ALLOWED_HOSTS = ['*']

env = os.environ.copy()
SECRET_KEY = env['SECRET_KEY']

DEBUG = False

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# email settings
EMAIL_HOST = env['EMAIL_HOST']
EMAIL_PORT = env['EMAIL_PORT']
EMAIL_HOST_USER = env['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = env['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env['DEFAULT_FROM_EMAIL'] # e.g 'Admin <noreply@example.com>'