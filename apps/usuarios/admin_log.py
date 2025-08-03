from django.contrib import admin
from .models_log import LogSistema

@admin.register(LogSistema)
class LogSistemaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'acao', 'data_hora', 'ip']
    search_fields = ['usuario__username', 'acao', 'detalhes', 'ip']
    list_filter = ['acao', 'data_hora']
    readonly_fields = ['usuario', 'acao', 'detalhes', 'data_hora', 'ip']
