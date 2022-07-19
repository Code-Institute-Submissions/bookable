""" Production Settings """

import os
from .common import *
import dj_database_url

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = [
    'mt-bookable.herokuapp.com',
]

# if os.path.isfile('dev.py'):
#     import bookable.settings.dev as dev

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
