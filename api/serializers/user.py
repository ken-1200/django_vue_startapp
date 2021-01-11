from rest_framework import serializers
from user.models.users import User, CustomUserManager
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password, make_password

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=False)
  class Meta:
    model = User
    fields = ['id', 'user_name', 'user_email', 'password']

# パスワード更新
  def update(self, instance, validated_data):
    exist_password = instance.password
    valid_password = validated_data.get('password', instance.password)

    # パスワードチェック
    if check_password(valid_password, exist_password):
      # 同じパスワードの時 既存のデータを返す
      print('既存と同じパスワードです。')
      instance.save()
      return instance

    # 更新の場合 make_passwordを使ってpasswordをハッシュ化
    password = validated_data.get('password', instance.password)
    instance.password = make_password(password)
    instance.save()
    print('新しいパスワード更新しました。')
    return instance

# UserModelで定義したユーザー作成のメソッドを呼ぶ
  def create(self, validated_data):
    return User.objects.create_user(request_data=validated_data)