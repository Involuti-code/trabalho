# -*- coding: utf-8 -*-
"""
URLs do app Clientes
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')

urlpatterns = router.urls



