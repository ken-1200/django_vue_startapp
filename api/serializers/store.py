from rest_framework import serializers
from store.models.stores import Store, CustomStoreManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash

class StoreSerializer(serializers.ModelSerializer):
  store_password = serializers.CharField(write_only=True, required=False)
  class Meta:
    model = Store
    fields = ['group_ptr_id', 'store_name', 'store_email', 'store_password']

# パスワード更新
  def update(self, instance, validated_data):
    if 'store_password' in validated_data:
      # 更新の場合 make_passwordを使ってpasswordをハッシュ化
      password = validated_data.get('store_password', instance.store_password)
      instance.store_password = make_password(password)
      print('更新しました。')
    else:
      instance.super().update(instance, validated_data)
      print('更新しませんでした。')
    instance.save()
    return instance

# StoreModelで定義したユーザー作成のメソッドを呼ぶ
  def create(self, validated_data):
    return Store.objects.create_user(request_data=validated_data, name=validated_data.get('store_name'))
