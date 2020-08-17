from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers.item import ItemSerializer
from item.models.items import Item
from django.utils import timezone

# Create your views here.

# ItemViewSetの作成
class ItemViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows items to be viewed or edited.
  """
  queryset = Item.objects.all()
  serializer_class = ItemSerializer