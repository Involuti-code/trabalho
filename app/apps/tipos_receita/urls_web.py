# -*- coding: utf-8 -*-
"""
URLs Web do app Tipos de Receita
"""

from django.urls import path
from . import views_web

app_name = 'tipos_receita'

urlpatterns = [
    path('', views_web.tipos_receita_list, name='tipos_receita_list'),
    path('api/', views_web.tipos_receita_api, name='tipos_receita_api'),
    path('api/<int:tipo_id>/', views_web.tipos_receita_api, name='tipos_receita_api_detail'),
    path('api/<int:tipo_id>/inativar/', views_web.tipo_receita_inativar, name='tipo_receita_inativar'),
    path('api/<int:tipo_id>/reativar/', views_web.tipo_receita_reativar, name='tipo_receita_reativar'),
]

