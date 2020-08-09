from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse
from api.serializers.store import StoreSerializer
from store.models.stores import Store
from django.utils import timezone

# Create your views here.

# StoreViewSetの作成
class StoreViewSet(viewsets.ModelViewSet):
  queryset = Store.objects.all()
  serializer_class = StoreSerializer

# post override
def post(self, request, *arg, **kwargs):
  store_name = request.data['store_name']
  store_email = request.data['store_email']
  store_password = request.data['store_password']
  return HttpResponse({ 'message' : 'New Store Created'}, status=200)
