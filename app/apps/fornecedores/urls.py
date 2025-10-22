# -*- coding: utf-8 -*-
"""
URLs do app Fornecedores
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FornecedorViewSet

router = DefaultRouter()
router.register(r'fornecedores', FornecedorViewSet, basename='fornecedor')

urlpatterns = router.urls



