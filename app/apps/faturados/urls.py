# -*- coding: utf-8 -*-
"""
URLs do app Faturados
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FaturadoViewSet

router = DefaultRouter()
router.register(r'faturados', FaturadoViewSet, basename='faturado')

urlpatterns = router.urls



