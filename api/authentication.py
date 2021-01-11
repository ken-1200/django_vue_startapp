from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import status
from customtoken.models.customtoken import CustomToken
from rest_framework.authtoken.models import Token
from user.models.users import User
from django.utils import timezone

# 経過時間値
from datetime import timedelta

# Store認証機能
class CustomAuthentication(authentication.BaseAuthentication):
  def authenticate(self, request):
    # リクエストヘッダーからトークンを取得する
    token_str = request.META.get('HTTP_AUTHORIZATION')
    # print(token_str)

    if not token_str:
      # リクエストヘッダーにトークンが含まれない場合
      raise exceptions.AuthenticationFailed({'message': 'トークンが不正です。'})

    # トークンを取得する
    token = CustomToken.get(token_str)
    # print(token)
    if token == None:
      # トークンが取得できない場合
      raise exceptions.AuthenticationFailed({'message': 'トークンがありません。'})

    # トークンが取得できた場合は、有効期間をチェックする
    if not token.valid_time_token():
      # 有効期限切れの場合
      raise exceptions.AuthenticationFailed({'message': 'トークンが期限切れです。'})

    # トークンが有効な場合は、アクセス日時を更新
    token.update_token()
    return(token.store_user, None)

# User認証機能
class UserAuthentication(authentication.BaseAuthentication):
  def authenticate(self, request):
    # リクエストヘッダーからトークンを取得する
    token_str = request.META.get('HTTP_AUTHORIZATION')
    # print(token_str)

    if not token_str:
      raise exceptions.AuthenticationFailed({'message': 'トークンが不正です。'})

    # 引数のトークンの文字列が存在するかチェックする
    if Token.objects.filter(key=token_str[7:]).exists():
      # 存在した場合
      token = Token.objects.get(key=token_str[7:])
    else:
      # トークンが取得できない場合
      raise exceptions.AuthenticationFailed({'message': 'トークンがありません。'})

    # 有効期間をチェックする
    if not UserAuthentication.valid_time_token(token):
      # 有効期限切れの場合
      raise exceptions.AuthenticationFailed({'message': 'トークンが期限切れです。'})

    # トークンが有効な場合は、アクセス日時を更新
    UserAuthentication.update_token(token)
    return (token.user, None)

# 有効時間60分
  def valid_time_token(self):
    # 経過時間60分 < 今の時間 - トークン生成時の時間
    validtime = timedelta(minutes=60)
    if (validtime < timezone.now() - self.created):
      # 60分以上の場合
      print('トークンで有効期限切れです。')
      return False
    else:
      # 60分以下の場合
      print('トークンが有効期限内です。')
      return True

# トークン生成時間を最新に更新する
  def update_token(self):
    # 現在日時で更新する
    self.created = timezone.now()
    print('アクセストークンの生成時間を最新に更新しました。')
    self.save()
