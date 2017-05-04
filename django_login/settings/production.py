#
#   Production settings
#

from .base import *

import os

env = os.environ.copy()
SECRET_KEY = env['SECRET_KEY']

DEBUG = False

EMAIL_HOST = env['EMAIL_HOST']
EMAIL_PORT = env['EMAIL_PORT']
EMAIL_HOST_USER = env['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = env['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env['DEFAULT_FROM_EMAIL'] # e.g 'Admin <noreply@example.com>'