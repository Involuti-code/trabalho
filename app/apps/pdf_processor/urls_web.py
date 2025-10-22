# -*- coding: utf-8 -*-
"""
URLs Web do app Processador de PDF
"""

from django.urls import path
from . import views_web

app_name = 'pdf_processor'

urlpatterns = [
    path('', views_web.pdf_processor_list, name='pdf_processor_list'),
    path('processados/', views_web.pdf_processed_list, name='pdf_processed_list'),
    path('processados/<int:processamento_id>/', views_web.pdf_processed_detail, name='pdf_processed_detail'),
    path('api/', views_web.pdf_processor_api, name='pdf_processor_api'),
    path('api/<int:processamento_id>/', views_web.pdf_processor_api, name='pdf_processor_api_detail'),
    path('api/<int:processamento_id>/reprocessar/', views_web.pdf_processor_reprocessar, name='pdf_processor_reprocessar'),
    path('api/<int:processamento_id>/criar-registros/', views_web.criar_registros_banco, name='criar_registros_banco'),
    path('api/upload/', views_web.pdf_processor_upload, name='pdf_processor_upload'),
]



