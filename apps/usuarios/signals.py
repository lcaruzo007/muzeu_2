
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.apps import apps
from django.conf import settings
from django.utils import timezone
from .models import Perfil
from .models_log import LogSistema

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()

# Log de login
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR') if request else None
    LogSistema.objects.create(
        usuario=user,
        acao='login',
        detalhes='Usuário entrou no sistema',
        ip=ip
    )

# Log de criação e edição para todos os modelos
def log_model_save(sender, instance, created, **kwargs):
    # Não logar o próprio LogSistema para evitar recursão
    if sender.__name__ == 'LogSistema':
        return
    user = getattr(instance, 'user', None)
    acao = 'incluir' if created else 'editar'
    detalhes = f'{sender.__name__} {acao} (ID={instance.pk})'
    LogSistema.objects.create(
        usuario=user if isinstance(user, User) else None,
        acao=acao,
        detalhes=detalhes,
    )

def log_model_delete(sender, instance, **kwargs):
    if sender.__name__ == 'LogSistema':
        return
    user = getattr(instance, 'user', None)
    detalhes = f'{sender.__name__} excluído (ID={instance.pk})'
    LogSistema.objects.create(
        usuario=user if isinstance(user, User) else None,
        acao='excluir',
        detalhes=detalhes,
    )

# Conectar signals para todos os modelos do projeto (exceto LogSistema)
def connect_model_signals():
    for model in apps.get_models():
        if model.__name__ != 'LogSistema':
            post_save.connect(log_model_save, sender=model, dispatch_uid=f'log_save_{model.__name__}')
            post_delete.connect(log_model_delete, sender=model, dispatch_uid=f'log_delete_{model.__name__}')

connect_model_signals()
