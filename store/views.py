from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# store
def store(request):
  return HttpResponse('hi ken!')