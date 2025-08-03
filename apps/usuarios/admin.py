from django.contrib import admin
from .models import Perfil
from .models_log import LogSistema


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'cpf', 'data_nascimento', 'criado_em']
    search_fields = ['user__username', 'cpf']
    list_filter = ['criado_em']


@admin.register(LogSistema)
class LogSistemaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'acao', 'data_hora', 'ip']
    search_fields = ['usuario__username', 'acao', 'detalhes', 'ip']
    list_filter = ['acao', 'data_hora']
    readonly_fields = ['usuario', 'acao', 'detalhes', 'data_hora', 'ip']

    def has_delete_permission(self, request, obj=None):
        return False
