from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.usuarios.models import Perfil

class Command(BaseCommand):
    help = 'Cria um perfil para o superusuário caso não exista.'

    def handle(self, *args, **options):
        superusers = User.objects.filter(is_superuser=True)
        for user in superusers:
            if not hasattr(user, 'perfil'):
                Perfil.objects.create(
                    user=user,
                    nome=user.get_full_name() or user.username,
                    email=user.email,
                    cpf='000.000.000-00',  # Atualize depois
                )
                self.stdout.write(self.style.SUCCESS(f'Perfil criado para: {user.username}'))
            else:
                self.stdout.write(f'Perfil já existe para: {user.username}')
