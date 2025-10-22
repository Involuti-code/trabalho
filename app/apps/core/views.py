# -*- coding: utf-8 -*-
"""
Views do app Core
"""

from rest_framework import viewsets
from rest_framework.response import Response
from .models import CategoriaDespesa, StatusConta, StatusParcela
from .serializers import CategoriaDespesaSerializer, StatusContaSerializer, StatusParcelaSerializer


class CategoriaDespesaViewSet(viewsets.ViewSet):
    """
    ViewSet para Categorias de Despesa
    """
    
    def list(self, request):
        """Lista todas as categorias de despesa"""
        categorias = CategoriaDespesa.choices
        serializer = CategoriaDespesaSerializer(categorias, many=True)
        return Response(serializer.data)


class StatusContaViewSet(viewsets.ViewSet):
    """
    ViewSet para Status de Conta
    """
    
    def list(self, request):
        """Lista todos os status de conta"""
        status = StatusConta.choices
        serializer = StatusContaSerializer(status, many=True)
        return Response(serializer.data)


class StatusParcelaViewSet(viewsets.ViewSet):
    """
    ViewSet para Status de Parcela
    """
    
    def list(self, request):
        """Lista todos os status de parcela"""
        status = StatusParcela.choices
        serializer = StatusParcelaSerializer(status, many=True)
        return Response(serializer.data)



