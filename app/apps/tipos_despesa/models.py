# -*- coding: utf-8 -*-
"""
Modelos do app Tipos de Despesa
"""

from django.db import models
from apps.core.models import BaseModel, CategoriaDespesa


class TipoDespesa(BaseModel):
    """
    Modelo para Tipos de Despesa
    Baseado nas 9 categorias principais especificadas no projeto
    """
    
    nome = models.CharField(
        'Nome', 
        max_length=255,
        unique=True,
        help_text='Nome do tipo de despesa'
    )
    
    descricao = models.TextField(
        'Descrição', 
        blank=True, 
        null=True,
        help_text='Descrição detalhada do tipo de despesa'
    )
    
    codigo = models.CharField(
        'Código', 
        max_length=20, 
        unique=True,
        help_text='Código único para identificação'
    )
    
    categoria = models.CharField(
        'Categoria',
        max_length=50,
        choices=CategoriaDespesa.choices,
        help_text='Categoria principal da despesa'
    )
    
    cor = models.CharField(
        'Cor', 
        max_length=7, 
        default='#dc3545',
        help_text='Cor para identificação visual (formato hex: #000000)'
    )
    
    # Campos para classificação automática
    palavras_chave = models.TextField(
        'Palavras-chave',
        blank=True,
        null=True,
        help_text='Palavras-chave para classificação automática (separadas por vírgula)'
    )

    class Meta:
        verbose_name = 'Tipo de Despesa'
        verbose_name_plural = 'Tipos de Despesa'
        ordering = ['categoria', 'nome']
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['codigo']),
            models.Index(fields=['categoria']),
            models.Index(fields=['ativo']),
        ]

    def __str__(self):
        return f"{self.nome} - {self.get_categoria_display()}"

    def get_palavras_chave_list(self):
        """Retorna lista de palavras-chave"""
        if self.palavras_chave:
            return [palavra.strip().lower() for palavra in self.palavras_chave.split(',')]
        return []

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
        # Permitir pular validação se skip_validation=True
        if not kwargs.pop('skip_validation', False):
            self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def classificar_por_descricao(cls, descricao):
        """
        Classifica uma despesa baseada na descrição
        Retorna o tipo de despesa mais provável
        """
        if not descricao:
            return None
        
        descricao_lower = descricao.lower()
        
        # Buscar por palavras-chave
        tipos = cls.objects.filter(ativo=True)
        melhor_match = None
        melhor_score = 0
        
        for tipo in tipos:
            palavras_chave = tipo.get_palavras_chave_list()
            score = 0
            
            for palavra in palavras_chave:
                if palavra in descricao_lower:
                    score += 1
            
            if score > melhor_score:
                melhor_score = score
                melhor_match = tipo
        
        return melhor_match



