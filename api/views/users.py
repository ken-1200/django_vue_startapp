from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers.user import UserSerializer
from user.models.users import User
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.exceptions import ValidationError

from rest_framework.views import APIView
from django.http.response import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from api.serializers.user_login import UserLoginSerializer
from rest_framework import authentication, permissions, generics
from django.http import HttpResponse, Http404
from api.serializers.user_refresh_token import UserRefreshTokenSerializer
from api.authentication import UserAuthentication
from api.permission import CustomUserPermission

import json

# ログインユーザー情報取得←ここはまだ修正が必要
class LoginUserGetView(generics.GenericAPIView):
  """
  ログインしている状態で自分自身の情報を取得する
  """
  # 認証/権限
  authentication_classes = [UserAuthentication,]
  permission_classes = (CustomUserPermission,)
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def get(self, request, format=None):
    content = {
      'user_name': request.user.user_name,
      'user_email': request.user.user_email,
    }
    return Response(data=content, status=status.HTTP_200_OK)

# アップデート専用(ログインしているユーザー)
class UserUpdateView(generics.UpdateAPIView):
  """
  ログインしている状態で自分自身の情報をupdateする
  """
  # 認証/権限
  authentication_classes = [UserAuthentication,]
  permission_classes = (CustomUserPermission,)
  queryset = User.objects.all()
  serializer_class = UserSerializer
  # 検索キーの指定(デフォルトはid)
  lookup_fields = 'user_email'

  def get_object(self):
    # まずここが読み込まれる 
    # 認証、権限のえられたストアユーザーが入ってきて、その情報をinstanceとして返却
    try:
      instance = self.queryset.get(user_email=self.request.user)
      print(instance)
      return instance
    except User.DoesNotExist:
      raise Http404


# refreshToken
class UserRefreshToken(APIView):
  @swagger_auto_schema(request_body=UserRefreshTokenSerializer(), operation_description="description")
  def post(self, request, format=None):
    try:
      # リクエストデータ読み込み
      refresh_key = request.data.get('key')
    except:
      # Jsonの読み込み失敗
      return JsonResponse({'message': '読み込みに失敗しました。'}, status=400)

    # リフレッシュトークンの整合性チェック
    if not Token.objects.filter(key=refresh_key).exists():
      # 存在しない場合
      return JsonResponse({'message': 'リフレッシュトークンが違います。'}, status=403)
    token = Token.objects.get(key=refresh_key)

    # ユーザー情報取得
    user = User.objects.get(id=token.user_id)

    # リフレッシュトークンを使ってアクセストークンのアクセス日時を更新する
    token.created = timezone.now()
    print('アクセストークンの生成時間を最新に更新しました。')

    response = {
      'user_id': token.user_id,
      'user_name': user.user_name,
      'user_email': user.user_email,
      'access_token': token.key,
      'refresh_token': token.key,
      'expires_in': 3600,
    }
    return Response({'message': 'Success', 'data': response, 'status': 200})

# LoginAPIView-User
class UserLogin(APIView):
  # パーミッション解除
  permission_classes = ()

  @swagger_auto_schema(request_body=UserLoginSerializer, operation_description="description")
  def post(self, request, format=None):
    try:
      # dataの読み込み
      data = json.loads(request.body)
      request_email = data['user_email']
      request_password = data['password']
    except:
      # json読み込み失敗
      return JsonResponse({'message': '読み込みに失敗しました。'}, status=400)
    
    # メールアドレスからユーザー取得
    if not User.objects.filter(user_email=request_email):
      # 存在しない場合
      return JsonResponse({'message': 'メールアドレスが存在しません。'}, status=403)
    user = User.objects.get(user_email=request_email)

    # パスワードチェック
    if not user.check_password(request_password):
      return JsonResponse({'message': 'パスワードが違います。'}, status=403)

    # ユーザーが保持しているトークンを取得
    if Token.objects.filter(user_id=user.id):
      # トークンがある場合は削除
      print('削除します。')
      Token.objects.get(user_id=user.id).delete()
      print('削除しました。')

    # トークン生成 defaultのcreateメソッド
    token = Token.objects.create(user=user)

    print('ログインしました。')

    login_data = {
      'user_id': token.user_id,
      'user_name': user.user_name,
      'user_email': request_email,
      'user_password': request_password,
      'access_token': token.key,
      'refresh_token': token.key,
      'expires_in': 3600,
    }
    return Response({'message': 'Success', 'data': login_data, 'status': 200})

# APIException
class NotFound(APIException):
  status_code = 404
  default_detail = "見つかりませんでした。"
  default_code = "HTTP_404_NOT_FOUND"

# UserViewSet
class UserViewSet(viewsets.ModelViewSet):
  # パーミッション解除
  permission_classes = ()
  queryset = User.objects.all()
  serializer_class = UserSerializer

# create
  @action(detail=False, methods=['post'])
  def create_user(self, request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response({'user': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# delete_endpoint
  @action(detail=True, methods=['delete'])
  def delete_user(self, request, pk=None):
    print('delete_endpoint')
    # user削除 emailだけ残す
    try:
      user_obj = self.get_object()
      user_obj.user_name = ''
      user_obj.user_email = user_obj.user_email
      user_obj.password = ''
      user_obj.withdrawal_at = timezone.now()
      user_obj.save()
      content = {
        'user_name': user_obj.user_name,
        'user_email': user_obj.user_email,
        'password': user_obj.password,
        'withdrawal_at': user_obj.withdrawal_at
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