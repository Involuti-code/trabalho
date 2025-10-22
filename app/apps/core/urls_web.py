# -*- coding: utf-8 -*-
"""
URLs Web do app Core
"""

from django.urls import path
from . import views_web

app_name = 'core'

urlpatterns = [
    path('', views_web.dashboard, name='dashboard'),
    path('dashboard/', views_web.dashboard, name='dashboard'),
    path('api/dashboard/stats/', views_web.dashboard_stats, name='dashboard_stats'),
    path('api/dashboard/fluxo-caixa/', views_web.fluxo_caixa_data, name='fluxo_caixa_data'),
    path('api/dashboard/despesas-categoria/', views_web.despesas_por_categoria_data, name='despesas_categoria_data'),
]



