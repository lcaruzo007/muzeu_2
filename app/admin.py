from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import (
    Categoria, ItemAcervo, ImagemItemAcervo, Patrimonio,
    ImagemPatrimonio, DocumentoHistorico
)


# Resources for import/export
class CategoriaResource(resources.ModelResource):
    """Resource class for Categoria import/export."""
    
    class Meta:
        model = Categoria
        fields = ('id', 'nome', 'descricao', 'ativa')
        export_order = ('id', 'nome', 'descricao', 'ativa')


class ItemAcervoResource(resources.ModelResource):
    """Resource class for ItemAcervo import/export."""
    
    class Meta:
        model = ItemAcervo
        fields = (
            'id', 'nome', 'categoria', 'descricao', 'origem', 
            'numero_registro', 'estado_conservacao', 'status'
        )
        export_order = (
            'id', 'nome', 'categoria', 'descricao', 'origem',
            'numero_registro', 'estado_conservacao', 'status'
        )


# Inline admins
class ImagemItemAcervoInline(admin.TabularInline):
    """Inline admin for collection item images."""
    model = ImagemItemAcervo
    extra = 1
    fields = ('imagem', 'legenda', 'eh_principal', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        """Display image preview."""
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 120px;" />',
                obj.imagem.url
            )
        return "Sem imagem"
    preview.short_description = "Preview"


class ImagemPatrimonioInline(admin.TabularInline):
    """Inline admin for patrimony images."""
    model = ImagemPatrimonio
    extra = 1
    fields = ('imagem', 'legenda', 'eh_principal', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        """Display image preview."""
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 120px;" />',
                obj.imagem.url
            )
        return "Sem imagem"
    preview.short_description = "Preview"


# Admin configurations
@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
    """Admin configuration for Categoria model."""
    
    resource_class = CategoriaResource
    list_display = ('nome', 'ativa', 'get_total_itens', 'get_total_documentos', 'data_criacao')
    list_filter = ('ativa', 'data_criacao')
    search_fields = ('nome', 'descricao')
    date_hierarchy = 'data_criacao'
    fieldsets = (
        ('Informações da Categoria', {
            'fields': ('nome', 'descricao', 'ativa')
        }),
    )

    def get_total_itens(self, obj):
        """Display total number of items in category."""
        return obj.itens_acervo.count()
    get_total_itens.short_description = 'Total de Itens'

    def get_total_documentos(self, obj):
        """Display total number of documents in category."""
        return obj.documentos.count()
    get_total_documentos.short_description = 'Total de Documentos'


@admin.register(ItemAcervo)
class ItemAcervoAdmin(ImportExportModelAdmin):
    """Admin configuration for ItemAcervo model."""
    
    resource_class = ItemAcervoResource
    list_display = (
        'nome', 'numero_registro', 'categoria', 'origem', 
        'estado_conservacao', 'status', 'data_adicao'
    )
    list_filter = ('categoria', 'estado_conservacao', 'status', 'data_adicao')
    search_fields = ('nome', 'numero_registro', 'descricao', 'origem')
    date_hierarchy = 'data_adicao'
    inlines = [ImagemItemAcervoInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'numero_registro', 'categoria', 'descricao')
        }),
        ('Origem e História', {
            'fields': ('origem', 'data_origem')
        }),
        ('Estado e Localização', {
            'fields': ('estado_conservacao', 'status', 'localizacao_fisica')
        }),
        ('Informações Adicionais', {
            'fields': ('valor_estimado', 'usuario_adicionado'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('categoria', 'usuario_adicionado')


@admin.register(ImagemItemAcervo)
class ImagemItemAcervoAdmin(admin.ModelAdmin):
    """Admin configuration for ImagemItemAcervo model."""
    
    list_display = ('item_acervo', 'legenda', 'eh_principal', 'get_preview', 'data_upload')
    list_filter = ('eh_principal', 'data_upload', 'item_acervo__categoria')
    search_fields = ('item_acervo__nome', 'legenda')
    date_hierarchy = 'data_upload'
    fieldsets = (
        ('Imagem', {
            'fields': ('item_acervo', 'imagem', 'legenda', 'eh_principal')
        }),
    )

    def get_preview(self, obj):
        """Display image preview."""
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 80px;" />',
                obj.imagem.url
            )
        return "Sem imagem"
    get_preview.short_description = 'Preview'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('item_acervo')


@admin.register(Patrimonio)
class PatrimonioAdmin(admin.ModelAdmin):
    """Admin configuration for Patrimonio model."""
    
    list_display = (
        'nome', 'tipo', 'localizacao', 'status', 
        'data_origem', 'data_adicao'
    )
    list_filter = ('tipo', 'status', 'data_adicao')
    search_fields = ('nome', 'descricao', 'localizacao')
    date_hierarchy = 'data_adicao'
    inlines = [ImagemPatrimonioInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'tipo', 'descricao')
        }),
        ('Localização', {
            'fields': ('localizacao', 'coordenadas')
        }),
        ('História', {
            'fields': ('data_origem', 'importancia_historica')
        }),
        ('Status', {
            'fields': ('status', 'usuario_adicionado')
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('usuario_adicionado')


@admin.register(ImagemPatrimonio)
class ImagemPatrimonioAdmin(admin.ModelAdmin):
    """Admin configuration for ImagemPatrimonio model."""
    
    list_display = ('patrimonio', 'legenda', 'eh_principal', 'get_preview', 'data_upload')
    list_filter = ('eh_principal', 'data_upload', 'patrimonio__tipo')
    search_fields = ('patrimonio__nome', 'legenda')
    date_hierarchy = 'data_upload'
    fieldsets = (
        ('Imagem', {
            'fields': ('patrimonio', 'imagem', 'legenda', 'eh_principal')
        }),
    )

    def get_preview(self, obj):
        """Display image preview."""
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 80px;" />',
                obj.imagem.url
            )
        return "Sem imagem"
    get_preview.short_description = 'Preview'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('patrimonio')


@admin.register(DocumentoHistorico)
class DocumentoHistoricoAdmin(admin.ModelAdmin):
    """Admin configuration for DocumentoHistorico model."""
    
    list_display = (
        'titulo', 'tipo_documento', 'categoria', 'autor', 
        'data_origem', 'data_adicao'
    )
    list_filter = ('tipo_documento', 'categoria', 'data_origem', 'data_adicao')
    search_fields = ('titulo', 'descricao', 'autor', 'local_origem')
    date_hierarchy = 'data_adicao'
    fieldsets = (
        ('Informações do Documento', {
            'fields': ('titulo', 'tipo_documento', 'categoria', 'descricao')
        }),
        ('Autoria e Origem', {
            'fields': ('autor', 'data_origem', 'local_origem')
        }),
        ('Características Físicas', {
            'fields': ('numero_paginas', 'documento')
        }),
        ('Sistema', {
            'fields': ('usuario_adicionado',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('categoria', 'usuario_adicionado')