# -*- coding: utf-8 -*-
"""
URLs do app Processador de PDF
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProcessamentoPDFViewSet

router = DefaultRouter()
router.register(r'processamentos-pdf', ProcessamentoPDFViewSet, basename='processamento-pdf')

urlpatterns = router.urls



