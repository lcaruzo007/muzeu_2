from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re

def validar_cpf(cpf):
    """Validador de CPF brasileiro"""
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido')
    
    # Validação matemática do CPF
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[9]) != dv1:
        raise ValidationError('CPF inválido')
    
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[10]) != dv2:
        raise ValidationError('CPF inválido')

# Validador de número de registro do museu
validador_numero_registro = RegexValidator(
    regex=r'^[A-Z]{2,3}-\d{4,6}$',
    message='Formato deve ser: ABC-1234 ou AB-12345'
)
