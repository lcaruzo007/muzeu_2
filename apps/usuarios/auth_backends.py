from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from apps.usuarios.models import Perfil

class CPFBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Permite login tanto por username quanto por CPF
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                perfil = Perfil.objects.get(cpf=username)
                user = perfil.user
            except Perfil.DoesNotExist:
                return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
