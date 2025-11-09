# -*- coding: utf-8 -*-
"""
Admin do app RAG
"""

from django.contrib import admin
from .models import ConsultaRAG


@admin.register(ConsultaRAG)
class ConsultaRAGAdmin(admin.ModelAdmin):
    list_display = ['id', 'pergunta', 'tipo_rag', 'tempo_resposta', 'criado_em']
    list_filter = ['tipo_rag', 'criado_em', 'ativo']
    search_fields = ['pergunta', 'resposta_llm']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Consulta', {
            'fields': ('pergunta', 'tipo_rag')
        }),
        ('Resposta', {
            'fields': ('contexto_retornado', 'resposta_llm', 'tempo_resposta')
        }),
        ('Metadados', {
            'fields': ('ativo', 'criado_em', 'atualizado_em')
        }),
    )

