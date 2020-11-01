from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import hashlib

# Create your models here.

# BaseUserManager継承
class CustomStoreManager(BaseUserManager):
  def create_user(self, request_data, **extra_fields):
    """
    メールアドレスとパスワードでStoreユーザーを作成、保存します
    """
    if not request_data['store_email']:
      raise ValueError('Users must have an email address')
    if not request_data['store_name']:
      raise ValueError('Users must have an user name')
    # 渡された文字列をハッシュ化し、ユーザのパスワードに設定します。Userオブジェクトの保存は行いません
    password = make_password(request_data['store_password'])
    store = self.model(
      store_email=self.normalize_email(request_data['store_email']),
      store_name=request_data['store_name'],
      store_password=password,
      **extra_fields
    )
    # 保存する(使う)データベースを教えてる
    store.save(using=self._db)

    # token生成（email, password, timezone）
    tz = timezone.now()
    uniquestr = store.store_email + store.store_password + tz.strftime('%Y%m%d%H%M%S%f')
    hashkey = hashlib.sha256(uniquestr.encode('utf-8')).hexdigest()

    # 生成されたtokenをCustomTokenモデルに保存
    from customtoken.models.customtoken import CustomToken
    token = CustomToken.objects.create(
      store_user_id=store.id,
      key=hashkey,
    )
    return store

# Groupモデルを継承
class Store(Group):
  # @、。、+、-、および_に加えて、Unicode文字を許可するフィールドバリデーター
  storename_validator = UnicodeUsernameValidator()
  store_name = models.CharField(
    verbose_name='store_name',
    max_length=30,
    validators=[storename_validator],
    unique=True
  )
  store_email = models.EmailField(
    verbose_name='store_email address',
    max_length=255,
    unique=True
  )
  store_password = models.CharField(max_length=128, verbose_name='store_password')
  date_joined = models.DateTimeField(verbose_name='date_joined', default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)
  withdrawal_at = models.DateTimeField(null=True, blank=True)
  # 使うマネージャーを指定
  objects = CustomStoreManager()

  def __str__(self):
    return self.store_email
