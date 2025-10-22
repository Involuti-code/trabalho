# -*- coding: utf-8 -*-
"""
Modelos do app Fornecedores
"""

from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import BaseModel


class Fornecedor(BaseModel):
    """
    Modelo para Fornecedores
    Campos obrigatórios conforme especificação:
    - Razão Social
    - Fantasia  
    - CNPJ
    """
    
    # Validador para CNPJ
    cnpj_validator = RegexValidator(
        regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
        message='CNPJ deve estar no formato: 00.000.000/0000-00'
    )
    
    razao_social = models.CharField(
        'Razão Social', 
        max_length=255, 
        unique=True,
        help_text='Razão social da empresa'
    )
    
    fantasia = models.CharField(
        'Nome Fantasia', 
        max_length=255,
        blank=True,
        null=True,
        help_text='Nome fantasia da empresa'
    )
    
    cnpj = models.CharField(
        'CNPJ', 
        max_length=18, 
        unique=True,
        validators=[cnpj_validator],
        help_text='CNPJ no formato: 00.000.000/0000-00'
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
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['razao_social']
        indexes = [
            models.Index(fields=['razao_social']),
            models.Index(fields=['cnpj']),
            models.Index(fields=['ativo']),
        ]

    def __str__(self):
        return f"{self.razao_social} ({self.cnpj})"

    def get_nome_display(self):
        """Retorna o nome fantasia se existir, senão a razão social"""
        return self.fantasia or self.razao_social

    def clean(self):
        """Validações adicionais"""
        from django.core.exceptions import ValidationError
        
        # Verificar se CNPJ é válido (algoritmo básico)
        if self.cnpj:
            cnpj_limpo = self.cnpj.replace('.', '').replace('/', '').replace('-', '')
            if len(cnpj_limpo) != 14 or not cnpj_limpo.isdigit():
                raise ValidationError({'cnpj': 'CNPJ deve conter 14 dígitos'})
            
            # Verificar se não é uma sequência de números iguais
            if cnpj_limpo == cnpj_limpo[0] * 14:
                raise ValidationError({'cnpj': 'CNPJ inválido'})

    def save(self, *args, **kwargs):
        """Override save para aplicar validações"""
        self.full_clean()
        super().save(*args, **kwargs)



