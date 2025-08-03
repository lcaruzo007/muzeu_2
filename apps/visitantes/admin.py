from django.contrib import admin
from .models import TipoVisita, Visitante, Visita, AgendamentoVisita


class VisitaInline(admin.TabularInline):
    model = Visita
    extra = 0
    readonly_fields = ['registrado_em']


@admin.register(TipoVisita)
class TipoVisitaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'valor', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome']


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'cidade', 'estado', 'total_visitas', 'cadastrado_em']
    list_filter = ['estado', 'cadastrado_em']
    search_fields = ['nome', 'email', 'cidade']
    readonly_fields = ['cadastrado_em']
    inlines = [VisitaInline]


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ['visitante', 'tipo_visita', 'data_visita', 'numero_acompanhantes', 'avaliacao']
    list_filter = ['tipo_visita', 'data_visita', 'avaliacao']
    search_fields = ['visitante__nome', 'guia']
    readonly_fields = ['registrado_em']
    
    fieldsets = (
        ('Informações da Visita', {
            'fields': ('visitante', 'tipo_visita', 'data_visita', 'numero_acompanhantes', 'guia')
        }),
        ('Avaliação', {
            'fields': ('avaliacao', 'comentario')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Timestamp', {
            'fields': ('registrado_em',),
            'classes': ('collapse',)
        }),
    )


@admin.register(AgendamentoVisita)
class AgendamentoVisitaAdmin(admin.ModelAdmin):
    list_display = ['nome_responsavel', 'instituicao', 'tipo_visita', 'data_desejada', 'numero_visitantes', 'status']
    list_filter = ['status', 'tipo_visita', 'data_desejada']
    search_fields = ['nome_responsavel', 'email', 'instituicao']
    readonly_fields = ['solicitado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações do Responsável', {
            'fields': ('nome_responsavel', 'email', 'telefone', 'instituicao')
        }),
        ('Detalhes da Visita', {
            'fields': ('tipo_visita', 'data_desejada', 'numero_visitantes')
        }),
        ('Status e Observações', {
            'fields': ('status', 'observacoes')
        }),
        ('Timestamps', {
            'fields': ('solicitado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
