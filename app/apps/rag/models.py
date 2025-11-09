# -*- coding: utf-8 -*-
"""
Modelos do app RAG
"""

from django.db import models
from apps.core.models import BaseModel


class ConsultaRAG(BaseModel):
    """
    Modelo para armazenar consultas RAG realizadas
    """
    
    TIPO_RAG_SIMPLES = 'SIMPLES'
    TIPO_RAG_EMBEDDINGS = 'EMBEDDINGS'
    
    TIPO_CHOICES = [
        (TIPO_RAG_SIMPLES, 'RAG Simples'),
        (TIPO_RAG_EMBEDDINGS, 'RAG com Embeddings'),
    ]
    
    pergunta = models.TextField(
        'Pergunta',
        help_text='Pergunta realizada pelo usuário'
    )
    
    tipo_rag = models.CharField(
        'Tipo de RAG',
        max_length=20,
        choices=TIPO_CHOICES,
        default=TIPO_RAG_SIMPLES,
        help_text='Tipo de RAG utilizado'
    )
    
    contexto_retornado = models.TextField(
        'Contexto Retornado',
        blank=True,
        null=True,
        help_text='Contexto retornado pela busca RAG'
    )
    
    resposta_llm = models.TextField(
        'Resposta do LLM',
        blank=True,
        null=True,
        help_text='Resposta elaborada pelo LLM'
    )
    
    tempo_resposta = models.FloatField(
        'Tempo de Resposta (segundos)',
        null=True,
        blank=True,
        help_text='Tempo de processamento em segundos'
    )
    
    class Meta:
        verbose_name = 'Consulta RAG'
        verbose_name_plural = 'Consultas RAG'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['tipo_rag']),
            models.Index(fields=['criado_em']),
        ]

    def __str__(self):
        return f"Consulta RAG - {self.pergunta[:50]}..."

