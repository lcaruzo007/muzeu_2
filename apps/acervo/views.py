from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import ItemAcervo, CategoriaAcervo
from apps.exposicoes.models import Exposicao
from apps.noticias.models import Noticia
from apps.eventos.models import Evento
from apps.usuarios.elasticsearch_service import elasticsearch_service

class HomeView(TemplateView):
    template_name = 'acervo/home.html'
    
    def get_context_data(self, **kwargs):
        from apps.arte.models import ObraArte
        from apps.personalidades.models import Personalidade
        from apps.patrimonio.models import Patrimonio

        context = super().get_context_data(**kwargs)
        context['itens_destaque'] = ItemAcervo.objects.filter(ativo=True, disponivel_exposicao=True)[:6]
        context['exposicoes_ativas'] = Exposicao.objects.filter(ativa=True)[:3]
        context['noticias_recentes'] = Noticia.objects.filter(status='publicado')[:4]
        context['proximos_eventos'] = Evento.objects.filter(ativo=True)[:3]
        context['total_itens'] = ItemAcervo.objects.filter(ativo=True).count()
        context['total_obras_arte'] = ObraArte.objects.filter(status='ativo').count() if hasattr(ObraArte, 'status') else ObraArte.objects.count()
        context['total_personalidades'] = Personalidade.objects.filter(ativo=True).count() if hasattr(Personalidade, 'ativo') else Personalidade.objects.count()
        context['total_patrimonios'] = Patrimonio.objects.filter(status='ativo').count() if hasattr(Patrimonio, 'status') else Patrimonio.objects.count()
        context['categorias'] = CategoriaAcervo.objects.annotate(total_itens=Count('itemacervo'))
        return context

class AcervoListView(ListView):
    model = ItemAcervo
    template_name = 'acervo/lista.html'
    context_object_name = 'itens'
    paginate_by = 12
    
    def get_queryset(self):
        return ItemAcervo.objects.filter(ativo=True).select_related('categoria').prefetch_related('fotos')

