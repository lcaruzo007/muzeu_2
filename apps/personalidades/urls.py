from django.urls import path
from . import views

app_name = 'personalidades'

urlpatterns = [
    path('', views.salao_honra, name='salao_honra'),
    path('<int:pk>/', views.personalidade_detail, name='detail'),
]
