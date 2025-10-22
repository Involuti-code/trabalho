# -*- coding: utf-8 -*-
"""
Admin do app Fornecedores
"""

from django.contrib import admin
from .models import Fornecedor


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['razao_social', 'fantasia', 'cnpj', 'email', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['razao_social', 'fantasia', 'cnpj', 'email']
    readonly_fields = ['criado_em', 'atualizado_em']
    ordering = ['razao_social']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('razao_social', 'fantasia', 'cnpj')
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



