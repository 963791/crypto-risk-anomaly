from .base import *

DEBUG = False
ALLOWED_HOSTS = ["yourdomain.com"]

# Example: PostgreSQL in production
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "yourdbname",
        "USER": "yourdbuser",
        "PASSWORD": "yourpassword",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

