# -*- coding: utf-8 -*-
"""
Configuração do app Processador de PDF
"""

from django.apps import AppConfig


class PdfProcessorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pdf_processor'
    verbose_name = 'Processador de PDF'



