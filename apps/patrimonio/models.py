from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class Categoria(models.Model):
    """Categorias para itens do patrimônio histórico da cidade."""
    
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome da Categoria",
        help_text="Nome da categoria do patrimônio"
    )
    descricao = models.TextField(
        verbose_name="Descrição da Categoria",
        help_text="Descrição detalhada da categoria"
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name="Ativa",
        help_text="Indica se a categoria está ativa"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )

    class Meta:
        verbose_name = "Categoria de Patrimônio"
        verbose_name_plural = "Categorias de Patrimônio"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class ItemPatrimonio(models.Model):
    """Itens do patrimônio histórico de Muzambinho - edificações, locais históricos, etc."""
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('em_restauracao', 'Em Restauração'),
        ('emprestado', 'Emprestado'),
        ('inativo', 'Inativo'),
    ]
    
    ESTADO_CONSERVACAO_CHOICES = [
        ('excelente', 'Excelente'),
        ('bom', 'Bom'),
        ('regular', 'Regular'),
        ('ruim', 'Ruim'),
        ('pessimo', 'Péssimo'),
    ]

    nome = models.CharField(
        max_length=255,
        verbose_name="Nome do Item Patrimonial",
        help_text="Nome do item do patrimônio histórico"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="itens_patrimonio",
        verbose_name="Categoria",
        help_text="Categoria do item patrimonial"
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada do item patrimonial"
    )
    origem = models.CharField(
        max_length=255,
        verbose_name="Origem",
        help_text="Origem ou procedência do item"
    )
    data_origem = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Origem",
        help_text="Data estimada de criação/origem do item"
    )
    numero_registro = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Número de Registro",
        help_text="Número único de registro do item patrimonial"
    )
    estado_conservacao = models.CharField(
        max_length=15,
        choices=ESTADO_CONSERVACAO_CHOICES,
        default='bom',
        verbose_name="Estado de Conservação"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ativo',
        verbose_name="Status"
    )
    localizacao_fisica = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Localização Física",
        help_text="Endereço ou local físico onde o patrimônio está localizado"
    )
    valor_estimado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Valor Estimado",
        help_text="Valor estimado do patrimônio (opcional)"
    )
    modelo_3d = models.FileField(
        upload_to='modelos_3d/',
        blank=True,
        null=True,
        verbose_name="Modelo 3D",
        help_text="Arquivo do modelo 3D (.glb, .gltf, .obj)"
    )
    data_adicao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Adição",
        help_text="Data em que o item foi adicionado ao sistema"
    )
    usuario_adicionado = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="itens_patrimonio_adicionados",
        verbose_name="Usuário que Adicionou",
        help_text="Usuário que adicionou o item patrimonial"
    )

    class Meta:
        verbose_name = "Item do Patrimônio"
        verbose_name_plural = "Itens do Patrimônio"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.numero_registro})"

    def clean(self):
        """Validate item data."""
        if self.data_origem and self.data_origem > timezone.now().date():
            raise ValidationError(
                'Data de origem não pode ser no futuro.'
            )


class ImagemItemPatrimonio(models.Model):
    """Imagens dos itens do patrimônio histórico."""
    
    item_patrimonio = models.ForeignKey(
        ItemPatrimonio,
        on_delete=models.CASCADE,
        related_name="imagens",
        verbose_name="Item do Patrimônio",
        help_text="Item do patrimônio relacionado à imagem"
    )
    imagem = models.ImageField(
        upload_to='imagens_patrimonio/',
        verbose_name="Imagem",
        help_text="Imagem do item patrimonial"
    )
    legenda = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Legenda",
        help_text="Legenda ou descrição da imagem"
    )
    eh_principal = models.BooleanField(
        default=False,
        verbose_name="Imagem Principal",
        help_text="Marcar como imagem principal do item"
    )
    data_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Upload"
    )

    class Meta:
        verbose_name = "Imagem do Item do Patrimônio"
        verbose_name_plural = "Imagens dos Itens do Patrimônio"
        ordering = ['item_patrimonio__nome', '-eh_principal', 'data_upload']

    def __str__(self):
        return f"Imagem de {self.item_patrimonio.nome}"


