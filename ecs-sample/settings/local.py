from .base import *
from .secrets import *

DEBUG = True

################################################################
# COMMON BLOCK FOR ENV FILE
################################################################
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        from django.core.exceptions import ImproperlyConfigured

        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)


ENV = get_env_variable("ENV")

ALLOWED_HOSTS = ["*"]

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": f"sample",  # TODO add branch name or etc for different fixture
#         "USER": "admin",
#         "PASSWORD": DB_PASSWORD,
#         "HOST": DB_HOST,  # Or an IP Address that your DB is hosted on
#         "PORT": "3306",
#         "CONN_MAX_AGE": 60 * 5,
#         "OPTIONS": {
#             "init_command": "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1, read_rnd_buffer_size=256000",
#             "charset": "utf8mb4",
#         },
#         "TEST": {"CHARSET": "utf8mb4", "COLLATION": "utf8mb4_unicode_ci"},
#     }
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTION": True,  # needed for redis is only cache
            "PARSER_CLASS": "redis.connection.HiredisParser",
        },

    },
    "async": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PARSER_CLASS": "redis.connection.HiredisParser",
        },
        "URL": os.getenv("REDISTOGO_URL", f"redis://{REDIS_HOST}:6379"),  # If you're
    }
}

RQ_QUEUES = {
    "async": {
        "USE_REDIS_CACHE": "async",
        "URL": os.getenv("REDISTOGO_URL", f"redis://{REDIS_HOST}:6379"),
    }
}