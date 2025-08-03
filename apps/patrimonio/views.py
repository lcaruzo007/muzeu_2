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
