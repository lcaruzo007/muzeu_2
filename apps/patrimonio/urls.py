from django.urls import path
from . import views

app_name = 'patrimonio'

urlpatterns = [
    path('', views.lista_patrimonio, name='lista'),
    path('detalhe/<int:id>/', views.detalhe_patrimonio, name='detalhe'),
    path('ajax/adicionar/', views.ajax_adicionar_patrimonio, name='ajax_adicionar'),
]
