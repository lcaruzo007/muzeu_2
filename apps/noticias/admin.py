from django.contrib import admin
from .models import CategoriaNoticia, Noticia, ImagemNoticia, ComentarioNoticia, Newsletter


class ImagemNoticiaInline(admin.TabularInline):
    model = ImagemNoticia
    extra = 1


@admin.register(CategoriaNoticia)
class CategoriaNoticiaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'cor', 'ativa']
    list_filter = ['ativa']
    search_fields = ['nome']
    prepopulated_fields = {'slug': ('nome',)}


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'autor', 'status', 'destaque', 'visualizacoes', 'data_publicacao']
    list_filter = ['categoria', 'status', 'destaque', 'autor', 'data_publicacao']
    search_fields = ['titulo', 'resumo', 'conteudo', 'tags']
    readonly_fields = ['visualizacoes', 'criado_em', 'atualizado_em']
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [ImagemNoticiaInline]
    
    fieldsets = (
        ('Conteúdo', {
            'fields': ('titulo', 'slug', 'resumo', 'conteudo', 'imagem_destaque')
        }),
        ('Classificação', {
            'fields': ('categoria', 'tags', 'autor')
        }),
        ('Publicação', {
            'fields': ('status', 'destaque', 'data_publicacao')
        }),
        ('Estatísticas', {
            'fields': ('visualizacoes',)
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ComentarioNoticia)
class ComentarioNoticiaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'noticia', 'aprovado', 'comentado_em']
    list_filter = ['aprovado', 'comentado_em']
    search_fields = ['nome', 'email', 'comentario', 'noticia__titulo']
    readonly_fields = ['comentado_em']
    
    actions = ['aprovar_comentarios', 'reprovar_comentarios']
    
    def aprovar_comentarios(self, request, queryset):
        queryset.update(aprovado=True)
    aprovar_comentarios.short_description = "Aprovar comentários selecionados"
    
    def reprovar_comentarios(self, request, queryset):
        queryset.update(aprovado=False)
    reprovar_comentarios.short_description = "Reprovar comentários selecionados"


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'nome', 'ativo', 'inscrito_em']
    list_filter = ['ativo', 'inscrito_em']
    search_fields = ['email', 'nome']
    readonly_fields = ['inscrito_em']
