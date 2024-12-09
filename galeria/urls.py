
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('adicionar/', views.Adiciona, name="adicionar"),
    path('login/', views.recebe_login, name="login"),
    path('cadastro/', views.cadastro, name="cadastro"),
    path('logout/', views.realiza_logout, name="logout"),
    path('colecoes/', views.collections, name="colecoes"),
]