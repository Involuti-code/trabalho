# -*- coding: utf-8 -*-
"""
Modelos do app Faturados
"""

from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import BaseModel


class Faturado(BaseModel):
    """
    Modelo para Faturados
    Campos obrigatórios conforme especificação:
    - Nome Completo
    - CPF
    """
    
    # Validador para CPF
    cpf_validator = RegexValidator(
        regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        message='CPF deve estar no formato: 000.000.000-00'
    )
    
    nome_completo = models.CharField(
        'Nome Completo', 
        max_length=255,
        help_text='Nome completo do faturado'
    )
    
    cpf = models.CharField(
        'CPF', 
        max_length=14, 
        unique=True,
        validators=[cpf_validator],
        help_text='CPF no formato: 000.000.000-00'
    )
    
    email = models.EmailField(
        'E-mail', 
        blank=True, 
        null=True,
        help_text='E-mail de contato'
    )
    
    telefone = models.CharField(
        'Telefone', 
        max_length=20, 
        blank=True, 
        null=True,
        help_text='Telefone de contato'
    )
    
    endereco = models.TextField(
        'Endereço', 
        blank=True, 
        null=True,
        help_text='Endereço completo'
    )
    
    observacoes = models.TextField(
        'Observações', 
        blank=True, 
        null=True,
        help_text='Observações adicionais'
    )

    class Meta:
        verbose_name = 'Faturado'
        verbose_name_plural = 'Faturados'
        ordering = ['nome_completo']
        indexes = [
            models.Index(fields=['nome_completo']),
            models.Index(fields=['cpf']),
            models.Index(fields=['ativo']),
        ]

    def __str__(self):
        return f"{self.nome_completo} ({self.cpf})"

    def clean(self):
        """Validações adicionais"""
        from django.core.exceptions import ValidationError
        
        # Verificar se CPF é válido (algoritmo básico)
        if self.cpf:
            cpf_limpo = self.cpf.replace('.', '').replace('-', '')
            if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
                raise ValidationError({'cpf': 'CPF deve conter 11 dígitos'})
            
            # Verificar se não é uma sequência de números iguais
            if cpf_limpo == cpf_limpo[0] * 11:
                raise ValidationError({'cpf': 'CPF inválido'})

    def save(self, *args, **kwargs):
        """Override save para aplicar validações"""
        # Permitir pular validação se skip_validation=True
        if not kwargs.pop('skip_validation', False):
            self.full_clean()
        super().save(*args, **kwargs)



