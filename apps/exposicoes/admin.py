from django.contrib import admin
from .models import Exposicao, ItemExposicao, FotoExposicao


class ItemExposicaoInline(admin.TabularInline):
    model = ItemExposicao
    extra = 1


class FotoExposicaoInline(admin.TabularInline):
    model = FotoExposicao
    extra = 1


@admin.register(Exposicao)
class ExposicaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'status', 'data_inicio', 'data_fim', 'numero_visitantes', 'ativa']
    list_filter = ['tipo', 'status', 'ativa', 'data_inicio']
    search_fields = ['titulo', 'descricao', 'curador']
    readonly_fields = ['criado_em', 'atualizado_em']
    inlines = [ItemExposicaoInline, FotoExposicaoInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'tipo', 'status', 'imagem_principal')
        }),
        ('Datas e Local', {
            'fields': ('data_inicio', 'data_fim', 'local')
        }),
        ('Responsável', {
            'fields': ('curador',)
        }),
        ('Estatísticas', {
            'fields': ('numero_visitantes',)
        }),
        ('Observações', {
            'fields': ('observacoes', 'ativa')
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
