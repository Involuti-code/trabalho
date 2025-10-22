# -*- coding: utf-8 -*-
"""
Admin do app Contas a Pagar
"""

from django.contrib import admin
from .models import ContaPagar


class ParcelaInline(admin.TabularInline):
    model = ContaPagar.parcelas.through
    extra = 0


@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ['numero_nota_fiscal', 'fornecedor', 'faturado', 'valor_total', 'status', 'data_emissao', 'ativo']
    list_filter = ['status', 'data_emissao', 'ativo', 'criado_em']
    search_fields = ['numero_nota_fiscal', 'fornecedor__razao_social', 'faturado__nome_completo', 'descricao_produtos']
    readonly_fields = ['criado_em', 'atualizado_em']
    ordering = ['-data_emissao', '-criado_em']
    filter_horizontal = ['tipos_despesa']
    inlines = [ParcelaInline]
    
    fieldsets = (
        ('Informações da Nota Fiscal', {
            'fields': ('numero_nota_fiscal', 'data_emissao', 'descricao_produtos')
        }),
        ('Fornecedor e Faturado', {
            'fields': ('fornecedor', 'faturado')
        }),
        ('Valores e Parcelas', {
            'fields': ('valor_total', 'quantidade_parcelas')
        }),
        ('Classificação', {
            'fields': ('tipos_despesa',)
        }),
        ('Controle', {
            'fields': ('status', 'ativo', 'observacoes')
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em', 'criado_por', 'atualizado_por'),
            'classes': ('collapse',)
        }),
    )

