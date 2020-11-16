from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import status
from customtoken.models.customtoken import CustomToken

# 認証機能
class CustomAuthentication(authentication.BaseAuthentication):
  def authenticate(self, request):
    # リクエストヘッダーからトークンを取得する
    token_str = request.META.get('HTTP_AUTHORIZATION')
    # print(token_str)
    # print(request.META)
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
