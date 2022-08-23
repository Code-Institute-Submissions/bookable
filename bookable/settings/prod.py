""" Production Settings """
import os
import dj_database_url
from .common import *

DEBUG = False

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'SAMEORIGIN'

SECRET_KEY = os.environ['SECRET_KEY']

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

ALLOWED_HOSTS = [
    'mt-bookable.herokuapp.com',
]

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
