from rest_framework import serializers
from store.models.stores import Store

class StoreLoginSerializer(serializers.ModelSerializer):
  store_password = serializers.CharField(write_only=True, required=False)
  class Meta:
    model = Store
    fields = ['group_ptr_id', 'store_email', 'store_password']

