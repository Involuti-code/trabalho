# -*- coding: utf-8 -*-
"""
URLs Web do app Contas a Receber
"""

from django.urls import path
from . import views_web

app_name = 'contas_receber'

urlpatterns = [
    path('', views_web.contas_receber_list, name='contas_receber_list'),
    path('api/', views_web.contas_receber_api, name='contas_receber_api'),
    path('api/<int:conta_id>/', views_web.contas_receber_api, name='contas_receber_api_detail'),
    path('api/<int:conta_id>/inativar/', views_web.conta_receber_inativar, name='conta_receber_inativar'),
    path('api/<int:conta_id>/reativar/', views_web.conta_receber_reativar, name='conta_receber_reativar'),
]

