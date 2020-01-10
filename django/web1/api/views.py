from django.shortcuts import render
from django.http import HttpResponse
from .models import Item
from .serializers import ItemSerializer
from rest_framework.renderers import JSONRenderer
import json

# Create your views here.

def upper(request):
    if request.method == "GET":
        return HttpResponse("how to use only upper domain")
        
# {"id":"a"}
def select1(request):
    if request.method == "GET":
        key = request.GET.get("key", "")
        no = request.GET.get("no", 1)

        if key == "abc":
            obj = Item.objects.get(no=no)
            serializer = ItemSerializer(obj)
            data = JSONRenderer().render(serializer.data)
            return HttpResponse(data)
        else:
            data = json.dumps({"ret":"key error"})
            return HttpResponse(data)
            
# [{"id":"a"}, {"id":"b"}, ...]
def select2(request):
    if request.method == "GET":
        key = request.GET.get("key", "")
        data = json.dumps({"ret":"key error"})
        search = 1

        if key == "all":
            obj = Item.objects.all()
            serializer = ItemSerializer(obj, many=True)
            data = JSONRenderer().render(serializer.data)

        return HttpResponse(data)

# sql = """
#     SELECT * FROM API_ITEM WHERE NAME LIKE '%%SEARCH%%'
# """
# rows = Table2.objects.raw(sql)[page_start:page_end]
# cnt = Table2.objects.filter(name__contains=txt).count()

def select3(request):
    if request.method == "GET":
        key = request.GET.get("key", "")
        num = int(request.GET.get("num", 1))
        search = request.GET.get("search", "")

        data = json.dumps({"ret":"key error"})

        if key == "abc":
            obj = Item.objects.filter(name__contains=str(search))[0:num]
            serializer = ItemSerializer(obj, many=True)
            data = JSONRenderer().render(serializer.data)
        return HttpResponse(data)
        

def insert1(request): # 대충 만든 insert
    if request.method == "GET":
        # for i in range(30):
        #     obj = Item()
        #     obj.name = '티비'+str(i)
        #     obj.price = 4000+i
        #     obj.save()
        return HttpResponse("insert1")
        
    