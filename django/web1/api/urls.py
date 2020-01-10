from django.urls import path
from . import views

urlpatterns = [
    path('', views.upper, name="upper"),
    path('select1', views.select1, name="select1"),
    path('insert1', views.insert1, name="insert1"),
]
