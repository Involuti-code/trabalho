# -*- coding: utf-8 -*-
"""
URLs do app Core
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaDespesaViewSet, StatusContaViewSet, StatusParcelaViewSet
)

router = DefaultRouter()
router.register(r'categorias-despesa', CategoriaDespesaViewSet, basename='categoria-despesa')
router.register(r'status-conta', StatusContaViewSet, basename='status-conta')
router.register(r'status-parcela', StatusParcelaViewSet, basename='status-parcela')

urlpatterns = router.urls



