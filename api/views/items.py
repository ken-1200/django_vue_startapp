from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers.item import ItemSerializer
from item.models.items import Item
from django.utils import timezone
from rest_framework.exceptions import APIException
from django.core import serializers
from django.http import HttpResponse, Http404
from api.permission import CustomItemPermission
from api.authentication import CustomAuthentication
from rest_framework import permissions, generics
from store.models.stores import Store

# Create your views here.

# 商品一覧
# モデルインスタンスのコレクションを表すための読み取り/書き込みエンドポイントに使用される get/post
class ItemList(generics.ListCreateAPIView):
  """
  アイテム GET(ALL), POST
  """
  queryset = Item.objects.all()
  serializer_class = ItemSerializer
  authentication_classes = [CustomAuthentication,]
  # 認証されたユーザのリクエストは読み書きが可能になり、認証されていないリクエストは読み取りのみ可能
  permission_classes = [CustomItemPermission,]

  # 新しいオブジェクトインスタンスを保存するときに呼び出される
  def perform_create(self, serializer):
    print('認証されたユーザーで商品を作成します。')
    serializer.save(store_owner=self.request.user)

# 商品詳細クラス
# 単一のモデルインスタンスを表すための読み取り-書き込み-削除エンドポイントに使用
class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
  """
  アイテム GET(pk指定), PUT, PATCH, DELETE(レコード削除)
  """
  queryset = Item.objects.all()
  serializer_class = ItemSerializer
  authentication_classes = [CustomAuthentication,]
  # 編集や削除は作成者のみが行える
  permission_classes = [CustomItemPermission, ]

# APIException
class NotFound(APIException):
  status_code = 404
  default_detail = "見つかりませんでした。"
  default_code = "HTTP_404_NOT_FOUND"

# ItemViewSetの作成
class ItemViewSet(viewsets.ModelViewSet):
  """
  アイテム GET(ストアオーナーに紐づいたアイテム一覧), アイテム GET(削除された商品以外全ての一覧), PATCH(item_idに紐づく商品を更新する), DELETE(レコードは残る)
  """
  # パーミッション設定
  # authentication_classesで使用する認証クラスを指定
  # permission_classesにはこのAPIを使用するための権限を設定
  # IsAuthenticatedはauthentication_classesで設定した認証が行えた場合にこのAPIにアクセス可能
  authentication_classes = [CustomAuthentication,]
  permission_classes = [CustomItemPermission,]
  queryset = Item.objects.all()
  serializer_class = ItemSerializer

# ストアオーナーに紐づいたアイテムを取得する
  @action(detail=False, methods=['get'])
  def get_item_detail(self, request):
    try:
      # deleted_at=Noneの商品をJsonにシリアル化
      item = Item.objects.filter(store_owner=request.user.id)
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

# 
  @action(detail=True, methods=['patch'])
  def update_item(self, request, pk=None):
    # 商品がある場合商品を更新する
    if not Item.objects.filter(store_owner=request.user.id):
      # オーナーの商品がない場合
      return Response({'message': 'あなたの商品が存在しません。'}, status=403)

    # リクエストデータを取得する
    try:
      ob = request.data
      item_id = ob['item_id']
      item_name = ob['item_name']
      item_detail = ob['item_detail']
      item_price = ob['item_price']
      item_total = ob['item_total']
      item_img = ob['item_img']
    except:
      return Response({'message': '読み込みに失敗しました。'}, status=400)

    try:
      # 商品アップデート
      item_obj = self.queryset.get(pk=ob['item_id'])
      item_obj.id = item_id
      item_obj.item_name = item_name
      item_obj.item_img = item_img
      item_obj.item_detail = item_detail
      item_obj.item_price = item_price
      item_obj.item_total = item_total
      item_obj.updated_at = timezone.now()
      item_obj.save()

      # レスポンスデータ
      content = {
        'item_id': item_obj.id,
        'item_name': item_obj.item_name,
        'item_detail': item_obj.item_detail,
        'item_price': item_obj.item_price,
        'item_total': item_obj.item_total,
        'updated_at': item_obj.updated_at,
        'item_img': '{item_obj.item_img}'.format(item_obj=item_obj),
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
    return Response({'message': 'Success', 'data': content, 'status': 201})


# 存在する商品(削除されたもの以外全て)List取得
  @action(detail=False, methods=['get'])
  def get_items_list(self, request):
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

# 完全削除はせずに各値に初期値を入れて、削除
  @action(detail=True, methods=['delete'])
  def delete_item(self, request, pk=None):
    # itemボタン押下時に、削除日時に押下時の時間を入れる。
    try:
      item_obj = self.queryset.get(pk=request.data['item_id'])
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
