from django.views.generic import ListView, DetailView
from .models import Noticia

class NoticiaListView(ListView):
    model = Noticia
    template_name = 'noticias/lista.html'
    context_object_name = 'noticias'
    paginate_by = 10
    
    def get_queryset(self):
        return Noticia.objects.filter(status='publicado').order_by('-data_publicacao')

class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = 'noticias/detalhe.html'
    context_object_name = 'noticia'
