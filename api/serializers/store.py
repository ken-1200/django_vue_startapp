from rest_framework import serializers
from store.models.stores import Store, CustomStoreManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password

class StoreSerializer(serializers.ModelSerializer):
  store_password = serializers.CharField(write_only=True, required=False)
  class Meta:
    model = Store
    fields = ['group_ptr_id', 'store_name', 'store_email', 'store_password']

# パスワード更新
  def update(self, instance, validated_data):
    exist_password = instance.store_password
    valid_password = validated_data.get('store_password', instance.store_password)

    # パスワードチェック
    if check_password(valid_password, exist_password):
      # 同じパスワードの時 既存のデータを返す
      print('既存と同じパスワードです。')
      instance.save()
      return instance

    # 更新の場合 make_passwordを使ってpasswordをハッシュ化
    password = validated_data.get('store_password', instance.store_password)
    instance.store_password = make_password(password)
    instance.save()
    print('パスワード更新しました。')
    return instance

# StoreModelで定義したユーザー作成のメソッドを呼ぶ
  def create(self, validated_data):
    return Store.objects.create_user(request_data=validated_data, name=validated_data.get('store_name'))
