from django.db import models
from django.urls import reverse
from django.utils import timezone


class TecnicaArtistica(models.Model):
    """Técnicas artísticas (óleo, aquarela, escultura, etc.)"""
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=50, choices=[
        ('pintura', 'Pintura'),
        ('escultura', 'Escultura'),
        ('desenho', 'Desenho'),
        ('fotografia', 'Fotografia'),
        ('gravura', 'Gravura'),
        ('instalacao', 'Instalação'),
        ('performance', 'Performance'),
        ('digital', 'Arte Digital'),
        ('artesanato', 'Artesanato'),
    ], default='pintura')
    
    class Meta:
        verbose_name = "Técnica Artística"
        verbose_name_plural = "Técnicas Artísticas"
        ordering = ['tipo', 'nome']
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class Artista(models.Model):
    """Artistas locais"""
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('homenageado', 'Homenageado'),
    ]
    
    # Dados básicos
    nome = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='arte/artistas/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    tecnicas_dominadas = models.ManyToManyField(TecnicaArtistica, related_name='artistas')
    data_nascimento = models.DateField(blank=True, null=True)
    local_nascimento = models.CharField(max_length=200, blank=True)
    data_falecimento = models.DateField(blank=True, null=True)
    local_falecimento = models.CharField(max_length=200, blank=True)
    biografia = models.TextField(blank=True)
    estilo_artistico = models.CharField(max_length=200, blank=True)
    influencias = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Artista"
        verbose_name_plural = "Artistas"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class ObraArte(models.Model):
    """Obras de arte do acervo cultural"""
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('em_restauro', 'Em Restauro'),
    ]
    
    # Dados básicos
    titulo = models.CharField(max_length=200)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE, related_name='obras')
    ano_criacao = models.DateField(help_text="Data de criação da obra")
    tecnica = models.ForeignKey(TecnicaArtistica, on_delete=models.SET_NULL, null=True)
    
    # Descrição e contexto
    descricao = models.TextField(help_text="Descrição detalhada da obra")
    dimensoes = models.CharField(max_length=100, blank=True, help_text="Ex: 50x70 cm")
    material_suporte = models.CharField(max_length=100, blank=True, help_text="Ex: tela, papel, madeira")
    estado_conservacao = models.CharField(max_length=50, choices=[
        ('excelente', 'Excelente'),
        ('boa', 'Boa'),
        ('regular', 'Regular'),
        ('ruim', 'Ruim'),
        ('restauracao', 'Necessita Restauração'),
    ], default='boa')
    
    # Localização e propriedade
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    localizacao_atual = models.CharField(max_length=200, blank=True)
    valor_estimado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Mídias
    imagem = models.ImageField(upload_to='arte/obras/', blank=True, null=True)
    imagem_detalhe = models.ImageField(upload_to='arte/obras/detalhes/', blank=True, null=True)
    audio_descricao = models.FileField(upload_to='arte/obras/audio/', blank=True, null=True)
    
    # Metadados
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Obra de Arte"
        verbose_name_plural = "Obras de Arte"
        ordering = ['-ano_criacao', 'titulo']
    
    def __str__(self):
        return f"{self.titulo} - {self.artista} ({self.ano_criacao})"


class ExposicaoArte(models.Model):
    """Exposições de arte (físicas e virtuais)"""
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('encerrado', 'Encerrado'),
    ]
    
    # Dados básicos
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=300, blank=True)
    curador = models.CharField(max_length=200, help_text="Nome do curador")
    
    # Descrição
    descricao = models.TextField(help_text="Descrição geral da exposição")
    conceito_curatorial = models.TextField(blank=True, help_text="Conceito e proposta curatorial")
    
    # Datas e local
    data_inicio = models.DateField()
    data_fim = models.DateField()
    local = models.CharField(max_length=200, help_text="Local da exposição")
    endereco = models.TextField(blank=True)
    
    # Status e visitação
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    virtual = models.BooleanField(default=False)
    link_virtual = models.URLField(blank=True)
    capacidade_visitantes = models.PositiveIntegerField(blank=True, null=True)
    
    # Mídias
    imagem_banner = models.ImageField(upload_to='arte/exposicoes/banners/', blank=True, null=True)
    
    # Relacionamentos
    obras = models.ManyToManyField(ObraArte, related_name='exposicoes')
    
    # Metadados
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Exposição de Arte"
        verbose_name_plural = "Exposições de Arte"
        ordering = ['-data_inicio']
    
    def __str__(self):
        return f"{self.titulo} ({self.data_inicio.year})"
