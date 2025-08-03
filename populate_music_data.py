#!/usr/bin/env python
import os
import sys
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('.')
django.setup()

from apps.acervo.models import ItemAcervo, CategoriaAcervo
from apps.personalidades.models import Personalidade, AreaAtuacao
from apps.arte.models import ObraArte, Artista, TecnicaArtistica

print("=== POPULANDO BANCO COM DADOS MUSICAIS ===\n")

# 1. Criar categorias musicais
print("1. Criando categorias musicais...")
categoria_musica, created = CategoriaAcervo.objects.get_or_create(
    nome="Instrumentos Musicais",
    defaults={'descricao': 'Instrumentos musicais tradicionais e históricos'}
)
print(f"   - Categoria 'Instrumentos Musicais': {'criada' if created else 'já existia'}")

categoria_gravacao, created = CategoriaAcervo.objects.get_or_create(
    nome="Gravações Musicais",
    defaults={'descricao': 'Gravações históricas e tradicionais'}
)
print(f"   - Categoria 'Gravações Musicais': {'criada' if created else 'já existia'}")

# 2. Criar áreas de atuação
print("\n2. Criando áreas de atuação...")
area_musica, created = AreaAtuacao.objects.get_or_create(
    nome="Música",
    defaults={'descricao': 'Área musical e composição', 'icone': 'music', 'cor': '#6B2C26'}
)
print(f"   - Área 'Música': {'criada' if created else 'já existia'}")

# 3. Criar itens musicais do acervo
print("\n3. Criando itens musicais...")
instrumentos = [
    {
        'titulo': 'Violão Clássico Antigo',
        'numero_registro': 'MUS001',
        'categoria': categoria_musica,
        'tipo_item': 'instrumento',
        'descricao': 'Violão clássico do século XIX, pertencente a um músico local famoso.',
        'origem': 'Muzambinho - MG',
        'data_aproximada': '1890',
        'material': 'Madeira (cedro e jacarandá)',
        'dimensoes': '100cm x 37cm',
    },
    {
        'titulo': 'Bandolim Tradicional',
        'numero_registro': 'MUS002',
        'categoria': categoria_musica,
        'tipo_item': 'instrumento',
        'descricao': 'Bandolim usado nas serenatas tradicionais de Muzambinho.',
        'origem': 'Muzambinho - MG',
        'data_aproximada': '1920',
        'material': 'Madeira',
        'dimensoes': '60cm x 20cm',
    },
    {
        'titulo': 'Sanfona Antiga',
        'numero_registro': 'MUS003',
        'categoria': categoria_musica,
        'tipo_item': 'instrumento',
        'descricao': 'Sanfona utilizada em festivais folclóricos locais.',
        'origem': 'Muzambinho - MG',
        'data_aproximada': '1950',
        'material': 'Metal e madeira',
        'dimensoes': '40cm x 30cm x 20cm',
    }
]

for inst_data in instrumentos:
    instrumento, created = ItemAcervo.objects.get_or_create(
        numero_registro=inst_data['numero_registro'],
        defaults=inst_data
    )
    print(f"   - {inst_data['titulo']}: {'criado' if created else 'já existia'}")

# 4. Criar personalidades musicais
print("\n4. Criando personalidades musicais...")
personalidades = [
    {
        'nome_completo': 'João da Silva Santos',
        'nome_artistico': 'João Violeiro',
        'tipo': 'musico',
        'data_nascimento': date(1930, 5, 15),
        'local_nascimento': 'Muzambinho - MG',
        'resumo': 'Violeiro tradicional, conhecido por suas modas de viola e serenatas.',
        'biografia': 'João da Silva Santos, conhecido como João Violeiro, foi um dos mais respeitados músicos tradicionais de Muzambinho. Suas modas de viola ecoaram pelas ruas da cidade por décadas.',
    },
    {
        'nome_completo': 'Maria das Graças Oliveira',
        'nome_artistico': 'Maria Cantora',
        'tipo': 'musico',
        'data_nascimento': date(1925, 8, 22),
        'local_nascimento': 'Muzambinho - MG',
        'resumo': 'Cantora folclórica, preservou cantigas tradicionais da região.',
        'biografia': 'Maria das Graças dedicou sua vida à preservação das cantigas folclóricas de Muzambinho, ensinando as tradições para as novas gerações.',
    }
]

for pers_data in personalidades:
    personalidade, created = Personalidade.objects.get_or_create(
        nome_completo=pers_data['nome_completo'],
        defaults=pers_data
    )
    if created:
        personalidade.areas_atuacao.add(area_musica)
    print(f"   - {pers_data['nome_artistico']}: {'criada' if created else 'já existia'}")

# 5. Criar técnica artística e artista para obras musicais
print("\n5. Criando dados para obras de arte...")
tecnica_pintura, created = TecnicaArtistica.objects.get_or_create(
    nome="Óleo sobre Tela",
    defaults={'descricao': 'Pintura a óleo sobre tela', 'tipo': 'pintura'}
)

artista, created = Artista.objects.get_or_create(
    nome="Pedro Músico Pintor",
    defaults={
        'status': 'ativo',
        'data_nascimento': date(1940, 3, 10),
        'local_nascimento': 'Muzambinho - MG',
        'biografia': 'Artista local que retratava cenas musicais da cidade.',
        'estilo_artistico': 'Realismo Regional'
    }
)
if created:
    artista.tecnicas_dominadas.add(tecnica_pintura)

print(f"   - Artista 'Pedro Músico Pintor': {'criado' if created else 'já existia'}")

# 6. Criar obras de arte musicais
print("\n6. Criando obras de arte musicais...")
obras = [
    {
        'titulo': 'Serenata na Praça',
        'artista': artista,
        'ano_criacao': date(1960, 1, 1),
        'tecnica': tecnica_pintura,
        'descricao': 'Pintura retratando uma serenata tradicional na praça central de Muzambinho.',
        'dimensoes': '80x60 cm',
        'material_suporte': 'Tela',
        'status': 'ativo'
    },
    {
        'titulo': 'O Violeiro',
        'artista': artista,
        'ano_criacao': date(1965, 1, 1),
        'tecnica': tecnica_pintura,
        'descricao': 'Retrato de um violeiro tradicional tocando sob a luz do luar.',
        'dimensoes': '70x50 cm',
        'material_suporte': 'Tela',
        'status': 'ativo'
    }
]

for obra_data in obras:
    obra, created = ObraArte.objects.get_or_create(
        titulo=obra_data['titulo'],
        artista=obra_data['artista'],
        defaults=obra_data
    )
    print(f"   - {obra_data['titulo']}: {'criada' if created else 'já existia'}")

print("\n=== DADOS MUSICAIS CRIADOS COM SUCESSO! ===")
print(f"Total de categorias: {CategoriaAcervo.objects.count()}")
print(f"Total de itens do acervo: {ItemAcervo.objects.count()}")
print(f"Total de personalidades: {Personalidade.objects.count()}")
print(f"Total de obras de arte: {ObraArte.objects.count()}")
