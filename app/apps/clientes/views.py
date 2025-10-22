# -*- coding: utf-8 -*-
"""
Views do app Clientes
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Cliente
from .serializers import (
    ClienteSerializer, ClienteListSerializer,
    ClienteCreateSerializer, ClienteUpdateSerializer
)


class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Clientes
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'criado_em', 'data_nascimento']
    search_fields = ['nome', 'cpf', 'email']
    ordering_fields = ['nome', 'cpf', 'criado_em']
    ordering = ['nome']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada ação"""
        if self.action == 'list':
            return ClienteListSerializer
        elif self.action == 'create':
            return ClienteCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ClienteUpdateSerializer
        return ClienteSerializer
    
    def get_queryset(self):
        """Filtra apenas clientes ativos por padrão"""
        queryset = super().get_queryset()
        
        # Filtro para incluir inativos (parâmetro include_inactive)
        include_inactive = self.request.query_params.get('include_inactive', 'false').lower() == 'true'
        if not include_inactive:
            queryset = queryset.filter(ativo=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Lista apenas clientes ativos"""
        queryset = self.get_queryset().filter(ativo=True)
        serializer = ClienteListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inativos(self, request):
        """Lista apenas clientes inativos"""
        queryset = self.get_queryset().filter(ativo=False)
        serializer = ClienteListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def inativar(self, request, pk=None):
        """Inativa um cliente"""
        cliente = self.get_object()
        cliente.inativar()
        serializer = self.get_serializer(cliente)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reativar(self, request, pk=None):
        """Reativa um cliente"""
        cliente = self.get_object()
        cliente.reativar()
        serializer = self.get_serializer(cliente)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """Busca clientes por termo"""
        termo = request.query_params.get('q', '')
        if not termo:
            return Response({'error': 'Parâmetro q é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(
            Q(nome__icontains=termo) |
            Q(cpf__icontains=termo) |
            Q(email__icontains=termo)
        )
        
        serializer = ClienteListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas dos clientes"""
        total = self.get_queryset().count()
        ativos = self.get_queryset().filter(ativo=True).count()
        inativos = self.get_queryset().filter(ativo=False).count()
        
        return Response({
            'total': total,
            'ativos': ativos,
            'inativos': inativos
        })



