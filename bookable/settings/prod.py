""" Production Settings """

import os
import dj_database_url
from common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = [
    'mt-bookable.herokuapp.com',
]

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
