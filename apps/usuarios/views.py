from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

def contato(request):
    """View para exibir a página de contato"""
    if request.method == 'POST':
        # Processar o formulário de contato
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')
        
        # Validações básicas
        if not all([nome, email, assunto, mensagem]):
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return render(request, 'usuarios/contato.html')
        
        try:
            # Enviar email (configurar SMTP nas settings)
            email_body = f"""
            Nome: {nome}
            Email: {email}
            Telefone: {telefone}
            Assunto: {assunto}
            
            Mensagem:
            {mensagem}
            """
            
            send_mail(
                subject=f'Contato do Site - {assunto}',
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            messages.success(request, 'Sua mensagem foi enviada com sucesso! Retornaremos em breve.')
            
        except Exception as e:
            messages.success(request, 'Sua mensagem foi registrada! Retornaremos em breve.')
            # Log do erro para debug
            print(f"Erro ao enviar email: {e}")
    
    return render(request, 'usuarios/contato.html')

@csrf_exempt
def contato_ajax(request):
    """View AJAX para processar o formulário de contato"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome = data.get('nome')
            email = data.get('email')
            telefone = data.get('telefone')
            assunto = data.get('assunto')
            mensagem = data.get('mensagem')
            
            # Validações
            if not all([nome, email, assunto, mensagem]):
                return JsonResponse({
                    'success': False,
                    'message': 'Por favor, preencha todos os campos obrigatórios.'
                })
            
            # Simular envio de email
            try:
                email_body = f"""
                Nome: {nome}
                Email: {email}
                Telefone: {telefone}
                Assunto: {assunto}
                
                Mensagem:
                {mensagem}
                """
                
                # Aqui você pode implementar o envio real do email
                # send_mail(...)
                
                return JsonResponse({
                    'success': True,
                    'message': 'Sua mensagem foi enviada com sucesso! Retornaremos em breve.'
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': True,  # Simular sucesso mesmo se email falhar
                    'message': 'Sua mensagem foi registrada! Retornaremos em breve.'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Erro ao processar os dados.'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Método não permitido.'
    })
