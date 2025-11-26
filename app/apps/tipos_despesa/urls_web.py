# -*- coding: utf-8 -*-
"""
URLs Web do app Tipos de Despesa
"""

from django.urls import path
from . import views_web

app_name = 'tipos_despesa'

urlpatterns = [
    path('', views_web.tipos_despesa_list, name='tipos_despesa_list'),
    path('api/', views_web.tipos_despesa_api, name='tipos_despesa_api'),
    path('api/<int:tipo_id>/', views_web.tipos_despesa_api, name='tipos_despesa_api_detail'),
    path('api/<int:tipo_id>/inativar/', views_web.tipo_despesa_inativar, name='tipo_despesa_inativar'),
    path('api/<int:tipo_id>/reativar/', views_web.tipo_despesa_reativar, name='tipo_despesa_reativar'),
]

