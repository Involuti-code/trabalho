# -*- coding: utf-8 -*-
"""
URLs Web do app Faturados
"""

from django.urls import path
from . import views_web

app_name = 'faturados'

urlpatterns = [
    path('', views_web.faturados_list, name='faturados_list'),
    path('api/', views_web.faturados_api, name='faturados_api'),
    path('api/<int:faturado_id>/', views_web.faturados_api, name='faturados_api_detail'),
    path('api/<int:faturado_id>/inativar/', views_web.faturado_inativar, name='faturado_inativar'),
    path('api/<int:faturado_id>/reativar/', views_web.faturado_reativar, name='faturado_reativar'),
]

