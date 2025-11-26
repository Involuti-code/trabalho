# -*- coding: utf-8 -*-
"""
URLs Web do app Contas a Pagar
"""

from django.urls import path
from . import views_web

app_name = 'contas_pagar'

urlpatterns = [
    path('', views_web.contas_pagar_list, name='contas_pagar_list'),
    path('api/', views_web.contas_pagar_api, name='contas_pagar_api'),
    path('api/<int:conta_id>/', views_web.contas_pagar_api, name='contas_pagar_api_detail'),
    path('api/<int:conta_id>/inativar/', views_web.conta_pagar_inativar, name='conta_pagar_inativar'),
    path('api/<int:conta_id>/reativar/', views_web.conta_pagar_reativar, name='conta_pagar_reativar'),
]

