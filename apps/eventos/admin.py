from django.contrib import admin
from .models import CategoriaEvento, Evento, InscricaoEvento, MaterialEvento


class InscricaoEventoInline(admin.TabularInline):
    model = InscricaoEvento
    extra = 0
    readonly_fields = ['inscrito_em']


class MaterialEventoInline(admin.TabularInline):
    model = MaterialEvento
    extra = 1


@admin.register(CategoriaEvento)
class CategoriaEventoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cor']
    search_fields = ['nome']


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'data_inicio', 'local', 'total_inscritos', 'status', 'ativo']
    list_filter = ['categoria', 'status', 'ativo', 'data_inicio']
    search_fields = ['titulo', 'descricao', 'palestrante']
    readonly_fields = ['criado_em', 'atualizado_em']
    inlines = [InscricaoEventoInline, MaterialEventoInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'categoria', 'palestrante', 'imagem')
        }),
        ('Data e Local', {
            'fields': ('data_inicio', 'data_fim', 'local')
        }),
        ('Inscrições', {
            'fields': ('requer_inscricao', 'capacidade_maxima', 'valor_inscricao')
        }),
        ('Status', {
            'fields': ('status', 'ativo')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InscricaoEvento)
class InscricaoEventoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'evento', 'email', 'confirmada', 'presente', 'inscrito_em']
    list_filter = ['confirmada', 'presente', 'evento', 'inscrito_em']
    search_fields = ['nome', 'email', 'evento__titulo']
    readonly_fields = ['inscrito_em']
