from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers.payment import PaymentSerializer
from api.serializers.role import RoleSerializer
from api.serializers.item import ItemSerializer
from payment.models.payments import Payment
from payment.models.roles import Role
from item.models.items import Item
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from drf_yasg.utils import swagger_auto_schema

# APIView
class PaymentList(APIView):
  """
  List all payments, or create a new payments.
  """
  # @swagger_auto_schema(responses={200: PaymentSerializer(many=True)})
  # def get(self, request, format=None):
  #   payments = Payment.objects.all()
  #   serializer = PaymentSerializer(payments, read_only=True, many=True)
  #   return Response({'payments': serializer.data})

  @swagger_auto_schema(request_body=PaymentSerializer(), operation_description="description")
  def post(self, request, format=None):
    serializer = PaymentSerializer(data=request.data)
    # 総数から購入数を引く処理
    try:
      for role in request.data['role']:
        item = Item.objects.get(id=role['item_id'])
        item.item_total -= role['item_quantity']
        item.save()
    except Exception as err:
      # システム終了以外の全ての組み込み例外
      raise ValidationError("商品の在庫が足りていません。", code=err)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response({'payments': serializer.data}, status=status.HTTP_201_CREATED)
    return Response({ 'payments': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# is_valid 関数には、raise_exception=True を与えることで erorrs 情報をラップした ValidationError を投げてくれる機能がついています。
# perform_createはCreateModelMixinから呼び出されて、新しいオブジェクトインスタンスを保存するときに呼び出されるメソッドのようですね。
# serializer.data = {'id': 58, 'item_id': 1, 'pay_totalprice': 10, 'user_email': '', 'withdrawal_datetime': '2020-08-23T20:52:53.157620+09:00'}
# role-item_idとitem_quantity
# roles = serializer.data['role']
# for role in roles:
#   item = Item.objects.get(id=role['item_id'])
#   serializer.data['pay_totalprice'] = item.item_price * role['item_quantity']
#   print(serializer.data['pay_totalprice'])
