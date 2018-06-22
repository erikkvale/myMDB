from django.core.exceptions import ImproperlyConfigured
from .base_settings import *

DEBUG = False

if SECRET_KEY is None:
    raise ImproperlyConfigured(
        "Please provide a DJANGO_SECRET_KEY "
        "environment variable with a value")

ALLOWED_HOSTS += [
    os.getenv('DJANGO_ALLOWED_HOSTS'),
]