import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# パブリックIPv4アドレス(EIP)/ パブリックIPv4DNS/ CNAME プロパティの値
ALLOWED_HOSTS = ['13.230.53.216', 'ec2-13-230-53-216.ap-northeast-1.compute.amazonaws.com', 'App-Django-Vue-dev.ap-northeast-1.elasticbeanstalk.com']

# S3共通の設定(本番)
if 'AWS_ACCESS_KEY_ID' in os.environ:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ebdb',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': 'aa1pjt00ez303v6.colsjxq8adqw.ap-northeast-1.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}
