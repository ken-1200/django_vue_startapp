from rest_framework import serializers
from store.models.stores import Store

class StoreSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Store
    fields = ['id', 'store_name', 'store_email', 'store_password', 'withdrawal_datetime']