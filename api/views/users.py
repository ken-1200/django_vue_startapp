from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers.user import UserSerializer
from user.models.users import User
from django.utils import timezone
from rest_framework.exceptions import APIException

# APIException
class NotFound(APIException):
  status_code = 404
  default_detail = "見つかりませんでした。"
  default_code = "HTTP_404_NOT_FOUND"

# UserViewSet
class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

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