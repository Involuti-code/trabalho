# -*- coding: utf-8 -*-
"""
App config for PDF Extractor
"""

from django.apps import AppConfig


class PdfExtractorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pdf_extractor'
    verbose_name = 'PDF Extractor'


