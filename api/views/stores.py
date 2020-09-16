from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers.store import StoreSerializer
from store.models.stores import Store
from django.utils import timezone
from rest_framework.exceptions import APIException

# Create your views here.

# APIException
class NotFound(APIException):
  status_code = 404
  default_detail = "見つかりませんでした。"
  default_code = "HTTP_404_NOT_FOUND"

# StoreViewSetの作成
class StoreViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows stores to be viewed or edited.
  """
  queryset = Store.objects.all()
  serializer_class = StoreSerializer

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