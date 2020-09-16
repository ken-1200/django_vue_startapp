from rest_framework import serializers
from payment.models.payments import Payment
from payment.models.roles import Role
from item.models.items import Item
from api.serializers.role import RoleSerializer

# PaymentSerializer
class PaymentSerializer(serializers.ModelSerializer):
  role = RoleSerializer(many=True)

  class Meta:
    model = Payment
    fields = ['role', 'pay_totalprice', 'user_email']

  def update(self, instance, validated_data):
    instance.id = validated_data.get('id', instance.id)
    instance.pay_totalprice = validated_data.get('pay_totalprice', instance.pay_totalprice)
    instance.user_email = validated_data.get('user_email', instance.user_email)
    instance.withdrawal_datetime = validated_data.get('withdrawal_datetime', instance.withdrawal_datetime)
    return instance

  def create(self, validated_data):
  # Paymentを作成してからRoleを作成する
    items = validated_data.pop('role')
    payment_obj = Payment.objects.create(**validated_data)
    validated_data['role'] = items
    # paymentの中身
    for item in items:
      Role.objects.create(pay_id=payment_obj, **item)
    return validated_data
