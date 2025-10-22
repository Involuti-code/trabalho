# -*- coding: utf-8 -*-
"""
URLs do app Tipos de Receita
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TipoReceitaViewSet

router = DefaultRouter()
router.register(r'tipos-receita', TipoReceitaViewSet, basename='tipo-receita')

urlpatterns = router.urls



