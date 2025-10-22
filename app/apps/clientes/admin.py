# -*- coding: utf-8 -*-
"""
Admin do app Clientes
"""

from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'email', 'telefone', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em', 'data_nascimento']
    search_fields = ['nome', 'cpf', 'email']
    readonly_fields = ['criado_em', 'atualizado_em']
    ordering = ['nome']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'cpf', 'data_nascimento')
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



