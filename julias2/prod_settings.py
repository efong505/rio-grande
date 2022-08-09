""" Production Settings """
# default: use settings from main settings.py if not overwritten
from .settings import *

import django_heroku


DEBUG = True
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)
# adjust to the URL of your Heroku app
ALLOWED_HOSTS = ['*']

# Activate Django-Heroku.
django_heroku.settings(locals())
