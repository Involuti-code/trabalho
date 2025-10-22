# -*- coding: utf-8 -*-
"""
Admin do app Parcelas
"""

from django.contrib import admin
from .models import Parcela


@admin.register(Parcela)
class ParcelaAdmin(admin.ModelAdmin):
    list_display = ['numero_parcela', 'data_vencimento', 'valor', 'status', 'data_pagamento', 'ativo']
    list_filter = ['status', 'data_vencimento', 'data_pagamento', 'ativo', 'criado_em']
    search_fields = ['observacoes']
    readonly_fields = ['criado_em', 'atualizado_em']
    ordering = ['data_vencimento', 'numero_parcela']
    
    fieldsets = (
        ('Informações da Parcela', {
            'fields': ('numero_parcela', 'data_vencimento', 'valor', 'status')
        }),
        ('Pagamento', {
            'fields': ('data_pagamento', 'valor_pago')
        }),
        ('Controle', {
            'fields': ('ativo', 'observacoes')
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em', 'criado_por', 'atualizado_por'),
            'classes': ('collapse',)
        }),
    )



