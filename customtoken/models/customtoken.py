from django.db import models
from store.models.stores import Store
from django.utils import timezone
# このモジュールは、セキュアハッシュやメッセージダイジェスト用のさまざまなアルゴリズムを実装したもの
import hashlib

# Storeモデル専用のカスタムトークン
class CustomToken(models.Model):
  store_user = models.ForeignKey(Store, on_delete=models.CASCADE)
  key = models.CharField(max_length=64, null=False)
  created = models.DateTimeField(auto_now_add=True, null=True)

  def __str__(self):
    return self.store_user

# tokencreate関数（静的メソッド）
  @staticmethod
  def create(store: Store):
    # ユーザーが保持しているトークンを取得
    if CustomToken.objects.filter(store_user_id=store.id).exists():
      # tokenがある場合は削除
      print('削除します')
      CustomToken.objects.get(store_user_id=store.id).delete()
      print('削除しました')
    
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
      created=tz
    )
    return token
