from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class CategoriaNoticia(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    cor = models.CharField(max_length=7, default="#355D9B", verbose_name="Cor (Hex)")
    ativa = models.BooleanField(default=True, verbose_name="Ativa")
    
    class Meta:
        verbose_name = "Categoria de Notícia"
        verbose_name_plural = "Categorias de Notícia"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Noticia(models.Model):
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('revisao', 'Em Revisão'),
        ('publicada', 'Publicada'),
        ('arquivada', 'Arquivada'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    resumo = models.TextField(max_length=300, verbose_name="Resumo")
    conteudo = models.TextField(verbose_name="Conteúdo")
    categoria = models.ForeignKey(CategoriaNoticia, on_delete=models.CASCADE, verbose_name="Categoria")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    imagem_destaque = models.ImageField(upload_to='noticias/', blank=True, verbose_name="Imagem de Destaque")
    tags = models.CharField(max_length=200, blank=True, verbose_name="Tags (separadas por vírgula)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='rascunho', verbose_name="Status")
    destaque = models.BooleanField(default=False, verbose_name="Notícia em Destaque")
    visualizacoes = models.IntegerField(default=0, verbose_name="Visualizações")
    data_publicacao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Publicação")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ['-data_publicacao', '-criado_em']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('noticias:detalhe', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class ImagemNoticia(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='imagens', verbose_name="Notícia")
    imagem = models.ImageField(upload_to='noticias/galeria/', verbose_name="Imagem")
    legenda = models.CharField(max_length=200, blank=True, verbose_name="Legenda")
    credito = models.CharField(max_length=100, blank=True, verbose_name="Crédito")
    ordem = models.IntegerField(default=0, verbose_name="Ordem")
    
    class Meta:
        verbose_name = "Imagem da Notícia"
        verbose_name_plural = "Imagens da Notícia"
        ordering = ['ordem']
    
    def __str__(self):
        return f"Imagem de {self.noticia.titulo}"


class ComentarioNoticia(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='comentarios', verbose_name="Notícia")
    nome = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail")
    comentario = models.TextField(verbose_name="Comentário")
    aprovado = models.BooleanField(default=False, verbose_name="Aprovado")
    comentado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['-comentado_em']
    
    def __str__(self):
        return f"Comentário de {self.nome} em {self.noticia.titulo}"


class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="E-mail")
    nome = models.CharField(max_length=100, blank=True, verbose_name="Nome")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    inscrito_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Assinante Newsletter"
        verbose_name_plural = "Assinantes Newsletter"
        ordering = ['-inscrito_em']
    
    def __str__(self):
        return self.email
