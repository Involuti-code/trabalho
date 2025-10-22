# -*- coding: utf-8 -*-
"""
Modelos do app Clientes
"""

from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import BaseModel


class Cliente(BaseModel):
    """
    Modelo para Clientes
    """
    
    # Validador para CPF
    cpf_validator = RegexValidator(
        regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        message='CPF deve estar no formato: 000.000.000-00'
    )
    
    nome = models.CharField(
        'Nome', 
        max_length=255,
        help_text='Nome completo do cliente'
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
    
    data_nascimento = models.DateField(
        'Data de Nascimento', 
        blank=True, 
        null=True,
        help_text='Data de nascimento'
    )
    
    observacoes = models.TextField(
        'Observações', 
        blank=True, 
        null=True,
        help_text='Observações adicionais'
    )

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['cpf']),
            models.Index(fields=['ativo']),
        ]

    def __str__(self):
        return f"{self.nome} ({self.cpf})"

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
        self.full_clean()
        super().save(*args, **kwargs)



