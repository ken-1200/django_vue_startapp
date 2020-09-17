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

# APIException
class NotFound(APIException):
  status_code = 404
  default_detail = "見つかりませんでした。"
  default_code = "HTTP_404_NOT_FOUND"

class BadRequest(APIException):
  status_code = 400
  default_detail = "不正なアクセスがありました。"
  default_code = "Bad_Request"

# UserViewSet
class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

# create
  @action(detail=False, methods=['post'])
  def create_store(self, request):
    serializer = UserSerializer(data=request.data)
    # user作成時、同じemailの場合はエラーを返す--レコードの存在をチェックする
    try:
      if User.objects.filter(user_email=request.data['user_email']).exists():
        return Response({'user': '既に存在するEmailです。'}, status=status.HTTP_400_BAD_REQUEST)
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
      return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response({'user': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# delete_endpoint
  @action(detail=True, methods=['delete'])
  def delete_user(self, request, pk=None):
    print('delete_endpoint')
    # user削除 emailだけ残す
    try:
      user_obj = self.get_object()
      user_obj.user_email = user_obj.user_email
      user_obj.user_password = ''
      user_obj.withdrawal_at = timezone.now()
      user_obj.save()
      content = {
        'user_email': user_obj.user_email,
        'user_password': user_obj.user_password,
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