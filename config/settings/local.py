from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'income_and_expense',
        'USER': 'inex',
        'PASSWORD': 'inex',
        'HOST': '',
        'PORT': ''
    }
}