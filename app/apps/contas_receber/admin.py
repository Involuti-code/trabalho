# -*- coding: utf-8 -*-
"""
Admin do app Contas a Receber
"""

from django.contrib import admin
from .models import ContaReceber


class ParcelaInline(admin.TabularInline):
    model = ContaReceber.parcelas.through
    extra = 0


@admin.register(ContaReceber)
class ContaReceberAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'cliente', 'valor_total', 'status', 'data_emissao', 'ativo']
    list_filter = ['status', 'data_emissao', 'ativo', 'criado_em']
    search_fields = ['numero_documento', 'cliente__nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']
    ordering = ['-data_emissao', '-criado_em']
    filter_horizontal = ['tipos_receita']
    inlines = [ParcelaInline]
    
    fieldsets = (
        ('Informações do Documento', {
            'fields': ('numero_documento', 'data_emissao', 'descricao')
        }),
        ('Cliente', {
            'fields': ('cliente',)
        }),
        ('Valores e Parcelas', {
            'fields': ('valor_total', 'quantidade_parcelas')
        }),
        ('Classificação', {
            'fields': ('tipos_receita',)
        }),
        ('Controle', {
            'fields': ('status', 'ativo', 'observacoes')
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em', 'criado_por', 'atualizado_por'),
            'classes': ('collapse',)
        }),
    )