class Patrimonio(models.Model):
    """Model representing historical heritage/patrimony."""
    
    TIPO_PATRIMONIO_CHOICES = [
        ('material', 'Material'),
        ('imaterial', 'Imaterial'),
        ('arquitetonico', 'Arquitetônico'),
        ('paisagistico', 'Paisagístico'),
        ('arqueologico', 'Arqueológico'),
    ]
    
    STATUS_CHOICES = [
        ('preservado', 'Preservado'),
        ('em_risco', 'Em Risco'),
        ('restauracao', 'Em Restauração'),
        ('perdido', 'Perdido'),
    ]

    nome = models.CharField(
        max_length=255,
        verbose_name="Nome do Patrimônio",
        help_text="Nome do patrimônio histórico"
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada do patrimônio"
    )
    tipo = models.CharField(
        max_length=15,
        choices=TIPO_PATRIMONIO_CHOICES,
        verbose_name="Tipo de Patrimônio"
    )
    data_origem = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Origem",
        help_text="Data estimada de origem do patrimônio"
    )
    localizacao = models.CharField(
        max_length=255,
        verbose_name="Localização",
        help_text="Localização geográfica do patrimônio"
    )
    coordenadas = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Coordenadas GPS",
        help_text="Coordenadas GPS (opcional)"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='preservado',
        verbose_name="Status de Conservação"
    )
    importancia_historica = models.TextField(
        blank=True,
        verbose_name="Importância Histórica",
        help_text="Descrição da importância histórica do patrimônio"
    )
    data_adicao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Adição",
        help_text="Data em que o patrimônio foi adicionado ao sistema"
    )
    usuario_adicionado = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="patrimonios_adicionados",
        verbose_name="Usuário que Adicionou",
        help_text="Usuário que adicionou o patrimônio ao sistema"
    )

    class Meta:
        verbose_name = "Patrimônio"
        verbose_name_plural = "Patrimônios"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.localizacao}"

    def clean(self):
        """Validate patrimony data."""
        if self.data_origem and self.data_origem > timezone.now().date():
            raise ValidationError(
                'Data de origem não pode ser no futuro.'
            )


class ImagemPatrimonio(models.Model):
    """Model representing images of patrimony."""
    
    patrimonio = models.ForeignKey(
        Patrimonio,
        on_delete=models.CASCADE,
        related_name="imagens",
        verbose_name="Patrimônio",
        help_text="Patrimônio relacionado à imagem"
    )
    imagem = models.ImageField(
        upload_to='imagens_patrimonio/',
        verbose_name="Imagem",
        help_text="Imagem do patrimônio"
    )
    legenda = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Legenda",
        help_text="Legenda ou descrição da imagem"
    )
    eh_principal = models.BooleanField(
        default=False,
        verbose_name="Imagem Principal",
        help_text="Marcar como imagem principal do patrimônio"
    )
    data_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Upload"
    )

    class Meta:
        verbose_name = "Imagem do Patrimônio"
        verbose_name_plural = "Imagens dos Patrimônios"
        ordering = ['patrimonio__nome', '-eh_principal', 'data_upload']

    def __str__(self):
        return f"Imagem de {self.patrimonio.nome}"


class DocumentoHistorico(models.Model):
    """Model representing historical documents."""
    
    TIPO_DOCUMENTO_CHOICES = [
        ('certidao', 'Certidão'),
        ('ata', 'Ata'),
        ('carta', 'Carta'),
        ('decreto', 'Decreto'),
        ('lei', 'Lei'),
        ('fotografia', 'Fotografia'),
        ('mapa', 'Mapa'),
        ('jornal', 'Jornal'),
        ('revista', 'Revista'),
        ('livro', 'Livro'),
        ('outro', 'Outro'),
    ]

    titulo = models.CharField(
        max_length=255,
        verbose_name="Título",
        help_text="Título do documento histórico"
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição detalhada do documento histórico"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="documentos",
        verbose_name="Categoria",
        help_text="Categoria do documento histórico"
    )
    tipo_documento = models.CharField(
        max_length=15,
        choices=TIPO_DOCUMENTO_CHOICES,
        verbose_name="Tipo de Documento"
    )
    autor = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Autor",
        help_text="Autor do documento histórico"
    )
    data_origem = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Origem",
        help_text="Data de criação do documento original"
    )
    local_origem = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Local de Origem",
        help_text="Local onde o documento foi criado"
    )
    numero_paginas = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Número de Páginas",
        help_text="Quantidade de páginas do documento"
    )
    documento = models.FileField(
        upload_to='documentos_historicos/',
        verbose_name="Arquivo",
        help_text="Arquivo digitalizado do documento histórico"
    )
    data_adicao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Adição",
        help_text="Data em que o documento foi adicionado ao acervo"
    )
    usuario_adicionado = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="documentos_adicionados",
        verbose_name="Usuário que Adicionou",
        help_text="Usuário que adicionou o documento ao acervo"
    )

    class Meta:
        verbose_name = "Documento Histórico"
        verbose_name_plural = "Documentos Históricos"
        ordering = ['-data_origem', 'titulo']

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_documento_display()})"

    def clean(self):
        """Validate document data."""
        if self.data_origem and self.data_origem > timezone.now().date():
            raise ValidationError(
                'Data de origem não pode ser no futuro.'
            )
