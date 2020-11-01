from rest_framework import serializers
from user.models.users import User

class UserLoginSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=False)
  class Meta:
    model = User
    fields = ['id', 'user_email', 'password']
