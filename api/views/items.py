from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers.item import ItemSerializer
from item.models.items import Item
from django.utils import timezone
from rest_framework.exceptions import APIException
from django.core import serializers
from django.http import HttpResponse

# Create your views here.

# APIException
class NotFound(APIException):
  status_code = 404
  default_detail = "見つかりませんでした。"
  default_code = "HTTP_404_NOT_FOUND"

# ItemViewSetの作成
class ItemViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows items to be viewed or edited.
  """
  # パーミッション解除
  permission_classes = ()
  queryset = Item.objects.all()
  serializer_class = ItemSerializer

# 存在する商品List取得
  @action(detail=False, methods=['get'])
  def get_items(self, request):
    try:
      # deleted_at=Noneの商品をJsonにシリアル化
      item = Item.objects.filter(deleted_at=None)
      item_list = serializers.serialize('json', item)
    except Exception as err:
      # システム終了以外の全ての組み込み例外
      print(err)
      raise NotFound({
        'NOT_FOUND': [
          NotFound().status_code,
          NotFound().default_detail,
        ]
      })
    return HttpResponse(content=item_list, content_type="application/json", status=200)

# delete_endpoint
  @action(detail=True, methods=['delete'])
  def delete_item(self, request, pk=None):
    # itemボタン押下時に、削除日時に押下時の時間を入れる。
    try:
      item_obj = self.get_object()
      item_obj.item_name = ''
      item_obj.item_img = ''
      item_obj.item_detail = ''
      item_obj.item_price = 0
      item_obj.item_total = 0
      item_obj.deleted_at = timezone.now()
      item_obj.save()
      content = {
        'item_name': item_obj.item_name,
        'item_img': '{item_obj.item_img}'.format(item_obj=item_obj),
        'item_detail': item_obj.item_detail,
        'item_price': item_obj.item_price,
        'item_total': item_obj.item_total,
        'deleted_at': item_obj.deleted_at
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
