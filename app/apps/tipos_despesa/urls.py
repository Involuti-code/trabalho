# -*- coding: utf-8 -*-
"""
URLs do app Tipos de Despesa
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TipoDespesaViewSet

router = DefaultRouter()
router.register(r'tipos-despesa', TipoDespesaViewSet, basename='tipo-despesa')

urlpatterns = router.urls



