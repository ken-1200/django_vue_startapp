import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4l3g)^t=9sk6lcp(n(_13q22&+k_+1o(sl2lk9ljs(!1-j5_cx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['MYSQL_DATABASE'],
        'USER': os.environ['MYSQL_USER'],
        'PASSWORD': os.environ['MYSQL_PASSWORD'],
        'HOST': 'db',
        'PORT': os.environ['MYSQL_PORT'],
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}
