from rest_framework import serializers
from item.models.items import Item

class ItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = Item
    fields = ['id', 'store_id', 'item_name', 'item_img', 'item_detail', 'item_price', 'item_total']

# create
  def create(self, validated_data):
    item = Item(
      store_id=validated_data['store_id'],
      item_name=validated_data['item_name'],
      item_detail=validated_data['item_detail'],
      item_price=validated_data['item_price'],
      item_total=validated_data['item_total'],
    )
    item.save()
    return item

# update-partial_update
  def update(self, instance, validated_data):
    instance.item_name = validated_data.get('item_name', instance.item_name)
    instance.item_img = validated_data.get('item_img', instance.item_img)
    instance.item_detail = validated_data.get('item_detail', instance.item_detail)
    instance.item_price = validated_data.get('item_price', instance.item_price)
    instance.item_total = validated_data.get('item_total', instance.item_total)
    instance.save()
    return instance
