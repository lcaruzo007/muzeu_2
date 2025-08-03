from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import ObraArte, ExposicaoArte, Artista, TecnicaArtistica


def galeria_arte(request):
    """View principal da galeria de arte"""
    # Filtros
    tecnica_filtro = request.GET.get('tecnica')
    artista_filtro = request.GET.get('artista')
    busca = request.GET.get('busca')
    
    # Query base
    obras = ObraArte.objects.filter(status='ativo').select_related('artista', 'tecnica')
    
    # Aplicar filtros
    if tecnica_filtro:
        obras = obras.filter(tecnica__id=tecnica_filtro)
    
    if artista_filtro:
        obras = obras.filter(artista__id=artista_filtro)
    
    if busca:
        obras = obras.filter(
            Q(titulo__icontains=busca) | 
            Q(artista__nome__icontains=busca) |
            Q(descricao__icontains=busca)
        )
    
    # Paginação
    paginator = Paginator(obras, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Dados para filtros
    tecnicas = TecnicaArtistica.objects.all().order_by('nome')
    artistas = Artista.objects.filter(status='ativo').order_by('nome')
    
    # Exposições ativas (em andamento ou futuras)
    agora = timezone.now().date()
    exposicoes = ExposicaoArte.objects.filter(
        status='ativo',
        data_fim__gte=agora
    ).order_by('-data_inicio')

    context = {
        'obras': page_obj,
        'tecnicas': tecnicas,
        'artistas': artistas,
        'tecnica_selecionada': tecnica_filtro,
        'artista_selecionado': artista_filtro,
        'busca': busca,
        'total_obras': obras.count(),
        'exposicoes': exposicoes
    }
    
    return render(request, 'arte/galeria.html', context)


def obra_detail(request, pk):
    """View de detalhes de uma obra de arte"""
    obra = get_object_or_404(
        ObraArte.objects.select_related('artista', 'tecnica'), 
        pk=pk, 
        status='ativo'
    )
    
    # Outras obras do mesmo artista
    outras_obras = ObraArte.objects.filter(
        artista=obra.artista, 
        status='ativo'
    ).exclude(pk=obra.pk)[:4]
    
    context = {
        'obra': obra,
        'outras_obras': outras_obras
    }
    
    return render(request, 'arte/obra_detail.html', context)


def exposicoes(request):
    """View das exposições de arte"""
    agora = timezone.now().date()
    
    # Filtros
    status_filtro = request.GET.get('status', 'ativas')
    busca = request.GET.get('busca')
    
    # Query base
    exposicoes_qs = ExposicaoArte.objects.filter(status='ativo').prefetch_related('obras')
    
    # Filtrar por status temporal
    if status_filtro == 'ativas':
        exposicoes_qs = exposicoes_qs.filter(
            data_inicio__lte=agora,
            data_fim__gte=agora
        )
    elif status_filtro == 'proximas':
        exposicoes_qs = exposicoes_qs.filter(data_inicio__gt=agora)
    elif status_filtro == 'passadas':
        exposicoes_qs = exposicoes_qs.filter(data_fim__lt=agora)
    
    # Busca
    if busca:
        exposicoes_qs = exposicoes_qs.filter(
            Q(titulo__icontains=busca) |
            Q(descricao__icontains=busca) |
            Q(curador__icontains=busca)
        )
    
    # Paginação
    paginator = Paginator(exposicoes_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'exposicoes': page_obj,
        'status_filtro': status_filtro,
        'busca': busca,
        'total_exposicoes': exposicoes_qs.count()
    }
    
    return render(request, 'arte/exposicoes.html', context)


def exposicao_detail(request, pk):
    """View de detalhes de uma exposição"""
    exposicao = get_object_or_404(
        ExposicaoArte.objects.prefetch_related('obras__artista'), 
        pk=pk, 
        status='ativo'
    )
    
    context = {
        'exposicao': exposicao,
        'obras': exposicao.obras.filter(status='ativo')
    }
    
    return render(request, 'arte/exposicao_detail.html', context)


def artista_detail(request, pk):
    """View de detalhes de um artista"""
    artista = get_object_or_404(
        Artista.objects.prefetch_related('tecnicas_dominadas'), 
        pk=pk, 
        status='ativo'
    )
    
    # Obras do artista
    obras = ObraArte.objects.filter(
        artista=artista, 
        status='ativo'
    ).order_by('-ano_criacao')
    
    # Paginação das obras
    paginator = Paginator(obras, 8)
    page_number = request.GET.get('page')
    obras_page = paginator.get_page(page_number)
    
    context = {
        'artista': artista,
        'obras': obras_page,
        'total_obras': obras.count()
    }
    
    return render(request, 'arte/artista_detail.html', context)
