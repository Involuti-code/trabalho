# -*- coding: utf-8 -*-
"""
Admin do app Tipos de Receita
"""

from django.contrib import admin
from .models import TipoReceita


@admin.register(TipoReceita)
class TipoReceitaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'cor', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'codigo', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']
    ordering = ['nome']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'codigo', 'descricao')
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



