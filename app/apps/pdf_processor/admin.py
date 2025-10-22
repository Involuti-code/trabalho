# -*- coding: utf-8 -*-
"""
Admin do app Processador de PDF
"""

from django.contrib import admin
from .models import ProcessamentoPDF


@admin.register(ProcessamentoPDF)
class ProcessamentoPDFAdmin(admin.ModelAdmin):
    list_display = ['nome_arquivo', 'tamanho_arquivo', 'status_processamento', 'data_processamento', 'ativo']
    list_filter = ['status_processamento', 'data_processamento', 'ativo', 'criado_em']
    search_fields = ['nome_arquivo', 'erro_processamento']
    readonly_fields = ['criado_em', 'atualizado_em', 'tamanho_arquivo', 'data_processamento', 'tempo_processamento']
    ordering = ['-criado_em']
    
    fieldsets = (
        ('Arquivo', {
            'fields': ('arquivo_pdf', 'nome_arquivo', 'tamanho_arquivo')
        }),
        ('Processamento', {
            'fields': ('status_processamento', 'data_processamento', 'tempo_processamento')
        }),
        ('Resultado', {
            'fields': ('dados_extraidos', 'erro_processamento')
        }),
        ('Controle', {
            'fields': ('ativo',)
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em', 'criado_por', 'atualizado_por'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Desabilita adição manual - apenas via upload"""
        return False



