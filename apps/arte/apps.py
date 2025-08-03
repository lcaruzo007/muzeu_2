from django.apps import AppConfig


class ArteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.arte'
    verbose_name = 'Arte e Exposições'
    
    def ready(self):
        """Importa sinais quando a aplicação está pronta"""
        pass
