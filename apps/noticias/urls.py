from django.urls import path
from . import views

app_name = 'noticias'

urlpatterns = [
    path('', views.NoticiaListView.as_view(), name='lista'),
    path('<int:pk>/', views.NoticiaDetailView.as_view(), name='detalhe'),
]
