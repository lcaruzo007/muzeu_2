from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import ItemPatrimonio

def lista_patrimonio(request):
    """Lista todos os patrimônios com filtros."""
    patrimonios = ItemPatrimonio.objects.all()
    
    # Filtro de busca
    q = request.GET.get('q')
    if q:
        patrimonios = patrimonios.filter(
            Q(nome__icontains=q) | 
            Q(descricao__icontains=q) |
            Q(origem__icontains=q)
        )
    
    # Filtro por categoria
    categoria = request.GET.get('categoria')
    if categoria:
        patrimonios = patrimonios.filter(categoria=categoria)
    
    # Filtro por estado de conservação
    estado = request.GET.get('estado')
    if estado:
        patrimonios = patrimonios.filter(estado_conservacao=estado)
    
    context = {
        'patrimonios': patrimonios,
    }
    return render(request, 'patrimonio/lista.html', context)

def detalhe_patrimonio(request, id):
    """Retorna detalhes do patrimônio via AJAX."""
    patrimonio = get_object_or_404(ItemPatrimonio, id=id)
    
    context = {
        'patrimonio': patrimonio,
    }
    return render(request, 'patrimonio/detalhe_modal.html', context)

@login_required
def ajax_adicionar_patrimonio(request):
    """Adiciona novo patrimônio via AJAX."""
    if request.method == 'POST':
        try:
            patrimonio = ItemPatrimonio.objects.create(
                nome=request.POST.get('nome'),
                numero_registro=request.POST.get('numero_registro'),
                descricao=request.POST.get('descricao'),
                categoria=request.POST.get('categoria'),
                origem=request.POST.get('origem'),
                estado_conservacao=request.POST.get('estado_conservacao'),
                valor_estimado=request.POST.get('valor_estimado') or None,
                observacoes=request.POST.get('observacoes'),
            )
            
            # Upload de arquivos
            if 'imagem' in request.FILES:
                patrimonio.imagem = request.FILES['imagem']
            
            if 'modelo_3d' in request.FILES:
                patrimonio.modelo_3d = request.FILES['modelo_3d']
            
            patrimonio.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Patrimônio adicionado com sucesso!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao adicionar patrimônio: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def espacos_culturais(request):
    """Página dos espaços culturais com informações sobre museu e casa da cultura."""
    
    # Informações sobre o museu
    museu_info = {
        'nome': 'Museu Municipal Francisco Leonardo Ceravolo',
        'descricao': 'O Museu Municipal Francisco Leonardo Ceravolo é um importante centro de preservação da memória e cultura de Muzambinho. Fundado para honrar a rica história da cidade, o museu abriga um acervo diversificado que conta a trajetória do município desde suas origens até os dias atuais.',
        'historia': 'Inaugurado em homenagem ao ilustre cidadão Francisco Leonardo Ceravolo, o museu se dedica à preservação do patrimônio histórico e cultural de Muzambinho. Suas exposições permanentes e temporárias oferecem aos visitantes uma jornada pela história local, destacando personagens importantes, tradições e momentos marcantes.',
        'endereco': 'Centro de Muzambinho, MG',
        'horario': 'Segunda a Sexta: 8h às 17h | Sábados: 8h às 12h',
        'telefone': '(35) 3571-1234',
        'email': 'museu@muzambinho.mg.gov.br'
    }
    
    # Informações sobre a casa da cultura
    casa_cultura_info = {
        'nome': 'Casa da Cultura de Muzambinho',
        'descricao': 'A Casa da Cultura é um espaço dinâmico dedicado à promoção e difusão das artes e manifestações culturais em Muzambinho. É um local de encontro para artistas, estudantes e toda a comunidade interessada em cultura.',
        'historia': 'Criada com o objetivo de fomentar a produção cultural local, a Casa da Cultura oferece oficinas, cursos, exposições e eventos que valorizam os talentos da região. É um centro de formação e expressão artística que contribui para o desenvolvimento cultural da cidade.',
        'endereco': 'Centro de Muzambinho, MG',
        'horario': 'Segunda a Sexta: 8h às 18h | Sábados: 8h às 14h',
        'telefone': '(35) 3571-5678',
        'email': 'cultura@muzambinho.mg.gov.br'
    }
    
    # Imagens para os carrosséis (você pode adicionar mais imagens depois)
    museu_imagens = [
        '/static/logo_museu.png',
        '/static/logo.png',
        '/static/logo2.png',
    ]
    
    casa_cultura_imagens = [
        '/static/logo3.png',
        '/static/logo.png',
        '/static/logo_museu.png',
    ]
    
    context = {
        'museu': museu_info,
        'casa_cultura': casa_cultura_info,
        'museu_imagens': museu_imagens,
        'casa_cultura_imagens': casa_cultura_imagens,
    }
    
    return render(request, 'patrimonio/espacos_culturais.html', context)
