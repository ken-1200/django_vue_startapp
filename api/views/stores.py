from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers.store import StoreSerializer
from store.models.stores import Store
from django.utils import timezone

# Create your views here.

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
    print('delete_endpoint')
    store_obj = self.get_object()
    store_obj.store_name = ''
    store_obj.store_email = store_obj.store_email
    store_obj.store_password = ''
    store_obj.save()
    content = {'store_name': '{store_obj.store_name}'.format(store_obj=store_obj), 'store_email': '{store_obj.store_email}'.format(store_obj=store_obj), 'store_password': '{store_obj.store_password}'.format(store_obj=store_obj)}
    return Response({'message': 'Success', 'data': content, 'status': 204})