from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers.user import UserSerializer
from user.models.users import User
from django.utils import timezone

# UserViewSet
class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

# delete_endpoint
  @action(detail=True, methods=['delete'])
  def delete_user(self, request, pk=None):
    print('delete_endpoint')
    user_obj = self.get_object()
    user_obj.user_email = user_obj.user_email
    user_obj.user_password = ''
    user_obj.save()
    content = {'user_email': '{user_obj.user_email}'.format(user_obj=user_obj), 'user_password': '{user_obj.user_password}'.format(user_obj=user_obj)}
    return Response({'message': 'Success', 'data': content, 'status': 204})