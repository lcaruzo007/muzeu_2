from django.db import models
from django.urls import reverse
from apps.acervo.models import ItemAcervo


class Exposicao(models.Model):
    TIPO_CHOICES = [
        ('permanente', 'Permanente'),
        ('temporaria', 'Temporária'),
        ('itinerante', 'Itinerante'),
        ('virtual', 'Virtual'),
    ]
    
    STATUS_CHOICES = [
        ('planejamento', 'Em Planejamento'),
        ('em_andamento', 'Em Andamento'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='temporaria', verbose_name="Tipo")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejamento', verbose_name="Status")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(null=True, blank=True, verbose_name="Data de Fim")
    local = models.CharField(max_length=200, verbose_name="Local")
    curador = models.CharField(max_length=200, blank=True, verbose_name="Curador")
    numero_visitantes = models.IntegerField(default=0, verbose_name="Número de Visitantes")
    imagem_principal = models.ImageField(upload_to='exposicoes/', blank=True, verbose_name="Imagem Principal")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    ativa = models.BooleanField(default=True, verbose_name="Ativa")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Exposição"
        verbose_name_plural = "Exposições"
        ordering = ['-data_inicio']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('exposicoes:detalhe', kwargs={'pk': self.pk})


class ItemExposicao(models.Model):
    exposicao = models.ForeignKey(Exposicao, on_delete=models.CASCADE, related_name='itens', verbose_name="Exposição")
    item_acervo = models.ForeignKey(ItemAcervo, on_delete=models.CASCADE, verbose_name="Item do Acervo")
    posicao = models.IntegerField(default=0, verbose_name="Posição na Exposição")
    destaque = models.BooleanField(default=False, verbose_name="Item em Destaque")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    
    class Meta:
        verbose_name = "Item da Exposição"
        verbose_name_plural = "Itens da Exposição"
        ordering = ['posicao']
        unique_together = ['exposicao', 'item_acervo']
    
    def __str__(self):
        return f"{self.exposicao.titulo} - {self.item_acervo.titulo}"


class FotoExposicao(models.Model):
    exposicao = models.ForeignKey(Exposicao, on_delete=models.CASCADE, related_name='fotos', verbose_name="Exposição")
    imagem = models.ImageField(upload_to='exposicoes/fotos/', verbose_name="Imagem")
    descricao = models.CharField(max_length=200, blank=True, verbose_name="Descrição")
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Foto da Exposição"
        verbose_name_plural = "Fotos da Exposição"
    
    def __str__(self):
        return f"Foto de {self.exposicao.titulo}"
