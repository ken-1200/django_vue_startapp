from rest_framework import serializers
from item.models.items import Item

class ItemSerializer(serializers.ModelSerializer):
  # Storeモデルのストア名をとってくる
  store_owner = serializers.ReadOnlyField(source='store_owner.store_name')
  class Meta:
    model = Item
    fields = ['id', 'item_name', 'item_img', 'item_detail', 'item_price', 'item_total', 'store_owner']

