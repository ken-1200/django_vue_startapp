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
from rest_framework.views import APIView
from customtoken.models.customtoken import CustomToken
from api.serializers.store_login import StoreLoginSerializer
from django.http.response import JsonResponse
from django.contrib.auth.hashers import check_password
from rest_framework import authentication, permissions, generics
from django.http import HttpResponse, Http404
from item.models.items import Item
from api.serializers.item import ItemSerializer
from api.permission import CustomItemPermission, CustomStorePermission
from api.authentication import CustomAuthentication
from api.serializers.store_refresh_token import StoreRefreshTokenSerializer

# Pythonの標準ライブラリのjsonモジュールを使うと
# JSON形式のファイルや文字列をパース（解析）して辞書dictなどのオブジェクトとして読み込める
# JSONに相当するオブジェクトを整形してJSON形式のファイルや文字列として出力・保存することも可能
import json
# swagger対応
from drf_yasg.utils import swagger_auto_schema

# ログインユーザー情報取得
class LoginStoreUserGetView(generics.GenericAPIView):
  """
  ログインしている状態で自分自身の情報を取得する
  """
  authentication_classes = [CustomAuthentication,]
  permission_classes = (CustomStorePermission,)
  queryset = Store.objects.all()
  serializer_class = StoreSerializer

  def get(self, request, format=None):
    content = {
      'store_name': request.user.store_name,
      'store_email': request.user.store_email,
    }
    return Response(data=content, status=status.HTTP_200_OK)

# アップデート専用(ログインしているユーザー)
class StoreUserUpdateView(generics.UpdateAPIView):
  """
  ログインしている状態で自分自身の情報をupdateする
  """
  authentication_classes = [CustomAuthentication,]
  permissions_classes = (CustomStorePermission,)
  queryset = Store.objects.all()
  serializer_class = StoreSerializer
  # 検索キーの指定(デフォルトはid)
  lookup_fields = 'store_email'

  def get_object(self):
    # まずここが読み込まれる 認証、権限のえられたストアユーザーが入ってきて、その情報をinstanceとして返却
    try:
      instance = self.queryset.get(store_email=self.request.user)
      return instance
    except Store.DoesNotExist:
      raise Http404

# refreshToken
class StoreRefreshToken(APIView):
  @swagger_auto_schema(request_body=StoreRefreshTokenSerializer(), operation_description="description")
  def post(self, request, format=None):
    try:
      # リクエストデータ読み込み
      refresh_key = request.data.get('refresh_key')
    except:
      # Jsonの読み込み失敗
      return JsonResponse({'message': '読み込みに失敗しました。'}, status=400)

    # リフレッシュトークンの整合性チェック
    if not CustomToken.objects.filter(refresh_key=refresh_key).exists():
      # 存在しない場合
      return JsonResponse({'message': 'リフレッシュトークンが違います。'}, status=403)
    customtoken = CustomToken.objects.get(refresh_key=refresh_key)
    # リフレッシュトークンを使ってアクセストークンのアクセス日時を更新する
    customtoken.update_token()

    response = {
      'store_user_id': customtoken.store_user_id,
      'access_token': customtoken.key,
      'refresh_token': customtoken.refresh_key,
      'expires_in': customtoken.expires_in,
    }
    return Response({'message': 'Success', 'data': response, 'status': 200})


# LoginAPIView-Store
class StoreLogin(APIView):
  # パーミッション解除
  permission_classes = ()

  @swagger_auto_schema(request_body=StoreLoginSerializer(), operation_description="description")
  def post(self, request, format=None):
    try:
      # リクエストボディのJSONを読み込み、メールアドレス、パスワードを取得
      data = json.loads(request.body)
      request_email = data['store_email']
      request_password = data['store_password']
    except:
      # Jsonの読み込み失敗
      return JsonResponse({'message': '読み込みに失敗しました。'}, status=400)

    # メールアドレスからユーザー取得
    if not Store.objects.filter(store_email=request_email).exists():
      # 存在しない場合
      return JsonResponse({'message': 'メールアドレスが存在しません。'}, status=403)
    store = Store.objects.get(store_email=request_email)
    # 登録されているハッシュ化されているパスワードを取得
    encoded = store.store_password

    # パスワードチェック
    if not check_password(request_password, encoded):
      # パスワードエラー
      return JsonResponse({'message': 'パスワードが違います。'}, status=403)
    # tokenの生成 createメソッドを呼ぶ
    token = CustomToken.create(store)

    print('ログインしました。')

    # レスポンス情報
    login_data = {
      'store_id': token.store_user_id,
      'store_email': request_email,
      'store_password': request_password,
      'access_token': token.key,
      'refresh_token': token.refresh_key,
      'expires_in': token.expires_in,
    }
    return Response({'message': 'Success', 'data': login_data, 'status': 200})

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
  # パーミッション解除
  permission_classes = ()
  queryset = Store.objects.all()
  serializer_class = StoreSerializer

# create
  @action(detail=False, methods=['post'])
  def create_store(self, request):
    serializer = StoreSerializer(data=request.data)
    # store作成時、同じemailの場合はエラーを返す--レコードの存在をチェックする
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
      store_obj.withdrawal_at = timezone.now()
      store_obj.save()
      content = {
        'store_name': store_obj.store_name,
        'store_email': store_obj.store_email,
        'store_password': store_obj.store_password,
        'withdrawal_at': store_obj.withdrawal_at
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