from rest_framework import serializers
from user.models.users import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'user_email', 'user_password', 'withdrawal_datetime']

# update-partial_update
  def update(self, instance, validated_data):
    print('update - partial_update')
    instance.user_password = validated_data.get('user_password', instance.user_password)
    instance.save()
    return instance