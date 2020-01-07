from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name="index"),
    path('join', views.join, name="join"),
    path('list', views.list, name="list"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('edit', views.edit, name="edit"),
    path('delete', views.delete, name="delete"),
    path('join1', views.join1, name="join1"),

    path('auth_join', views.auth_join, name="auth_join"),
    path('auth_index', views.auth_index, name="auth_index"),
    path('auth_login', views.auth_login, name="auth_login"),
    path('auth_logout', views.auth_logout, name="auth_logout"),
    path('auth_edit', views.auth_edit, name="auth_edit"),
    path('auth_pw', views.auth_pw, name="auth_pw"),
]

