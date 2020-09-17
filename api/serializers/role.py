from rest_framework import serializers
from payment.models.roles import Role

# RoleSerializer
class RoleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Role
    fields = ['id', 'item_id', 'item_quantity']
