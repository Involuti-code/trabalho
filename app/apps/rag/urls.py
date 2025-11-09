# -*- coding: utf-8 -*-
"""
URLs do app RAG
"""

from django.urls import path
from . import views

app_name = 'rag'

urlpatterns = [
    path('', views.RAGView.as_view(), name='index'),
    path('consultar/', views.ConsultarRAGView.as_view(), name='consultar'),
    path('historico/', views.HistoricoRAGView.as_view(), name='historico'),
]

