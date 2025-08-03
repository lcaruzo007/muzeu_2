from django.urls import path
from . import views

app_name = 'arte'

urlpatterns = [
    path('', views.galeria_arte, name='galeria'),
    path('obra/<int:pk>/', views.obra_detail, name='obra_detail'),
    path('exposicoes/', views.exposicoes, name='exposicoes'),
    path('exposicao/<int:pk>/', views.exposicao_detail, name='exposicao_detail'),
    path('artista/<int:pk>/', views.artista_detail, name='artista_detail'),
]
