from django.shortcuts import render
from django.http import HttpResponse
from .models import Item
# from .serializers import ItemSerializer

# Create your views here.

def upper(request):
    if request.method == "GET":
        return HttpResponse("how to use only upper domain")
    if request.method == "POST":
        pass

def select1(request):
    if request.method == "GET":
        return HttpResponse("{'id':'abc'}")
    if request.method == "POST":
        pass

def insert1(request): # 임시
    if request.method == "GET":
        # for i in range(30):
        #     obj = Item()
        #     obj.name = '티비'+str(i)
        #     obj.price = 4000+i
        #     obj.save()
        return HttpResponse("insert1")
    if request.method == "POST":
        pass
    