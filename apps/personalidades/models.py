from django.db import models
from django.urls import reverse

from django.utils import timezone

class AreaAtuacao(models.Model):
    """Áreas de atuação cultural (música, literatura, artes visuais, etc.)"""
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    icone = models.CharField(max_length=50, default='star')  # ícone feather
    cor = models.CharField(max_length=7, default='#6B2C26')  # cor hex
    
    class Meta:
        verbose_name = "Área de Atuação"
        verbose_name_plural = "Áreas de Atuação"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class Personalidade(models.Model):
    """Personalidades que marcaram a cultura muzambinhense"""
    
    TIPO_CHOICES = [
        ('artista', 'Artista'),
        ('escritor', 'Escritor/Poeta'),
        ('musico', 'Músico/Compositor'),
        ('historiador', 'Historiador'),
        ('educador', 'Educador Cultural'),
        ('politico', 'Político/Gestor Cultural'),
        ('empresario', 'Empresário/Mecenas'),
        ('outros', 'Outros'),
    ]
    
    STATUS_CHOICES = [
        ('vivo', 'Vivo'),
        ('falecido', 'Falecido'),
    ]
    
    # Dados básicos
    nome_completo = models.CharField(max_length=200)
    nome_artistico = models.CharField(max_length=150, blank=True, help_text="Nome pelo qual é conhecido")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    areas_atuacao = models.ManyToManyField(AreaAtuacao, related_name='personalidades')
    
    # Datas
    data_nascimento = models.DateField()
    data_falecimento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='vivo')
    
    # Informações pessoais
    local_nascimento = models.CharField(max_length=200, help_text="Cidade/região de nascimento")
    biografia = models.TextField(help_text="Biografia detalhada da personalidade")
    resumo = models.TextField(max_length=500, help_text="Resumo curto para cards")
    
    # Contribuições culturais
    principais_obras = models.TextField(blank=True, help_text="Lista das principais obras/contribuições")
    premios_reconhecimentos = models.TextField(blank=True, help_text="Prêmios e reconhecimentos recebidos")
    influencias = models.TextField(blank=True, help_text="Principais influências artísticas")
    legado = models.TextField(blank=True, help_text="Impacto e legado cultural")
    
    # Mídias
    foto_principal = models.ImageField(upload_to='personalidades/fotos/', blank=True)
    foto_galeria = models.ImageField(upload_to='personalidades/galeria/', blank=True)
    audio_depoimento = models.FileField(upload_to='personalidades/audios/', blank=True)
    video_depoimento = models.FileField(upload_to='personalidades/videos/', blank=True)
    
    nome = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='personalidades/fotos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    colaboradores = models.ManyToManyField('self', blank=True, related_name='parceiros')
    
    # Metadados
    destaque = models.BooleanField(default=False, help_text="Exibir em destaque no salão de honra")
    ordem_exibicao = models.PositiveIntegerField(default=0, help_text="Ordem de exibição (menor = primeiro)")
    data_inclusao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Personalidade Cultural"
        verbose_name_plural = "Personalidades Culturais"
        ordering = ['ordem_exibicao', 'nome_completo']
    
    def __str__(self):
        return self.nome_artistico or self.nome_completo
    
    def get_absolute_url(self):
        return reverse('personalidades:detalhe', kwargs={'pk': self.pk})
    
    @property
    def nome_exibicao(self):
        return self.nome_artistico or self.nome_completo
    
    @property
    def idade_atual_ou_falecimento(self):
        from datetime import date
        if self.data_falecimento:
            return self.data_falecimento.year - self.data_nascimento.year
        return date.today().year - self.data_nascimento.year
    
    @property
    def periodo_atuacao(self):
        inicio = self.data_nascimento.year + 15  # assume início da carreira aos 15 anos
        fim = self.data_falecimento.year if self.data_falecimento else "presente"
        return f"{inicio} - {fim}"

class ContribuicaoCultural(models.Model):
    """Contribuições específicas de cada personalidade"""
    
    TIPO_CONTRIBUICAO = [
        ('obra', 'Obra Artística'),
        ('evento', 'Evento Cultural'),
        ('instituicao', 'Fundação de Instituição'),
        ('movimento', 'Movimento Cultural'),
        ('ensino', 'Contribuição Educacional'),
        ('preservacao', 'Preservação Cultural'),
    ]
    
    personalidade = models.ForeignKey(Personalidade, on_delete=models.CASCADE, related_name='contribuicoes')
    tipo = models.CharField(max_length=20, choices=TIPO_CONTRIBUICAO)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_contribuicao = models.DateField(help_text="Data aproximada da contribuição")
    impacto = models.TextField(blank=True, help_text="Impacto da contribuição na cultura local")
    imagem = models.ImageField(upload_to='personalidades/contribuicoes/', blank=True)
    
    class Meta:
        verbose_name = "Contribuição Cultural"
        verbose_name_plural = "Contribuições Culturais"
        ordering = ['-data_contribuicao']
    
    def __str__(self):
        return f"{self.personalidade} - {self.titulo}"

class CitacaoPersonalidade(models.Model):
    """Citações e frases marcantes das personalidades"""
    personalidade = models.ForeignKey(Personalidade, on_delete=models.CASCADE, related_name='citacoes')
    texto = models.TextField(help_text="Texto da citação")
    contexto = models.CharField(max_length=200, blank=True, help_text="Contexto ou ocasião da citação")
    data_citacao = models.DateField(null=True, blank=True)
    fonte = models.CharField(max_length=200, blank=True, help_text="Fonte da citação")
    
    class Meta:
        verbose_name = "Citação"
        verbose_name_plural = "Citações"
        ordering = ['-data_citacao']
    
    def __str__(self):
        return f"{self.personalidade} - {self.texto[:50]}..."
