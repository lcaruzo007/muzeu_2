from django.contrib import admin
from .models import AreaPesquisa, Pesquisador, TipoPesquisa, Pesquisa, DocumentoPesquisa, Genealogia


class DocumentoPesquisaInline(admin.TabularInline):
    model = DocumentoPesquisa
    extra = 1


@admin.register(AreaPesquisa)
class AreaPesquisaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']


@admin.register(Pesquisador)
class PesquisadorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'instituicao', 'titulacao', 'ativo', 'cadastrado_em']
    list_filter = ['ativo', 'areas_interesse', 'cadastrado_em']
    search_fields = ['nome', 'email', 'instituicao']
    readonly_fields = ['cadastrado_em']
    filter_horizontal = ['areas_interesse']


@admin.register(TipoPesquisa)
class TipoPesquisaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']


@admin.register(Pesquisa)
class PesquisaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'area', 'tipo', 'pesquisador_principal', 'status', 'publica', 'criado_em']
    list_filter = ['area', 'tipo', 'status', 'publica', 'criado_em']
    search_fields = ['titulo', 'resumo', 'palavras_chave']
    readonly_fields = ['criado_em', 'atualizado_em']
    filter_horizontal = ['colaboradores']
    inlines = [DocumentoPesquisaInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'resumo', 'area', 'tipo', 'palavras_chave')
        }),
        ('Pesquisadores', {
            'fields': ('pesquisador_principal', 'colaboradores')
        }),
        ('Cronograma', {
            'fields': ('data_inicio', 'data_fim', 'status')
        }),
        ('Conteúdo Científico', {
            'fields': ('metodologia', 'resultados', 'conclusoes')
        }),
        ('Outros', {
            'fields': ('financiamento', 'publica')
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Genealogia)
class GenealogiaAdmin(admin.ModelAdmin):
    list_display = ['nome_pessoa', 'nome_pai', 'nome_mae', 'data_nascimento', 'verificado']
    list_filter = ['verificado', 'local_nascimento', 'cadastrado_em']
    search_fields = ['nome_pessoa', 'nome_pai', 'nome_mae', 'local_nascimento']
    readonly_fields = ['cadastrado_em']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome_pessoa', 'nome_pai', 'nome_mae', 'profissao')
        }),
        ('Nascimento', {
            'fields': ('data_nascimento', 'local_nascimento')
        }),
        ('Falecimento', {
            'fields': ('data_falecimento', 'local_falecimento')
        }),
        ('Fonte e Verificação', {
            'fields': ('fonte_informacao', 'verificado')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Timestamp', {
            'fields': ('cadastrado_em',),
            'classes': ('collapse',)
        }),
    )
