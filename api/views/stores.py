from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers.store import StoreSerializer
from store.models.stores import Store
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.exceptions import ValidationError

# Create your views here.

# APIException
class NotFound(APIException):
  status_code = 404
  default_detail = "見つかりませんでした。"
  default_code = "HTTP_404_NOT_FOUND"

class BadRequest(APIException):
  status_code = 400
  default_detail = "不正なアクセスがありました。"
  default_code = "Bad_Request"

# StoreViewSetの作成
class StoreViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows stores to be viewed or edited.
  """
  queryset = Store.objects.all()
  serializer_class = StoreSerializer

# create
  @action(detail=False, methods=['post'])
  def create_store(self, request):
    serializer = StoreSerializer(data=request.data)
    # store作成時、同じemailの場合はエラーを返す--レコードの存在をチェックする
    try:
      if Store.objects.filter(store_email=request.data['store_email']).exists():
        return Response({'store': '既に存在するEmailです。'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
      print(err)
      raise ValidationError({
        'Bad_Request': [
          BadRequest().status_code,
          BadRequest().default_detail
        ]
      })
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response({'store': serializer.data}, status=status.HTTP_201_CREATED)
    return Response({'store': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# delete_endpoint
  @action(detail=True, methods=['delete'])
  def delete_store(self, request, pk=None):
    # store削除 emailだけ残す
    try:
      store_obj = self.get_object()
      store_obj.store_name = ''
      store_obj.store_email = store_obj.store_email
      store_obj.store_password = ''
      store_obj.deleted_at = timezone.now()
      store_obj.save()
      content = {
        'store_name': store_obj.store_name,
        'store_email': store_obj.store_email,
        'store_password': store_obj.store_password,
        'deleted_at': store_obj.deleted_at
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
    return Response({'message': 'Success', 'data': content, 'status': 204})