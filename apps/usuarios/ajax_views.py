from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from apps.usuarios.models import Perfil
import json

@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    """View para registrar novo usuário via AJAX"""
    try:
        data = json.loads(request.body)
        
        # Validar dados obrigatórios
        required_fields = ['first_name', 'last_name', 'email', 'cpf', 'password1', 'password2']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'Campo {field} é obrigatório'
                }, status=400)
        
        # Validar senhas
        if data['password1'] != data['password2']:
            return JsonResponse({
                'success': False,
                'message': 'As senhas não coincidem'
            }, status=400)
        
        # Verificar se email já existe
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({
                'success': False,
                'message': 'Este email já está em uso'
            }, status=400)
        
        # Verificar se CPF já existe
        if Perfil.objects.filter(cpf=data['cpf']).exists():
            return JsonResponse({
                'success': False,
                'message': 'Este CPF já está cadastrado'
            }, status=400)
        
        # Criar usuário
        user = User.objects.create_user(
            username=data['email'],  # Usar email como username
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password1']
        )
        
        # Criar perfil
        perfil = Perfil.objects.create(
            user=user,
            cpf=data['cpf'],
            telefone=data.get('telefone', '')
        )
        
        # Fazer login automático
        user = authenticate(request, username=data['email'], password=data['password1'])
        if user:
            login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Conta criada com sucesso!',
            'redirect': '/'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dados inválidos'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Erro interno do servidor'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    """View para login de usuário via AJAX"""
    try:
        data = json.loads(request.body)
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({
                'success': False,
                'message': 'Username e senha são obrigatórios'
            }, status=400)
        
        # Tentar autenticar por email ou CPF
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Login realizado com sucesso!',
                'redirect': '/dashboard/' if user.is_staff else '/'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Credenciais inválidas'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dados inválidos'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Erro interno do servidor'
        }, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_patrimonio(request):
    """View para adicionar patrimônio via AJAX"""
    try:
        # Para upload de arquivos, usar request.POST e request.FILES
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        localizacao = request.POST.get('localizacao')
        ano_construcao = request.POST.get('ano_construcao')
        foto = request.FILES.get('foto')
        modelo_3d = request.FILES.get('modelo_3d')
        
        if not nome or not descricao:
            return JsonResponse({
                'success': False,
                'message': 'Nome e descrição são obrigatórios'
            }, status=400)
        
        # Importar o modelo aqui para evitar circular import
        from apps.patrimonio.models import ItemPatrimonio, Categoria
        
        # Criar categoria padrão se não existir
        categoria, created = Categoria.objects.get_or_create(
            nome='Geral',
            defaults={'descricao': 'Categoria geral para patrimônios'}
        )
        
        # Gerar número de registro único
        import uuid
        numero_registro = f"PAT-{uuid.uuid4().hex[:8].upper()}"
        
        # Criar item do patrimônio
        item = ItemPatrimonio.objects.create(
            nome=nome,
            categoria=categoria,
            descricao=descricao,
            origem=localizacao or 'Não especificado',
            numero_registro=numero_registro,
            localizacao_fisica=localizacao or '',
            usuario_adicionado=request.user
        )
        
        # Adicionar ano de construção se fornecido
        if ano_construcao:
            try:
                from datetime import date
                item.data_origem = date(int(ano_construcao), 1, 1)
                item.save()
            except ValueError:
                pass
        
        # Adicionar modelo 3D se fornecido
        if modelo_3d:
            item.modelo_3d = modelo_3d
            item.save()
        
        # Adicionar foto se fornecida
        if foto:
            from apps.patrimonio.models import ImagemItemPatrimonio
            ImagemItemPatrimonio.objects.create(
                item_patrimonio=item,
                imagem=foto,
                eh_principal=True,
                legenda=f"Foto principal de {nome}"
            )
        
        return JsonResponse({
            'success': True,
            'message': 'Patrimônio adicionado com sucesso!',
            'patrimonio_id': item.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao adicionar patrimônio: {str(e)}'
        }, status=500)

def get_patrimonio_data(request, patrimonio_id):
    """View para obter dados do patrimônio via AJAX"""
    try:
        from apps.patrimonio.models import ItemPatrimonio
        
        item = ItemPatrimonio.objects.get(id=patrimonio_id)
        
        data = {
            'success': True,
            'patrimonio': {
                'id': item.id,
                'nome': item.nome,
                'descricao': item.descricao,
                'localizacao': item.localizacao_fisica,
                'categoria': item.categoria.nome,
                'estado_conservacao': item.get_estado_conservacao_display(),
                'data_origem': item.data_origem.year if item.data_origem else None,
                'numero_registro': item.numero_registro,
                'valor_estimado': str(item.valor_estimado) if item.valor_estimado else None,
                'modelo_3d_url': item.modelo_3d.url if item.modelo_3d else None,
                'imagem_principal': None
            }
        }
        
        # Adicionar imagem principal se existir
        imagem_principal = item.imagens.filter(eh_principal=True).first()
        if imagem_principal:
            data['patrimonio']['imagem_principal'] = imagem_principal.imagem.url
        elif item.imagens.exists():
            data['patrimonio']['imagem_principal'] = item.imagens.first().imagem.url
        
        return JsonResponse(data)
        
    except ItemPatrimonio.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Patrimônio não encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Erro interno do servidor'
        }, status=500)

def list_patrimonios(request):
    """View para listar patrimônios via AJAX"""
    try:
        from apps.patrimonio.models import ItemPatrimonio
        
        items = ItemPatrimonio.objects.select_related('categoria').prefetch_related('imagens')
        
        patrimonios = []
        for item in items:
            imagem_url = None
            imagem_principal = item.imagens.filter(eh_principal=True).first()
            if imagem_principal:
                imagem_url = imagem_principal.imagem.url
            elif item.imagens.exists():
                imagem_url = item.imagens.first().imagem.url
            
            patrimonios.append({
                'id': item.id,
                'nome': item.nome,
                'localizacao': item.localizacao_fisica,
                'estado_conservacao': item.get_estado_conservacao_display(),
                'categoria': item.categoria.nome,
                'imagem_url': imagem_url,
                'modelo_3d_disponivel': bool(item.modelo_3d)
            })
        
        return JsonResponse({
            'success': True,
            'patrimonios': patrimonios
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Erro interno do servidor'
        }, status=500)
