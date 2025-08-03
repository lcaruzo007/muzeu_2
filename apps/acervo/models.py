from django.db import models
from django.urls import reverse


class CategoriaAcervo(models.Model):
    """Categorias para objetos físicos do museu"""
    nome = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Categoria do Acervo"
        verbose_name_plural = "Categorias do Acervo"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class ItemAcervo(models.Model):
    """Objetos físicos, documentos e artefatos da coleção do museu"""
    ESTADO_CHOICES = [
        ('excelente', 'Excelente'),
        ('bom', 'Bom'),
        ('regular', 'Regular'),
        ('ruim', 'Ruim'),
        ('precario', 'Precário'),
    ]
    
    TIPO_ITEM_CHOICES = [
        ('objeto', 'Objeto'),
        ('documento', 'Documento'),
        ('fotografia', 'Fotografia'),
        ('obra_arte', 'Obra de Arte'),
        ('mobiliario', 'Mobiliário'),
        ('instrumento', 'Instrumento'),
        ('vestuario', 'Vestuário'),
        ('ferramenta', 'Ferramenta'),
        ('livro', 'Livro'),
        ('musica', 'Música'),
        ('outros', 'Outros'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    numero_registro = models.CharField(max_length=50, unique=True, verbose_name="Número de Registro")
    categoria = models.ForeignKey(CategoriaAcervo, on_delete=models.CASCADE, verbose_name="Categoria")
    tipo_item = models.CharField(max_length=20, choices=TIPO_ITEM_CHOICES, default='objeto', verbose_name="Tipo de Item")
    descricao = models.TextField(verbose_name="Descrição")
    origem = models.CharField(max_length=200, blank=True, verbose_name="Origem/Procedência")
    data_aproximada = models.CharField(max_length=100, blank=True, verbose_name="Data Aproximada")
    material = models.CharField(max_length=200, blank=True, verbose_name="Material")
    dimensoes = models.CharField(max_length=200, blank=True, verbose_name="Dimensões")
    peso = models.CharField(max_length=100, blank=True, verbose_name="Peso")
    estado_conservacao = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='bom', verbose_name="Estado de Conservação")
    localizacao = models.CharField(max_length=200, blank=True, verbose_name="Localização no Museu")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    doador = models.CharField(max_length=200, blank=True, verbose_name="Doador")
    data_aquisicao = models.DateField(null=True, blank=True, verbose_name="Data de Aquisição")
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor Estimado")
    imagem = models.ImageField(upload_to='acervo/', blank=True, verbose_name="Imagem")
    arquivo_audio = models.FileField(upload_to='acervo/audios/', blank=True, null=True, verbose_name="Arquivo de Áudio")
    arquivo_documento = models.FileField(upload_to='acervo/documentos/', blank=True, null=True, verbose_name="Arquivo do Documento (PDF)")
    disponivel_exposicao = models.BooleanField(default=True, verbose_name="Disponível para Exposição")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Item do Acervo"
        verbose_name_plural = "Itens do Acervo"
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.numero_registro} - {self.titulo}"
    
    def get_absolute_url(self):
        return reverse('acervo:detalhe', kwargs={'pk': self.pk})


class FotoAcervo(models.Model):
    item = models.ForeignKey(ItemAcervo, on_delete=models.CASCADE, related_name='fotos', verbose_name="Item")
    imagem = models.ImageField(upload_to='acervo/fotos/', verbose_name="Imagem")
    descricao = models.CharField(max_length=200, blank=True, verbose_name="Descrição da Foto")
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Foto do Acervo"
        verbose_name_plural = "Fotos do Acervo"
    
    def __str__(self):
        return f"Foto de {self.item.titulo}"
