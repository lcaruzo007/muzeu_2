from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')

    nome = models.CharField(max_length=150, verbose_name='Nome Completo')
    email = models.EmailField(max_length=254, verbose_name='E-mail')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    foto = models.ImageField(upload_to='usuarios/fotos/', blank=True, null=True, verbose_name='Foto')
    data_nascimento = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

class Contato(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Nome Completo')
    email = models.EmailField(max_length=254, verbose_name='E-mail')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    assunto = models.CharField(max_length=100, verbose_name='Assunto')
    mensagem = models.TextField(verbose_name='Mensagem')
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name='Data de Envio')

    def __str__(self):
        return f"{self.nome} - {self.assunto} ({self.data_envio:%d/%m/%Y})"
