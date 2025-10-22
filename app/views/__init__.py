# -*- coding: utf-8 -*-
"""
Views do sistema administrativo-financeiro
"""

from .web_views import WebViews
from .fornecedor_views import FornecedorViews
from .cliente_views import ClienteViews
from .faturado_views import FaturadoViews
from .tipo_receita_views import TipoReceitaViews
from .tipo_despesa_views import TipoDespesaViews
from .conta_pagar_views import ContaPagarViews
from .conta_receber_views import ContaReceberViews
from .pdf_processor_views import PDFProcessorViews

__all__ = [
    'WebViews',
    'FornecedorViews',
    'ClienteViews',
    'FaturadoViews',
    'TipoReceitaViews', 
    'TipoDespesaViews',
    'ContaPagarViews',
    'ContaReceberViews',
    'PDFProcessorViews'
]

