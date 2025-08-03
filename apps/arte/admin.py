from django.contrib import admin
from .models import TecnicaArtistica, Artista, ObraArte, ExposicaoArte


@admin.register(TecnicaArtistica)
class TecnicaArtisticaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'descricao']
    list_filter = ['tipo']
    search_fields = ['nome']
    ordering = ['tipo', 'nome']


class ObraArteInline(admin.TabularInline):
    model = ObraArte
    extra = 1
    fields = ['titulo', 'ano_criacao', 'tecnica', 'status']


@admin.register(Artista)
class ArtistaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data_nascimento', 'get_tecnicas', 'status']
    list_filter = ['status', 'tecnicas_dominadas', 'data_nascimento']
    search_fields = ['nome', 'biografia']
    filter_horizontal = ['tecnicas_dominadas']
    date_hierarchy = 'data_nascimento'
    ordering = ['nome']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'foto', 'status')
        }),
        ('Dados Biográficos', {
            'fields': ('data_nascimento', 'local_nascimento', 'data_falecimento', 'local_falecimento')
        }),
        ('Arte e Técnicas', {
            'fields': ('biografia', 'tecnicas_dominadas', 'estilo_artistico', 'influencias')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['criado_em', 'atualizado_em']
    inlines = [ObraArteInline]
    
    def get_tecnicas(self, obj):
        return ", ".join([tecnica.nome for tecnica in obj.tecnicas_dominadas.all()[:3]])
    get_tecnicas.short_description = 'Técnicas Principais'


@admin.register(ObraArte)
class ObraArteAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'artista', 'ano_criacao', 'tecnica', 'status']
    list_filter = ['status', 'tecnica', 'ano_criacao', 'artista']
    search_fields = ['titulo', 'artista__nome', 'descricao']
    date_hierarchy = 'ano_criacao'
    ordering = ['-ano_criacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'artista', 'ano_criacao', 'tecnica')
        }),
        ('Detalhes da Obra', {
            'fields': ('descricao', 'dimensoes', 'material_suporte', 'estado_conservacao')
        }),
        ('Arquivos', {
            'fields': ('imagem', 'imagem_detalhe', 'audio_descricao')
        }),
        ('Status e Localização', {
            'fields': ('status', 'localizacao_atual', 'valor_estimado')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(ExposicaoArte)
class ExposicaoArteAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curador', 'data_inicio', 'data_fim', 'status']
    list_filter = ['status', 'data_inicio', 'curador']
    search_fields = ['titulo', 'descricao', 'curador']
    filter_horizontal = ['obras']
    date_hierarchy = 'data_inicio'
    ordering = ['-data_inicio']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'subtitulo', 'curador', 'imagem_banner')
        }),
        ('Período e Local', {
            'fields': ('data_inicio', 'data_fim', 'local', 'endereco')
        }),
        ('Conteúdo', {
            'fields': ('descricao', 'conceito_curatorial', 'obras')
        }),
        ('Configurações', {
            'fields': ('status', 'virtual', 'link_virtual', 'capacidade_visitantes')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['criado_em', 'atualizado_em']
