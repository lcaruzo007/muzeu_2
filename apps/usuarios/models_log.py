from django.db import models
from django.contrib.auth.models import User

class LogSistema(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    acao = models.CharField(max_length=255)
    detalhes = models.TextField(blank=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = 'Log do Sistema'
        verbose_name_plural = 'Logs do Sistema'
        ordering = ['-data_hora']

    def __str__(self):
        return f"{self.usuario} - {self.acao} em {self.data_hora}"
