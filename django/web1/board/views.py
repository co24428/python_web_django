from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#SQLite 연결
from django.db import connection
cursor = connection.cursor()

@csrf_exempt
def write(request):
    if request.method=='GET':
        return render(request, 'board/write.html')
    if request.method=='POST':
        pass