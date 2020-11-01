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

# Pythonの標準ライブラリのjsonモジュールを使うと
# JSON形式のファイルや文字列をパース（解析）して辞書dictなどのオブジェクトとして読み込める
# JSONに相当するオブジェクトを整形してJSON形式のファイルや文字列として出力・保存することも可能
import json
# swagger対応
from drf_yasg.utils import swagger_auto_schema

# ログインユーザー情報取得
class LoginStoreUserGetView(generics.GenericAPIView):
  # ログインしている状態で自分自身の情報を取得する
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Store.objects.all()
  serializer_class = StoreSerializer

  def get(self, request, format=None):
    return Response(data={
      'store_name': request.store_name,
      'store_email': request.store_email,
    }, status=status.HTTP_200_OK)

# アップデート専用(ログインしているユーザー)
class StoreUserUpdateView(generics.UpdateAPIView):
  permissions_classes = (permissions.IsAuthenticated,)
  queryset = Store.objects.all()
  serializer_class = StoreSerializer
  # 検索キーの指定(デフォルトはid)
  lookup_fields = 'store_email'

  def get_object(self):
    try:
      instance = self.queryset.get(store_email=self.request.user)
      print(instance)
      return instance
    except Store.DoesNotExist:
      raise Http404



# LoginAPIView-Store
class StoreLogin(APIView):
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
    login_data = {
      'store_email': request_email,
      'store_password': request_password,
      'token': token.key
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