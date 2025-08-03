#!/usr/bin/env python
import os
import sys
import django
from django.test import RequestFactory

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('.')
django.setup()

from apps.acervo.views import MusicaView
from django.contrib.auth.models import AnonymousUser

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
print("
2. Testando queries da view:")

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
print("
3. Testando a view MusicaView:")
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

print("
=== FIM DO TESTE ===")

# Simular uma requisição
factory = RequestFactory()
request = factory.get('/musica/')
request.user = AnonymousUser()

# Criar instância da view
view = MusicaView()
view.request = request

# Obter dados do contexto
context = view.get_context_data()

print("Dados no contexto da view:")
for key, value in context.items():
    if hasattr(value, '__len__') and not isinstance(value, str):
        print(f"  {key}: {len(value)} itens")
        if len(value) > 0:
            print(f"    Primeiro item: {value[0] if hasattr(value, '__getitem__') else 'N/A'}")
    else:
        print(f"  {key}: {value}")

print("\n=== DETALHES DOS DADOS ===")

# Verificar itens musicais
if 'itens_musica' in context:
    print(f"\nItens musicais ({len(context['itens_musica'])}):")
    for item in context['itens_musica']:
        print(f"  - {item.titulo} (Categoria: {item.categoria.nome}, Ativo: {item.ativo})")

# Verificar gravações musicais
if 'gravacoes_musicais' in context:
    print(f"\nGravações musicais ({len(context['gravacoes_musicais'])}):")
    for gravacao in context['gravacoes_musicais']:
        print(f"  - {gravacao.titulo} (Arquivo: {gravacao.arquivo_audio})")

# Verificar depoimentos
if 'depoimentos_musicais' in context:
    print(f"\nDepoimentos musicais ({len(context['depoimentos_musicais'])}):")
    for depoimento in context['depoimentos_musicais']:
        print(f"  - {depoimento.nome} (Áudio: {depoimento.audio_depoimento})")

# Verificar obras musicais
if 'obras_musicais' in context:
    print(f"\nObras musicais ({len(context['obras_musicais'])}):")
    for obra in context['obras_musicais']:
        print(f"  - {obra.titulo} (Status: {obra.status})")

print("\n=== FIM DO TESTE DA VIEW ===")
