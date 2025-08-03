from django.contrib import admin
from .models import CategoriaAcervo, ItemAcervo, FotoAcervo


class FotoAcervoInline(admin.TabularInline):
    model = FotoAcervo
    extra = 1


@admin.register(CategoriaAcervo)
class CategoriaAcervoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'criado_em']
    search_fields = ['nome']
    list_filter = ['criado_em']


@admin.register(ItemAcervo)
class ItemAcervoAdmin(admin.ModelAdmin):
    list_display = ['numero_registro', 'titulo', 'categoria', 'estado_conservacao', 'ativo', 'criado_em']
    list_filter = ['categoria', 'estado_conservacao', 'ativo', 'criado_em']
    search_fields = ['titulo', 'numero_registro', 'descricao', 'origem']
    readonly_fields = ['criado_em', 'atualizado_em']
    inlines = [FotoAcervoInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'numero_registro', 'categoria', 'tipo_item', 'descricao', 'imagem')
        }),
        ('Arquivos', {
            'fields': ('arquivo_audio', 'arquivo_documento')
        }),
        ('Detalhes Históricos', {
            'fields': ('origem', 'data_aproximada', 'doador', 'data_aquisicao')
        }),
        ('Características Físicas', {
            'fields': ('material', 'dimensoes', 'peso', 'estado_conservacao')
        }),
        ('Localização e Valor', {
            'fields': ('localizacao', 'valor_estimado')
        }),
        ('Observações', {
            'fields': ('observacoes', 'ativo', 'disponivel_exposicao')
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FotoAcervo)
class FotoAcervoAdmin(admin.ModelAdmin):
    list_display = ['item', 'descricao', 'criado_em']
    list_filter = ['criado_em', 'item__categoria']
    search_fields = ['item__titulo', 'descricao']
    readonly_fields = ['criado_em']
