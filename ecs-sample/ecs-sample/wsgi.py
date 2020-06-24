"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
ENV = os.environ.get("ENV", "dev")
if ENV in ["beta", "prod"]:
    settings = f"ecs-sample.settings_{ENV}"
else:
    settings = "ecs-sample.settings"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecs-sample.settings')

application = get_wsgi_application()
