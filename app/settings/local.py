import os
import environ
from .base import *

# settings.pyの位置を起点として３つ上の親ディレクトリを参照
BASE_DIR = environ.Path(__file__) - 3

env = environ.Env()

# 環境変数でDJANGO_READ_ENV_FILEをTrueにしておくと.envを読んでくれる
READ_ENV_FILE = env.bool('DJANGO_READ_ENV_FILE', default=True)
if READ_ENV_FILE:
    env_file = str(BASE_DIR.path('.env'))
    env.read_env(env_file)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# S3共通の設定(開発)
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

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
