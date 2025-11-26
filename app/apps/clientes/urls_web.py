# -*- coding: utf-8 -*-
"""
URLs Web do app Clientes
"""

from django.urls import path
from . import views_web

app_name = 'clientes'

urlpatterns = [
    path('', views_web.clientes_list, name='clientes_list'),
    path('api/', views_web.clientes_api, name='clientes_api'),
    path('api/<int:cliente_id>/', views_web.clientes_api, name='clientes_api_detail'),
    path('api/<int:cliente_id>/inativar/', views_web.cliente_inativar, name='cliente_inativar'),
    path('api/<int:cliente_id>/reativar/', views_web.cliente_reativar, name='cliente_reativar'),
]

