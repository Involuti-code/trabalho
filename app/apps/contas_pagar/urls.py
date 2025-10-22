# -*- coding: utf-8 -*-
"""
URLs do app Contas a Pagar
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ContaPagarViewSet

router = DefaultRouter()
router.register(r'contas-pagar', ContaPagarViewSet, basename='conta-pagar')

urlpatterns = router.urls



