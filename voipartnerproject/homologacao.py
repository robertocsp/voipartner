from voipartnerproject.base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ebdb',
        'USER': 'voipartner',
        'PASSWORD': 'voipartner',
        'HOST': 'aarscuu9ubkeqe.cwjb2a3zm7nz.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}
