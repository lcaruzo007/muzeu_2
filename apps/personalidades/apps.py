from django.apps import AppConfig


class PersonalidadesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.personalidades'
    verbose_name = 'Personalidades Culturais'
    
    def ready(self):
        """Importa sinais quando a aplicação está pronta"""
        pass
