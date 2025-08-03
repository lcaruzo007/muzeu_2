#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('.')
django.setup()

from apps.acervo.models import ItemAcervo, CategoriaAcervo
from apps.personalidades.models import Personalidade
from apps.arte.models import ObraArte
from django.db.models import Q

print("=== TESTE DE DADOS MUSICAIS ===\n")

# 1. Verificar se existem categorias relacionadas à música
print("1. Categorias relacionadas à música:")
categorias_musica = CategoriaAcervo.objects.filter(nome__icontains='música')
if categorias_musica:
    for cat in categorias_musica:
        print(f"   - {cat.nome} (ID: {cat.id})")
else:
    print("   Nenhuma categoria com 'música' encontrada")

categorias_instrumento = CategoriaAcervo.objects.filter(nome__icontains='instrumento')
if categorias_instrumento:
    for cat in categorias_instrumento:
        print(f"   - {cat.nome} (ID: {cat.id})")

print(f"\nTotal de categorias: {CategoriaAcervo.objects.count()}")

# 2. Verificar itens do acervo relacionados à música
print("\n2. Itens do acervo relacionados à música:")
itens_musica = ItemAcervo.objects.filter(
    Q(titulo__icontains='música') | Q(descricao__icontains='música') |
    Q(tipo_item='instrumento')
)
print(f"   Total de itens musicais: {itens_musica.count()}")
for item in itens_musica[:5]:  # Mostrar primeiros 5
    print(f"   - {item.titulo} (Tipo: {item.tipo_item})")

# 3. Verificar itens com arquivo de áudio
print("\n3. Itens com arquivo de áudio:")
itens_com_audio = ItemAcervo.objects.exclude(arquivo_audio='').exclude(arquivo_audio__isnull=True)
print(f"   Total de itens com áudio: {itens_com_audio.count()}")
for item in itens_com_audio[:5]:
    print(f"   - {item.titulo}: {item.arquivo_audio}")

# 4. Verificar personalidades musicais
print("\n4. Personalidades musicais:")
personalidades_musica = Personalidade.objects.filter(
    Q(tipo='musico') | Q(areas_atuacao__nome__icontains='música')
).distinct()
print(f"   Total de personalidades musicais: {personalidades_musica.count()}")
for pers in personalidades_musica[:5]:
    print(f"   - {pers.nome} (Tipo: {pers.tipo})")

# 5. Verificar depoimentos musicais
print("\n5. Depoimentos musicais:")
depoimentos_musicais = Personalidade.objects.filter(
    Q(audio_depoimento__isnull=False) & 
    (Q(tipo='musico') | Q(areas_atuacao__nome__icontains='música'))
).exclude(audio_depoimento='').distinct()
print(f"   Total de depoimentos musicais: {depoimentos_musicais.count()}")
for dep in depoimentos_musicais[:5]:
    print(f"   - {dep.nome}: {dep.audio_depoimento}")

# 6. Verificar obras de arte musicais
print("\n6. Obras de arte relacionadas à música:")
try:
    obras_musicais = ObraArte.objects.filter(
        Q(titulo__icontains='música') | Q(descricao__icontains='música'),
        status='ativo'
    )
    print(f"   Total de obras musicais: {obras_musicais.count()}")
    for obra in obras_musicais[:5]:
        print(f"   - {obra.titulo} (Status: {obra.status})")
except Exception as e:
    print(f"   Erro ao buscar obras: {e}")

print("\n=== FIM DO TESTE ===")
