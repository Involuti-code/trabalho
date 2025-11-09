# -*- coding: utf-8 -*-
"""
Configuração do app RAG
"""

from django.apps import AppConfig


class RagConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.rag'
    verbose_name = 'RAG - Busca Inteligente'

