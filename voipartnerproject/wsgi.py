"""
WSGI config for voipartnerproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

django_settings_module = os.environ['DJANGO_SETTINGS_MODULE']
os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_settings_module)

application = get_wsgi_application()
