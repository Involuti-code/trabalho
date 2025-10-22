# -*- coding: utf-8 -*-
"""
Admin do app Tipos de Despesa
"""

from django.contrib import admin
from .models import TipoDespesa


@admin.register(TipoDespesa)
class TipoDespesaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'categoria', 'cor', 'ativo', 'criado_em']
    list_filter = ['categoria', 'ativo', 'criado_em']
    search_fields = ['nome', 'codigo', 'descricao', 'palavras_chave']
    readonly_fields = ['criado_em', 'atualizado_em']
    ordering = ['categoria', 'nome']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'codigo', 'descricao', 'categoria')
        }),
        ('Classificação Automática', {
            'fields': ('palavras_chave',),
            'description': 'Palavras-chave separadas por vírgula para classificação automática'
        }),
        ('Aparência', {
            'fields': ('cor',)
        }),
        ('Controle', {
            'fields': ('ativo',)
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em', 'criado_por', 'atualizado_por'),
            'classes': ('collapse',)
        }),
    )



