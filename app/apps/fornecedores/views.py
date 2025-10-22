# -*- coding: utf-8 -*-
"""
Views do app Fornecedores
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Fornecedor
from .serializers import (
    FornecedorSerializer, FornecedorListSerializer,
    FornecedorCreateSerializer, FornecedorUpdateSerializer
)


class FornecedorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Fornecedores
    """
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'criado_em']
    search_fields = ['razao_social', 'fantasia', 'cnpj', 'email']
    ordering_fields = ['razao_social', 'fantasia', 'cnpj', 'criado_em']
    ordering = ['razao_social']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada ação"""
        if self.action == 'list':
            return FornecedorListSerializer
        elif self.action == 'create':
            return FornecedorCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return FornecedorUpdateSerializer
        return FornecedorSerializer
    
    def get_queryset(self):
        """Filtra apenas fornecedores ativos por padrão"""
        queryset = super().get_queryset()
        
        # Filtro para incluir inativos (parâmetro include_inactive)
        include_inactive = self.request.query_params.get('include_inactive', 'false').lower() == 'true'
        if not include_inactive:
            queryset = queryset.filter(ativo=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Lista apenas fornecedores ativos"""
        queryset = self.get_queryset().filter(ativo=True)
        serializer = FornecedorListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inativos(self, request):
        """Lista apenas fornecedores inativos"""
        queryset = self.get_queryset().filter(ativo=False)
        serializer = FornecedorListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def inativar(self, request, pk=None):
        """Inativa um fornecedor"""
        fornecedor = self.get_object()
        fornecedor.inativar()
        serializer = self.get_serializer(fornecedor)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reativar(self, request, pk=None):
        """Reativa um fornecedor"""
        fornecedor = self.get_object()
        fornecedor.reativar()
        serializer = self.get_serializer(fornecedor)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """Busca fornecedores por termo"""
        termo = request.query_params.get('q', '')
        if not termo:
            return Response({'error': 'Parâmetro q é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(
            Q(razao_social__icontains=termo) |
            Q(fantasia__icontains=termo) |
            Q(cnpj__icontains=termo) |
            Q(email__icontains=termo)
        )
        
        serializer = FornecedorListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas dos fornecedores"""
        total = self.get_queryset().count()
        ativos = self.get_queryset().filter(ativo=True).count()
        inativos = self.get_queryset().filter(ativo=False).count()
        
        return Response({
            'total': total,
            'ativos': ativos,
            'inativos': inativos
        })



