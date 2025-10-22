# -*- coding: utf-8 -*-
"""
Modelos do app Tipos de Receita
"""

from django.db import models
from apps.core.models import BaseModel


class TipoReceita(BaseModel):
    """
    Modelo para Tipos de Receita
    """
    
    nome = models.CharField(
        'Nome', 
        max_length=255,
        unique=True,
        help_text='Nome do tipo de receita'
    )
    
    descricao = models.TextField(
        'Descrição', 
        blank=True, 
        null=True,
        help_text='Descrição detalhada do tipo de receita'
    )
    
    codigo = models.CharField(
        'Código', 
        max_length=20, 
        unique=True,
        help_text='Código único para identificação'
    )
    
    cor = models.CharField(
        'Cor', 
        max_length=7, 
        default='#007bff',
        help_text='Cor para identificação visual (formato hex: #000000)'
    )

    class Meta:
        verbose_name = 'Tipo de Receita'
        verbose_name_plural = 'Tipos de Receita'
        ordering = ['nome']
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['codigo']),
            models.Index(fields=['ativo']),
        ]

    def __str__(self):
        return f"{self.nome} ({self.codigo})"

    def clean(self):
        """Validações adicionais"""
        from django.core.exceptions import ValidationError
        
        # Validar formato da cor
        if self.cor and not self.cor.startswith('#'):
            raise ValidationError({'cor': 'Cor deve começar com #'})
        
        if self.cor and len(self.cor) != 7:
            raise ValidationError({'cor': 'Cor deve ter 7 caracteres (#RRGGBB)'})

    def save(self, *args, **kwargs):
        """Override save para aplicar validações"""
        self.full_clean()
        super().save(*args, **kwargs)



