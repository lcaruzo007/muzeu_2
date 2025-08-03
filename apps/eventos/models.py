from django.db import models
from django.urls import reverse


class CategoriaEvento(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    cor = models.CharField(max_length=7, default="#355D9B", verbose_name="Cor (Hex)")
    
    class Meta:
        verbose_name = "Categoria de Evento"
        verbose_name_plural = "Categorias de Evento"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Evento(models.Model):
    STATUS_CHOICES = [
        ('planejamento', 'Em Planejamento'),
        ('divulgacao', 'Em Divulgação'),
        ('inscricoes_abertas', 'Inscrições Abertas'),
        ('inscricoes_encerradas', 'Inscrições Encerradas'),
        ('em_andamento', 'Em Andamento'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    categoria = models.ForeignKey(CategoriaEvento, on_delete=models.CASCADE, verbose_name="Categoria")
    palestrante = models.CharField(max_length=200, blank=True, verbose_name="Palestrante/Responsável")
    data_inicio = models.DateTimeField(verbose_name="Data e Hora de Início")
    data_fim = models.DateTimeField(verbose_name="Data e Hora de Fim")
    local = models.CharField(max_length=200, verbose_name="Local")
    capacidade_maxima = models.IntegerField(null=True, blank=True, verbose_name="Capacidade Máxima")
    valor_inscricao = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Valor da Inscrição")
    requer_inscricao = models.BooleanField(default=True, verbose_name="Requer Inscrição")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='planejamento', verbose_name="Status")
    imagem = models.ImageField(upload_to='eventos/', blank=True, verbose_name="Imagem")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-data_inicio']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('eventos:detalhe', kwargs={'pk': self.pk})
    
    def total_inscritos(self):
        return self.inscricoes.filter(confirmada=True).count()
    
    def vagas_disponiveis(self):
        if self.capacidade_maxima:
            return self.capacidade_maxima - self.total_inscritos()
        return None


class InscricaoEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes', verbose_name="Evento")
    nome = models.CharField(max_length=200, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    instituicao = models.CharField(max_length=200, blank=True, verbose_name="Instituição")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    confirmada = models.BooleanField(default=False, verbose_name="Confirmada")
    presente = models.BooleanField(default=False, verbose_name="Presente no Evento")
    inscrito_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Inscrição em Evento"
        verbose_name_plural = "Inscrições em Eventos"
        ordering = ['-inscrito_em']
        unique_together = ['evento', 'email']
    
    def __str__(self):
        return f"{self.nome} - {self.evento.titulo}"


class MaterialEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='materiais', verbose_name="Evento")
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    arquivo = models.FileField(upload_to='eventos/materiais/', verbose_name="Arquivo")
    publico = models.BooleanField(default=True, verbose_name="Público")
    adicionado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Material do Evento"
        verbose_name_plural = "Materiais do Evento"
        ordering = ['titulo']
    
    def __str__(self):
        return f"{self.evento.titulo} - {self.titulo}"
