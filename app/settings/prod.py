import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# パブリックIPv4アドレス(EIP)/ パブリックIPv4DNS
ALLOWED_HOSTS = ['54.95.222.39', 'ec2-54-95-222-39.ap-northeast-1.compute.amazonaws.com', 'django-vue-startapp-dev.ap-northeast-1.elasticbeanstalk.com']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': 'prd-rds.colsjxq8adqw.ap-northeast-1.rds.amazonaws.com',
        'PORT': 3306,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}
