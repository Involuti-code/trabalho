# -*- coding: utf-8 -*-
"""
Views do app Faturados
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Faturado
from .serializers import (
    FaturadoSerializer, FaturadoListSerializer,
    FaturadoCreateSerializer, FaturadoUpdateSerializer
)


class FaturadoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Faturados
    """
    queryset = Faturado.objects.all()
    serializer_class = FaturadoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'criado_em']
    search_fields = ['nome_completo', 'cpf', 'email']
    ordering_fields = ['nome_completo', 'cpf', 'criado_em']
    ordering = ['nome_completo']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada ação"""
        if self.action == 'list':
            return FaturadoListSerializer
        elif self.action == 'create':
            return FaturadoCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return FaturadoUpdateSerializer
        return FaturadoSerializer
    
    def get_queryset(self):
        """Filtra apenas faturados ativos por padrão"""
        queryset = super().get_queryset()
        
        # Filtro para incluir inativos (parâmetro include_inactive)
        include_inactive = self.request.query_params.get('include_inactive', 'false').lower() == 'true'
        if not include_inactive:
            queryset = queryset.filter(ativo=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Lista apenas faturados ativos"""
        queryset = self.get_queryset().filter(ativo=True)
        serializer = FaturadoListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inativos(self, request):
        """Lista apenas faturados inativos"""
        queryset = self.get_queryset().filter(ativo=False)
        serializer = FaturadoListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def inativar(self, request, pk=None):
        """Inativa um faturado"""
        faturado = self.get_object()
        faturado.inativar()
        serializer = self.get_serializer(faturado)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reativar(self, request, pk=None):
        """Reativa um faturado"""
        faturado = self.get_object()
        faturado.reativar()
        serializer = self.get_serializer(faturado)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """Busca faturados por termo"""
        termo = request.query_params.get('q', '')
        if not termo:
            return Response({'error': 'Parâmetro q é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(
            Q(nome_completo__icontains=termo) |
            Q(cpf__icontains=termo) |
            Q(email__icontains=termo)
        )
        
        serializer = FaturadoListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas dos faturados"""
        total = self.get_queryset().count()
        ativos = self.get_queryset().filter(ativo=True).count()
        inativos = self.get_queryset().filter(ativo=False).count()
        
        return Response({
            'total': total,
            'ativos': ativos,
            'inativos': inativos
        })