class AcervoDetailView(DetailView):
    model = ItemAcervo
    template_name = 'acervo/detalhe.html'
    context_object_name = 'item'
    
    def get_queryset(self):
        return ItemAcervo.objects.filter(ativo=True).select_related('categoria').prefetch_related('fotos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Itens relacionados da mesma categoria
        context['itens_relacionados'] = ItemAcervo.objects.filter(
            categoria=self.object.categoria, 
            ativo=True
        ).exclude(pk=self.object.pk)[:4]
        return context

class AcervoPorCategoriaView(ListView):
    model = ItemAcervo
    template_name = 'acervo/categoria.html'
    context_object_name = 'itens'
    paginate_by = 12
    
    def get_queryset(self):
        self.categoria = get_object_or_404(CategoriaAcervo, pk=self.kwargs['categoria_id'])
        return ItemAcervo.objects.filter(categoria=self.categoria, ativo=True).select_related('categoria')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.categoria
        return context

class BuscarAcervoView(TemplateView):
    template_name = 'acervo/buscar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        categoria = self.request.GET.get('categoria', '')
        page = self.request.GET.get('page', 1)
        
        context['query'] = query
        context['categoria_selecionada'] = categoria
        context['categorias'] = CategoriaAcervo.objects.all()
        
        if query:
            # Tentar busca com Elasticsearch primeiro
            if elasticsearch_service.is_available():
                filters = {}
                if categoria:
                    filters['category'] = get_object_or_404(CategoriaAcervo, pk=categoria).nome
                
                try:
                    page_num = int(page)
                    from_ = (page_num - 1) * 12
                except:
                    page_num = 1
                    from_ = 0
                
                results = elasticsearch_service.search(
                    query=query,
                    filters=filters,
                    size=12,
                    from_=from_
                )
                
                # Converter resultados do Elasticsearch
                items_data = []
                for hit in results['hits']['hits']:
                    source = hit['_source']
                    item_id = hit['_id'].split('_')[1]
                    try:
                        item = ItemAcervo.objects.get(pk=item_id)
                        items_data.append({
                            'item': item,
                            'highlight': hit.get('highlight', {})
                        })
                    except ItemAcervo.DoesNotExist:
                        pass
                
                # Simular paginação
                total_results = results['hits']['total']['value']
                total_pages = (total_results + 11) // 12
                
                context['items_data'] = items_data
                context['total_results'] = total_results
                context['current_page'] = page_num
                context['total_pages'] = total_pages
                context['has_previous'] = page_num > 1
                context['has_next'] = page_num < total_pages
                context['using_elasticsearch'] = True
                
            else:
                # Fallback para busca no Django
                queryset = ItemAcervo.objects.filter(ativo=True)
                
                queryset = queryset.filter(
                    Q(titulo__icontains=query) |
                    Q(descricao__icontains=query) |
                    Q(origem__icontains=query) |
                    Q(material__icontains=query)
                )
                
                if categoria:
                    queryset = queryset.filter(categoria_id=categoria)
                
                queryset = queryset.select_related('categoria').distinct()
                
                paginator = Paginator(queryset, 12)
                page_obj = paginator.get_page(page)
                
                context['page_obj'] = page_obj
                context['itens'] = page_obj
                context['total_results'] = paginator.count
                context['using_elasticsearch'] = False
        
        return context


class MusicaView(TemplateView):
    template_name = 'acervo/musica.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscar itens relacionados à música
        # Agora busca todos os itens do acervo com tipo_item='musica'
        context['itens_musica'] = ItemAcervo.objects.filter(
            tipo_item='musica',
            ativo=True
        ).select_related('categoria').prefetch_related('fotos')
        
        # Buscar itens com arquivos de áudio (gravações musicais)
        context['gravacoes_musicais'] = ItemAcervo.objects.filter(
            arquivo_audio__isnull=False,
            ativo=True
        ).exclude(arquivo_audio='').select_related('categoria')[:12]
        
        # Buscar áudios de personalidades (depoimentos musicais)
        from apps.personalidades.models import Personalidade
        context['depoimentos_musicais'] = Personalidade.objects.filter(
            Q(audio_depoimento__isnull=False) & 
            (Q(tipo='musico') | Q(areas_atuacao__nome__icontains='música'))
        ).exclude(audio_depoimento='').distinct()[:6]
        
        # Buscar obras de arte relacionadas à música
        from apps.arte.models import ObraArte
        context['obras_musicais'] = ObraArte.objects.filter(
            Q(titulo__icontains='música') | Q(descricao__icontains='música'),
            status='ativo'
        )[:6]
        
        return context


class LiteraturaView(TemplateView):
    template_name = 'acervo/literatura.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscar itens relacionados à literatura
        literatura_categoria = CategoriaAcervo.objects.filter(nome__icontains='literatura').first()
        if literatura_categoria:
            context['itens_literatura'] = ItemAcervo.objects.filter(
                categoria=literatura_categoria,
                ativo=True
            ).select_related('categoria')[:12]
        else:
            context['itens_literatura'] = ItemAcervo.objects.filter(
                Q(titulo__icontains='literatura') | Q(descricao__icontains='literatura') |
                Q(tipo_item='livro') | Q(tipo_item='documento'),
                ativo=True
            ).select_related('categoria')[:12]
        
        # Buscar personalidades da literatura
        from apps.personalidades.models import Personalidade
        context['personalidades_literatura'] = Personalidade.objects.filter(
            Q(tipo='escritor') | Q(areas_atuacao__nome__icontains='literatura')
        ).distinct()[:6]
        
        # Buscar obras de arte relacionadas à literatura
        from apps.arte.models import ObraArte
        context['obras_literarias'] = ObraArte.objects.filter(
            Q(titulo__icontains='literatura') | Q(descricao__icontains='literatura') |
            Q(titulo__icontains='livro') | Q(descricao__icontains='livro'),
            status='ativo'
        )[:6]
        
        return context
