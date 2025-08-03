from django.contrib import admin
from .models import Personalidade, AreaAtuacao, ContribuicaoCultural, CitacaoPersonalidade


@admin.register(AreaAtuacao)
class AreaAtuacaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome']
    ordering = ['nome']


@admin.register(ContribuicaoCultural)
class ContribuicaoCulturalAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'personalidade', 'tipo']  # Removed 'ano'
    list_filter = ['tipo', 'personalidade__areas_atuacao']  # Removed 'ano'
    search_fields = ['titulo', 'personalidade__nome']
    # date_hierarchy removed because 'ano' is not a DateField or DateTimeField
    # ordering = ['-ano']  # Removed 'ano' from ordering


@admin.register(CitacaoPersonalidade)
class CitacaoPersonalidadeAdmin(admin.ModelAdmin):
    list_display = ['personalidade', 'get_autor_citacao', 'get_citacao_preview']
    list_filter = ['personalidade__areas_atuacao']
    search_fields = ['citacao', 'autor_citacao', 'personalidade__nome']
    
    def get_autor_citacao(self, obj):
        return obj.autor_citacao
    get_autor_citacao.short_description = 'Autor da Citação'

    def get_citacao_preview(self, obj):
        return obj.citacao[:100] + '...' if len(obj.citacao) > 100 else obj.citacao
    get_citacao_preview.short_description = 'Citação'


class ContribuicaoCulturalInline(admin.TabularInline):
    model = ContribuicaoCultural
    extra = 1
    fields = ['titulo', 'tipo', 'data_contribuicao', 'descricao']


class CitacaoPersonalidadeInline(admin.TabularInline):
    model = CitacaoPersonalidade
    extra = 1
    fields = ['texto', 'contexto', 'fonte']


@admin.register(Personalidade)
class PersonalidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'get_areas_atuacao', 'data_nascimento', 'data_falecimento', 'status']
    list_filter = ['status', 'areas_atuacao', 'data_nascimento']
    search_fields = ['nome', 'biografia']
    filter_horizontal = ['areas_atuacao', 'colaboradores']
    date_hierarchy = 'data_nascimento'
    ordering = ['nome']

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'nome_completo', 'nome_artistico', 'tipo', 'areas_atuacao', 'foto', 'status', 'colaboradores')
        }),
        ('Dados Biográficos', {
            'fields': ('data_nascimento', 'local_nascimento', 'data_falecimento')
        }),
        ('Biografia e Resumo', {
            'fields': ('biografia', 'resumo', 'principais_obras', 'premios_reconhecimentos', 'influencias', 'legado')
        }),
        ('Mídias', {
            'fields': ('foto_principal', 'foto_galeria', 'audio_depoimento', 'video_depoimento')
        }),
        ('Metadados', {
            'fields': ('destaque', 'ordem_exibicao', 'data_inclusao', 'data_atualizacao')
        }),
    )
    readonly_fields = ['data_inclusao', 'data_atualizacao']
    inlines = [ContribuicaoCulturalInline, CitacaoPersonalidadeInline]

    def get_areas_atuacao(self, obj):
        return ", ".join([area.nome for area in obj.areas_atuacao.all()])
    get_areas_atuacao.short_description = 'Áreas de Atuação'
