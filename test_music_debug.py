#!/usr/bin/env python
import os
import sys
import django
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('.')
django.setup()

from apps.acervo.views import MusicaView
from apps.acervo.models import ItemAcervo, CategoriaAcervo
from apps.personalidades.models import Personalidade
from apps.arte.models import ObraArte
from django.db.models import Q

print("=== TESTE DA VIEW DE MÚSICA ===\n")

# Primeiro, verificar se temos dados no banco
print("1. Verificando dados no banco:")
print(f"   - Categorias: {CategoriaAcervo.objects.count()}")
print(f"   - Itens do acervo: {ItemAcervo.objects.count()}")
print(f"   - Personalidades: {Personalidade.objects.count()}")
print(f"   - Obras de arte: {ObraArte.objects.count()}")

# Testar as queries da view diretamente
print("\n2. Testando queries da view:")

# Buscar itens relacionados à música
musica_categoria = CategoriaAcervo.objects.filter(nome__icontains='música').first()
print(f"   - Categoria música encontrada: {musica_categoria}")

if musica_categoria:
    itens_musica = ItemAcervo.objects.filter(
        categoria=musica_categoria, 
        ativo=True
    ).select_related('categoria').prefetch_related('fotos')[:12]
else:
    itens_musica = ItemAcervo.objects.filter(
        Q(titulo__icontains='música') | Q(descricao__icontains='música') |
        Q(tipo_item='instrumento'),
        ativo=True
    ).select_related('categoria').prefetch_related('fotos')[:12]

print(f"   - Itens música encontrados: {itens_musica.count()}")
for item in itens_musica:
    print(f"     * {item.titulo} (Categoria: {item.categoria.nome})")

# Buscar itens com arquivos de áudio
try:
    gravacoes_musicais = ItemAcervo.objects.filter(
        arquivo_audio__isnull=False,
        ativo=True
    ).exclude(arquivo_audio='').select_related('categoria')[:12]
    print(f"   - Gravações musicais encontradas: {gravacoes_musicais.count()}")
except Exception as e:
    print(f"   - Erro ao buscar gravações: {e}")

# Buscar depoimentos musicais
depoimentos_musicais = Personalidade.objects.filter(
    Q(audio_depoimento__isnull=False) & 
    (Q(tipo='musico') | Q(areas_atuacao__nome__icontains='música'))
).exclude(audio_depoimento='').distinct()[:6]
print(f"   - Depoimentos musicais encontrados: {depoimentos_musicais.count()}")
for dep in depoimentos_musicais:
    print(f"     * {dep.nome} (Tipo: {dep.tipo})")

# Buscar obras musicais
try:
    obras_musicais = ObraArte.objects.filter(
        Q(titulo__icontains='música') | Q(descricao__icontains='música'),
        status='ativo'
    )[:6]
    print(f"   - Obras musicais encontradas: {obras_musicais.count()}")
    for obra in obras_musicais:
        print(f"     * {obra.titulo}")
except Exception as e:
    print(f"   - Erro ao buscar obras: {e}")

# Agora testar a view completa
print("\n3. Testando a view MusicaView:")
try:
    factory = RequestFactory()
    request = factory.get('/musica/')
    request.user = AnonymousUser()
    
    view = MusicaView()
    view.request = request
    context = view.get_context_data()
    
    print("   - Context data da view:")
    for key, value in context.items():
        if hasattr(value, '__len__') and not isinstance(value, str):
            try:
                print(f"     * {key}: {len(value)} itens")
            except:
                print(f"     * {key}: {value}")
        else:
            print(f"     * {key}: {value}")
            
except Exception as e:
    print(f"   - Erro ao testar view: {e}")
    import traceback
    traceback.print_exc()

print("\n=== FIM DO TESTE ===")
