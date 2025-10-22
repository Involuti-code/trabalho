# -*- coding: utf-8 -*-
"""
URLs do app Contas a Receber
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ContaReceberViewSet

router = DefaultRouter()
router.register(r'contas-receber', ContaReceberViewSet, basename='conta-receber')

urlpatterns = router.urls



