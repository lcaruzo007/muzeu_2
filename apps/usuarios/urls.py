from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('contato/', views.contato, name='contato'),
    path('contato/ajax/', views.contato_ajax, name='contato_ajax'),
]
