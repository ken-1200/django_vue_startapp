from rest_framework import serializers
from user.models.users import User, CustomUserManager
from django.contrib.auth import update_session_auth_hash

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=False)
  class Meta:
    model = User
    fields = ['id', 'user_name', 'user_email', 'password']

# パスワード更新
  def update(self, instance, validated_data):
    if 'password' in validated_data:
      # 更新の場合 set_passwordでハッシュ化
      instance.set_password(validated_data['password'])
      print('更新しました。')
    else:
      # 親クラス(defaultのupdateメソッド)を使う
      instance.super().update(instance, validated_data)
      print('更新しませんでした。')
    instance.save()
    return instance

# UserModelで定義したユーザー作成のメソッドを呼ぶ
  def create(self, validated_data):
    return User.objects.create_user(request_data=validated_data)