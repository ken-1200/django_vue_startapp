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
from rest_framework.exceptions import APIException
from django.core import serializers
from django.http import HttpResponse
from api.authentication import UserAuthentication
from api.permission import PaymentPermission
import json

# swagger対応
from drf_yasg.utils import swagger_auto_schema

# APIException
class BadRequest(APIException):
  status_code = 400
  default_detail = "不正なアクセスがありました。"
  default_code = "Bad_Request"

class NotFound(APIException):
  status_code = 404
  default_detail = "見つかりませんでした。"
  default_code = "HTTP_404_NOT_FOUND"

# ModelViewSet
class PaymentViewSet(viewsets.ModelViewSet):
  # 認証/権限
  authentication_classes = [UserAuthentication,]
  permission_classes = (PaymentPermission,)
  queryset = Payment.objects.all()
  serializer_class = PaymentSerializer

  # ユーザーidに紐づいた購入情報を取得する
  @action(detail=False, methods=['get'])
  def get_payment_info(self, request):
    try:
      # Userに紐づいた購入情報
      payment = Payment.objects.order_by('-bought_at').filter(user_email=request.user)
      payment_info = serializers.serialize('json', payment)
    except Exception as err:
      # システム終了以外の全ての組み込み例外
      print(err)
      raise NotFound({
        'NOT_FOUND': [
          NotFound().status_code,
          NotFound().default_detail,
        ]
      })
    return HttpResponse(content=payment_info, content_type="application/json", status=200)


  @action(detail=True, methods=['get'])
  def get_payments(self, request, pk=None):
    # pay_idに紐づく購入情報を取得
    try:
      # pkに紐づく購入情報を取得
      pay_obj = Payment.objects.order_by('-bought_at').filter(pk=pk).first()

      # 購入情報に紐づく購入品詳細を取得
      role_obj = Role.objects.order_by('-pay_id').filter(pay_id_id=pay_obj.id)

      # 購入品詳細をリストで格納
      role_list = []

      # 購入数をリストで格納
      item_quantity = []

      # 購入品詳細を取得
      for role in role_obj:
        # item_idに紐づく商品情報
        item_obj = Item.objects.filter(pk=role.item_id_id)
        item = serializers.serialize('json', item_obj)
        # json→辞書/リスト
        payment_item = json.loads(item)

        # 内容
        role_fields = {
          'pay_id': role.pay_id_id,
          'item_id': role.item_id_id,
          'item': payment_item,
          'item_quantity': role.item_quantity,
        }
        # 購入数（合計）
        item_quantity.append(role.item_quantity)

        # 購入品詳細追加する
        role_list.append(role_fields)

    # ResponseBody
      content = {
        'pay_id': pay_obj.id,
        'role': role_list,
        'pay_totalprice': pay_obj.pay_totalprice,
        'pay_totalquantity': sum(item_quantity),
        'user_email': pay_obj.user_email,
        'bought_at': pay_obj.bought_at
      }
    except Exception as err:
      # システム終了以外の全ての組み込み例外
      print(err)
      raise NotFound({
        'NOT_FOUND': [
          NotFound().status_code,
          NotFound().default_detail,
        ]
      })
    return Response({'message': 'Success', 'data': content, 'status': 200})

# APIView
class PaymentList(APIView):
  """
  List all payments, or create a new payments.
  """
  # パーミッション解除
  permission_classes = ()

  @swagger_auto_schema(request_body=PaymentSerializer(), operation_description="description")
  def post(self, request, format=None):
    serializer = PaymentSerializer(data=request.data)
    # 総数から購入数を引く処理
    if serializer.is_valid(raise_exception=True):
      try:
        for role in request.data['role']:
          item = Item.objects.get(id=role['item_id'])
          item.item_total -= role['item_quantity']
          item.save()
      except Exception as err:
        # システム終了以外の全ての組み込み例外
        print(err)
        raise ValidationError({
          'Bad_Request': [
            BadRequest().status_code,
            BadRequest().default_detail
          ]
        })
      serializer.save()
      return Response({'payments': serializer.data}, status=status.HTTP_201_CREATED)
    return Response({ 'payments': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
