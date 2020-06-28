# -*- coding: utf-8 -*-
import os

# TODO get all these variables from VAULT
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_env_variable("SECRET_KEY")
REDIS_HOST = "redis"
RQ_API_TOKEN = SECRET_KEY
