import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# パブリックIPv4アドレス(EIP)/ パブリックIPv4DNS
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': '',
        'PORT': 3306,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}
