from django.urls import path
from . import views

app_name = 'acervo'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('acervo/', views.AcervoListView.as_view(), name='lista'),
    path('acervo/<int:pk>/', views.AcervoDetailView.as_view(), name='detalhe'),
    path('categoria/<int:categoria_id>/', views.AcervoPorCategoriaView.as_view(), name='por_categoria'),
    path('buscar/', views.BuscarAcervoView.as_view(), name='buscar'),
    path('musica/', views.MusicaView.as_view(), name='musica'),
    path('literatura/', views.LiteraturaView.as_view(), name='literatura'),
]
