# -*- coding: utf-8 -*-
"""
URLs Web do app Fornecedores
"""

from django.urls import path
from . import views_web

app_name = 'fornecedores'

urlpatterns = [
    path('', views_web.fornecedores_list, name='fornecedores_list'),
    path('api/', views_web.fornecedores_api, name='fornecedores_api'),
    path('api/<int:fornecedor_id>/', views_web.fornecedores_api, name='fornecedores_api_detail'),
    path('api/<int:fornecedor_id>/inativar/', views_web.fornecedor_inativar, name='fornecedor_inativar'),
    path('api/<int:fornecedor_id>/reativar/', views_web.fornecedor_reativar, name='fornecedor_reativar'),
]



