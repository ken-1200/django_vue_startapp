from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from rest_framework.authtoken.models import Token

# 既存UserManegerを継承
class CustomUserManager(BaseUserManager):
  def create_user(self, request_data, **extra_fields):
    """
    メールアドレスとパスワードでユーザーを作成、保存します
    """
    # メールアドレス、ユーザー名の識別
    if not request_data['user_email']:
      raise ValueError('Users must have an email address')
    if not request_data['user_name']:
      raise ValueError('Users must have an user name')
    # User作成
    user = self.model(
      user_email=self.normalize_email(request_data['user_email']),
      user_name=request_data['user_name'],
      **extra_fields
    )
    # 渡された文字列をハッシュ化し、ユーザのパスワードに設定します。Userオブジェクトの保存は行いません
    user.set_password(request_data['password'])
    # 保存する(使う)データベースを教えてる
    user.save(using=self._db)

    # トークンの生成 Tokenモデルに保存
    token = Token.objects.create(user=user)
    return user

# 既存Userモデルを継承
class User(AbstractBaseUser, PermissionsMixin):
  # カラム定義
  # @、。、+、-、および_に加えて、Unicode文字を許可するフィールドバリデーター
  username_validator = UnicodeUsernameValidator()
  user_name = models.CharField(
    verbose_name='user_name',
    max_length=30,
    validators=[username_validator],
    unique=True
  )
  user_email = models.EmailField(
    verbose_name='user_email address',
    max_length=255,
    unique=True
  )
  date_joined = models.DateTimeField(verbose_name='date_joined', default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)
  withdrawal_at = models.DateTimeField(null=True, blank=True)
  is_superuser = None

  objects = CustomUserManager()

  EMAIL_FIELD = 'user_email'
  USERNAME_FIELD = 'user_name'
  REQUIRED_FIELDS = ['user_email']

  def __str__(self):
    return self.user_email
