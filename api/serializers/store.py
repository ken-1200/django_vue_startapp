from rest_framework import serializers
from store.models.stores import Store

class StoreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Store
    fields = ['id', 'store_name', 'store_email', 'store_password', 'withdrawal_datetime']
  
# update-partial_update
  def update(self, instance, validated_data):
    print('update - partial_update')
    instance.store_name = validated_data.get('store_name', instance.store_name)
    instance.store_password = validated_data.get('store_password', instance.store_password)
    instance.save()
    return instance