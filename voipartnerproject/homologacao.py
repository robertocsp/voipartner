from voipartnerproject.base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'voipartner',
        'USER': 'voipartner',
        'PASSWORD': 'voipartner',
        'HOST': 'voipartner.cwjb2a3zm7nz.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}
