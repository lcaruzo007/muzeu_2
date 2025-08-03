from django.db import models
from django.urls import reverse


class AreaPesquisa(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Área de Pesquisa")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    
    class Meta:
        verbose_name = "Área de Pesquisa"
        verbose_name_plural = "Áreas de Pesquisa"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Pesquisador(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    instituicao = models.CharField(max_length=200, blank=True, verbose_name="Instituição")
    titulacao = models.CharField(max_length=100, blank=True, verbose_name="Titulação")
    areas_interesse = models.ManyToManyField(AreaPesquisa, blank=True, verbose_name="Áreas de Interesse")
    biografia = models.TextField(blank=True, verbose_name="Biografia")
    foto = models.ImageField(upload_to='pesquisadores/', blank=True, verbose_name="Foto")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Pesquisador"
        verbose_name_plural = "Pesquisadores"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class TipoPesquisa(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Tipo de Pesquisa")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    
    class Meta:
        verbose_name = "Tipo de Pesquisa"
        verbose_name_plural = "Tipos de Pesquisa"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Pesquisa(models.Model):
    STATUS_CHOICES = [
        ('planejamento', 'Em Planejamento'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('publicada', 'Publicada'),
        ('arquivada', 'Arquivada'),
    ]
    
    titulo = models.CharField(max_length=300, verbose_name="Título")
    resumo = models.TextField(verbose_name="Resumo")
    area = models.ForeignKey(AreaPesquisa, on_delete=models.CASCADE, verbose_name="Área")
    tipo = models.ForeignKey(TipoPesquisa, on_delete=models.CASCADE, verbose_name="Tipo")
    pesquisador_principal = models.ForeignKey(Pesquisador, on_delete=models.CASCADE, related_name='pesquisas_principais', verbose_name="Pesquisador Principal")
    colaboradores = models.ManyToManyField(Pesquisador, blank=True, related_name='colaboracoes', verbose_name="Colaboradores")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(null=True, blank=True, verbose_name="Data de Fim")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejamento', verbose_name="Status")
    palavras_chave = models.CharField(max_length=500, blank=True, verbose_name="Palavras-chave")
    metodologia = models.TextField(blank=True, verbose_name="Metodologia")
    resultados = models.TextField(blank=True, verbose_name="Resultados")
    conclusoes = models.TextField(blank=True, verbose_name="Conclusões")
    financiamento = models.CharField(max_length=200, blank=True, verbose_name="Fonte de Financiamento")
    publica = models.BooleanField(default=False, verbose_name="Pesquisa Pública")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pesquisa"
        verbose_name_plural = "Pesquisas"
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('pesquisa:detalhe', kwargs={'pk': self.pk})


class DocumentoPesquisa(models.Model):
    TIPO_CHOICES = [
        ('artigo', 'Artigo'),
        ('relatorio', 'Relatório'),
        ('apresentacao', 'Apresentação'),
        ('dados', 'Base de Dados'),
        ('imagem', 'Imagem'),
        ('video', 'Vídeo'),
        ('audio', 'Áudio'),
        ('outro', 'Outro'),
    ]
    
    pesquisa = models.ForeignKey(Pesquisa, on_delete=models.CASCADE, related_name='documentos', verbose_name="Pesquisa")
    titulo = models.CharField(max_length=200, verbose_name="Título")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='outro', verbose_name="Tipo")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    arquivo = models.FileField(upload_to='pesquisa/documentos/', verbose_name="Arquivo")
    publico = models.BooleanField(default=False, verbose_name="Público")
    adicionado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Documento de Pesquisa"
        verbose_name_plural = "Documentos de Pesquisa"
        ordering = ['-adicionado_em']
    
    def __str__(self):
        return f"{self.pesquisa.titulo} - {self.titulo}"


class Genealogia(models.Model):
    nome_pessoa = models.CharField(max_length=200, verbose_name="Nome da Pessoa")
    nome_pai = models.CharField(max_length=200, blank=True, verbose_name="Nome do Pai")
    nome_mae = models.CharField(max_length=200, blank=True, verbose_name="Nome da Mãe")
    data_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    local_nascimento = models.CharField(max_length=200, blank=True, verbose_name="Local de Nascimento")
    data_falecimento = models.DateField(null=True, blank=True, verbose_name="Data de Falecimento")
    local_falecimento = models.CharField(max_length=200, blank=True, verbose_name="Local de Falecimento")
    profissao = models.CharField(max_length=200, blank=True, verbose_name="Profissão")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    fonte_informacao = models.CharField(max_length=300, blank=True, verbose_name="Fonte da Informação")
    verificado = models.BooleanField(default=False, verbose_name="Informação Verificada")
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Genealogia"
        verbose_name_plural = "Genealogias"
        ordering = ['nome_pessoa']
    
    def __str__(self):
        return self.nome_pessoa
