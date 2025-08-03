from django.db import models
from django.urls import reverse


class TipoVisita(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Tipo")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="Valor")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    class Meta:
        verbose_name = "Tipo de Visita"
        verbose_name_plural = "Tipos de Visita"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Visitante(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    cidade = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    estado = models.CharField(max_length=50, blank=True, verbose_name="Estado")
    pais = models.CharField(max_length=50, default="Brasil", verbose_name="País")
    idade = models.IntegerField(null=True, blank=True, verbose_name="Idade")
    profissao = models.CharField(max_length=100, blank=True, verbose_name="Profissão")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Visitante"
        verbose_name_plural = "Visitantes"
        ordering = ['-cadastrado_em']
    
    def __str__(self):
        return self.nome
    
    def total_visitas(self):
        return self.visitas.count()


class Visita(models.Model):
    visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, related_name='visitas', verbose_name="Visitante")
    tipo_visita = models.ForeignKey(TipoVisita, on_delete=models.CASCADE, verbose_name="Tipo de Visita")
    data_visita = models.DateTimeField(verbose_name="Data da Visita")
    numero_acompanhantes = models.IntegerField(default=0, verbose_name="Número de Acompanhantes")
    guia = models.CharField(max_length=200, blank=True, verbose_name="Guia")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    avaliacao = models.IntegerField(null=True, blank=True, 
                                   choices=[(i, f"{i} estrela{'s' if i != 1 else ''}") for i in range(1, 6)],
                                   verbose_name="Avaliação")
    comentario = models.TextField(blank=True, verbose_name="Comentário")
    registrado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Visita"
        verbose_name_plural = "Visitas"
        ordering = ['-data_visita']
    
    def __str__(self):
        return f"{self.visitante.nome} - {self.data_visita.strftime('%d/%m/%Y')}"
    
    def get_absolute_url(self):
        return reverse('visitantes:detalhe_visita', kwargs={'pk': self.pk})


class AgendamentoVisita(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('realizado', 'Realizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    nome_responsavel = models.CharField(max_length=200, verbose_name="Nome do Responsável")
    email = models.EmailField(verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    instituicao = models.CharField(max_length=200, blank=True, verbose_name="Instituição")
    tipo_visita = models.ForeignKey(TipoVisita, on_delete=models.CASCADE, verbose_name="Tipo de Visita")
    data_desejada = models.DateTimeField(verbose_name="Data Desejada")
    numero_visitantes = models.IntegerField(verbose_name="Número de Visitantes")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status")
    solicitado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Agendamento de Visita"
        verbose_name_plural = "Agendamentos de Visita"
        ordering = ['-solicitado_em']
    
    def __str__(self):
        return f"{self.nome_responsavel} - {self.data_desejada.strftime('%d/%m/%Y')}"
