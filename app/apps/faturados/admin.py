# -*- coding: utf-8 -*-
"""
Admin do app Faturados
"""

from django.contrib import admin
from .models import Faturado


@admin.register(Faturado)
class FaturadoAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'cpf', 'email', 'telefone', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome_completo', 'cpf', 'email']
    readonly_fields = ['criado_em', 'atualizado_em']
    ordering = ['nome_completo']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome_completo', 'cpf')
        }),
        ('Contato', {
            'fields': ('email', 'telefone', 'endereco')
        }),
        ('Controle', {
            'fields': ('ativo', 'observacoes')
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em', 'criado_por', 'atualizado_por'),
            'classes': ('collapse',)
        }),
    )



