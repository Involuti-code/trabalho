# -*- coding: utf-8 -*-
"""
Views do app Tipos de Receita
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import TipoReceita
from .serializers import (
    TipoReceitaSerializer, TipoReceitaListSerializer,
    TipoReceitaCreateSerializer, TipoReceitaUpdateSerializer
)


class TipoReceitaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Tipos de Receita
    """
    queryset = TipoReceita.objects.all()
    serializer_class = TipoReceitaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'criado_em']
    search_fields = ['nome', 'codigo', 'descricao']
    ordering_fields = ['nome', 'codigo', 'criado_em']
    ordering = ['nome']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada ação"""
        if self.action == 'list':
            return TipoReceitaListSerializer
        elif self.action == 'create':
            return TipoReceitaCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TipoReceitaUpdateSerializer
        return TipoReceitaSerializer
    
    def get_queryset(self):
        """Filtra apenas tipos ativos por padrão"""
        queryset = super().get_queryset()
        
        # Filtro para incluir inativos (parâmetro include_inactive)
        include_inactive = self.request.query_params.get('include_inactive', 'false').lower() == 'true'
        if not include_inactive:
            queryset = queryset.filter(ativo=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Lista apenas tipos ativos"""
        queryset = self.get_queryset().filter(ativo=True)
        serializer = TipoReceitaListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inativos(self, request):
        """Lista apenas tipos inativos"""
        queryset = self.get_queryset().filter(ativo=False)
        serializer = TipoReceitaListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def inativar(self, request, pk=None):
        """Inativa um tipo de receita"""
        tipo = self.get_object()
        tipo.inativar()
        serializer = self.get_serializer(tipo)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reativar(self, request, pk=None):
        """Reativa um tipo de receita"""
        tipo = self.get_object()
        tipo.reativar()
        serializer = self.get_serializer(tipo)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas dos tipos de receita"""
        total = self.get_queryset().count()
        ativos = self.get_queryset().filter(ativo=True).count()
        inativos = self.get_queryset().filter(ativo=False).count()
        
        return Response({
            'total': total,
            'ativos': ativos,
            'inativos': inativos
        })



