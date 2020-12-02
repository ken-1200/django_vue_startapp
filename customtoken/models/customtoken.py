from django.db import models
from store.models.stores import Store
from django.utils import timezone
# このモジュールは、セキュアハッシュやメッセージダイジェスト用のさまざまなアルゴリズムを実装したもの
import hashlib

# 経過時間値
from datetime import timedelta

# Storeモデル専用のカスタムトークン
class CustomToken(models.Model):
  store_user = models.ForeignKey(Store, on_delete=models.CASCADE)
  key = models.CharField(max_length=64, null=False)
  refresh_key = models.CharField(max_length=64, null=False)
  expires_in = models.IntegerField(null=False, blank=False, default=3600)
  created = models.DateTimeField(auto_now_add=True, null=True)

  def __str__(self):
    return self.store_user

  """
  トークン生成用のメソッド
  """
# tokencreate関数（静的メソッド）
  @staticmethod
  def create(store: Store):
    # ユーザーが保持しているトークンを取得
    if CustomToken.objects.filter(store_user_id=store.id).exists():
      # tokenがある場合は削除
      print('削除します。')
      CustomToken.objects.get(store_user_id=store.id).delete()
      print('削除しました。')
    
    # token生成（email, password, timezone）
    tz = timezone.now()
    # strftime関数は、引数で指定された書式文字列に従い、日付を表現する文字列を返す
    unique_str = store.store_email + store.store_password + tz.strftime('%Y%m%d%H%M%S%f')
    # メソッドに渡されたデータのダイジェスト値を16進形式文字列で返す 電子メールなどの非バイナリ環境で値を交換する場合に便利
    hashkey = hashlib.sha256(unique_str.encode('utf-8')).hexdigest()

    # tokenをCustomTokenモデルに保存
    token = CustomToken.objects.create(
      store_user_id=store.id,
      key=hashkey,
      refresh_key=hashkey,
      created=tz
    )
    return token

  """
  認証用のメソッドを用意
  """
# トークンを取得するメソッド
  @staticmethod
  def get(token_str: str):
    # 引数のトークンの文字列が存在するかチェックする
    if CustomToken.objects.filter(key=token_str[7:]).exists():
      # 存在した場合
      return CustomToken.objects.get(key=token_str[7:])
    else:
      # 存在しない場合
      return None

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
