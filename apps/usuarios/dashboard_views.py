from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.utils import timezone
from datetime import datetime, timedelta
from apps.acervo.models import ItemAcervo, CategoriaAcervo
from apps.patrimonio.models import ItemPatrimonio, Patrimonio
from apps.exposicoes.models import Exposicao
from apps.visitantes.models import Visitante, Visita
from apps.eventos.models import Evento, InscricaoEvento
from apps.noticias.models import Noticia
from apps.usuarios.models_log import LogSistema
import json

@staff_member_required
def dashboard_view(request):
    # Período para análise (últimos 12 meses)
    hoje = timezone.now()
    inicio_periodo = hoje - timedelta(days=365)
    
    # Estatísticas gerais
    stats = {
        'total_acervo': ItemAcervo.objects.filter(ativo=True).count(),
        'total_patrimonio': ItemPatrimonio.objects.count(),
        'total_visitantes': Visitante.objects.count(),
        'total_exposicoes': Exposicao.objects.count(),
        'exposicoes_ativas': Exposicao.objects.filter(ativa=True).count(),
        'eventos_ativos': Evento.objects.filter(ativo=True, data_inicio__gte=hoje).count(),
        'visitas_mes': Visita.objects.filter(data_visita__month=hoje.month, data_visita__year=hoje.year).count(),
        'noticias_publicadas': Noticia.objects.filter(status='publicado').count(),
    }
    
    # Gráfico: Itens por categoria
    categorias_acervo = list(CategoriaAcervo.objects.annotate(
        total=Count('itemacervo', filter=Q(itemacervo__ativo=True))
    ).values('nome', 'total'))
    
    # Gráfico: Visitas por mês (últimos 12 meses)
    visitas_por_mes = list(Visita.objects.filter(
        data_visita__gte=inicio_periodo
    ).annotate(
        mes=TruncMonth('data_visita')
    ).values('mes').annotate(
        total=Count('id')
    ).order_by('mes'))
    
    # Gráfico: Estado de conservação do acervo
    conservacao_stats = list(ItemAcervo.objects.filter(
        ativo=True
    ).values('estado_conservacao').annotate(
        total=Count('id')
    ))
    
    # Gráfico: Logs de atividade (últimos 30 dias)
    logs_atividade = list(LogSistema.objects.filter(
        data_hora__gte=hoje - timedelta(days=30)
    ).values('acao').annotate(
        total=Count('id')
    ).order_by('-total')[:10])
    
    # Top 5 categorias mais visitadas
    top_categorias = list(CategoriaAcervo.objects.annotate(
        visitas=Count('itemacervo__categoria__itemacervo')
    ).order_by('-visitas')[:5].values('nome', 'visitas'))
    
    # Eventos com mais inscrições
    eventos_populares = list(Evento.objects.annotate(
        total_inscricoes=Count('inscricoes', filter=Q(inscricoes__confirmada=True))
    ).filter(total_inscricoes__gt=0).order_by('-total_inscricoes')[:5].values(
        'titulo', 'total_inscricoes', 'data_inicio'
    ))
    
    # Crescimento mensal do acervo
    crescimento_acervo = list(ItemAcervo.objects.filter(
        criado_em__gte=inicio_periodo
    ).annotate(
        mes=TruncMonth('criado_em')
    ).values('mes').annotate(
        total=Count('id')
    ).order_by('mes'))
    
    # Preparar dados para gráficos em JSON
    context = {
        'stats': stats,
        'categorias_json': json.dumps([{
            'label': cat['nome'], 
            'value': cat['total']
        } for cat in categorias_acervo]),
        'visitas_json': json.dumps([{
            'mes': visita['mes'].strftime('%Y-%m') if visita['mes'] else '',
            'total': visita['total']
        } for visita in visitas_por_mes]),
        'conservacao_json': json.dumps([{
            'estado': dict(ItemAcervo.ESTADO_CHOICES).get(item['estado_conservacao'], item['estado_conservacao']),
            'total': item['total']
        } for item in conservacao_stats]),
        'logs_json': json.dumps([{
            'acao': log['acao'],
            'total': log['total']
        } for log in logs_atividade]),
        'crescimento_json': json.dumps([{
            'mes': item['mes'].strftime('%Y-%m') if item['mes'] else '',
            'total': item['total']
        } for item in crescimento_acervo]),
        'top_categorias': top_categorias,
        'eventos_populares': eventos_populares,
    }
    
    return render(request, 'dashboard/estatisticas.html', context)
