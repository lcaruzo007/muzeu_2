from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Personalidade, AreaAtuacao


def salao_honra(request):
    """View principal do Salão de Honra"""
    # Filtros
    area_filtro = request.GET.get('area')
    busca = request.GET.get('busca')

    # Query base
    personalidades = Personalidade.objects.filter(status__in=['vivo', 'falecido']).prefetch_related('areas_atuacao')

    # Aplicar filtros
    if area_filtro:
        personalidades = personalidades.filter(areas_atuacao__id=area_filtro)

    if busca:
        personalidades = personalidades.filter(
            Q(nome__icontains=busca) |
            Q(nome_completo__icontains=busca) |
            Q(nome_artistico__icontains=busca) |
            Q(biografia__icontains=busca) |
            Q(legado__icontains=busca)
        )

    # Paginação
    paginator = Paginator(personalidades, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Áreas para filtro
    areas = AreaAtuacao.objects.all().order_by('nome')

    context = {
        'personalidades': page_obj,
        'areas': areas,
        'area_selecionada': area_filtro,
        'busca': busca,
        'total_personalidades': personalidades.count()
    }

    return render(request, 'personalidades/salao_honra.html', context)


def personalidade_detail(request, pk=None, slug=None):
    """View de detalhes de uma personalidade"""
    if pk:
        personalidade = get_object_or_404(
            Personalidade.objects.prefetch_related(
                'contribuicoes', 'citacoes', 'areas_atuacao', 'colaboradores'
            ),
            pk=pk,
            status__in=['vivo', 'falecido']
        )
    elif slug:
        personalidade = get_object_or_404(
            Personalidade.objects.prefetch_related(
                'contribuicoes', 'citacoes', 'areas_atuacao', 'colaboradores'
            ),
            slug=slug,
            status__in=['vivo', 'falecido']
        )
    else:
        raise Http404()

    context = {
        'personalidade': personalidade,
        'contribuicoes': personalidade.contribuicoes.all().order_by('-data_contribuicao'),
        'citacoes': personalidade.citacoes.all()
    }

    return render(request, 'personalidades/personalidade_detail.html', context)
