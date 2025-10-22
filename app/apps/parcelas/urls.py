# -*- coding: utf-8 -*-
"""
URLs do app Parcelas
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ParcelaViewSet

router = DefaultRouter()
router.register(r'parcelas', ParcelaViewSet, basename='parcela')

urlpatterns = router.urls



