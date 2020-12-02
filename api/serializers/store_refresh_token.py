from rest_framework import serializers
from customtoken.models.customtoken import CustomToken

class StoreRefreshTokenSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomToken
    fields = ['refresh_key']
