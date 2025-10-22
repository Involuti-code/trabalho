# -*- coding: utf-8 -*-
"""
Views do app Contas a Receber
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum
from django.utils import timezone

from .models import ContaReceber
from .serializers import (
    ContaReceberSerializer, ContaReceberListSerializer,
    ContaReceberCreateSerializer, ContaReceberUpdateSerializer
)


class ContaReceberViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Contas a Receber
    """
    queryset = ContaReceber.objects.all()
    serializer_class = ContaReceberSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'data_emissao', 'cliente', 'ativo']
    search_fields = ['numero_documento', 'descricao', 'cliente__nome']
    ordering_fields = ['numero_documento', 'data_emissao', 'valor_total', 'status']
    ordering = ['-data_emissao', '-criado_em']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada ação"""
        if self.action == 'list':
            return ContaReceberListSerializer
        elif self.action == 'create':
            return ContaReceberCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ContaReceberUpdateSerializer
        return ContaReceberSerializer
    
    def get_queryset(self):
        """Filtra apenas contas ativas por padrão"""
        queryset = super().get_queryset()
        
        # Filtro para incluir inativas (parâmetro include_inactive)
        include_inactive = self.request.query_params.get('include_inactive', 'false').lower() == 'true'
        if not include_inactive:
            queryset = queryset.filter(ativo=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def ativas(self, request):
        """Lista apenas contas ativas"""
        queryset = self.get_queryset().filter(ativo=True)
        serializer = ContaReceberListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inativas(self, request):
        """Lista apenas contas inativas"""
        queryset = self.get_queryset().filter(ativo=False)
        serializer = ContaReceberListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        """Lista contas pendentes"""
        queryset = self.get_queryset().filter(status='PENDENTE')
        serializer = ContaReceberListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recebidas(self, request):
        """Lista contas recebidas"""
        queryset = self.get_queryset().filter(status='PAGA')
        serializer = ContaReceberListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        """Lista contas vencidas"""
        queryset = self.get_queryset().filter(status='VENCIDA')
        serializer = ContaReceberListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_cliente(self, request):
        """Lista contas por cliente"""
        cliente_id = request.query_params.get('cliente_id')
        if cliente_id:
            queryset = self.get_queryset().filter(cliente_id=cliente_id)
        else:
            queryset = self.get_queryset()
        
        serializer = ContaReceberListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def marcar_como_recebida(self, request, pk=None):
        """Marca uma conta como recebida"""
        conta = self.get_object()
        conta.marcar_como_recebida()
        serializer = self.get_serializer(conta)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def inativar(self, request, pk=None):
        """Inativa uma conta"""
        conta = self.get_object()
        conta.inativar()
        serializer = self.get_serializer(conta)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reativar(self, request, pk=None):
        """Reativa uma conta"""
        conta = self.get_object()
        conta.reativar()
        serializer = self.get_serializer(conta)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas das contas a receber"""
        total = self.get_queryset().count()
        pendentes = self.get_queryset().filter(status='PENDENTE').count()
        recebidas = self.get_queryset().filter(status='PAGA').count()
        vencidas = self.get_queryset().filter(status='VENCIDA').count()
        canceladas = self.get_queryset().filter(status='CANCELADA').count()
        
        # Valores totais
        valor_total = self.get_queryset().aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        valor_recebido = sum(conta.get_valor_recebido() for conta in self.get_queryset())
        valor_pendente = valor_total - valor_recebido
        
        # Estatísticas por cliente
        clientes_stats = {}
        for conta in self.get_queryset():
            cliente_nome = conta.cliente.nome
            if cliente_nome not in clientes_stats:
                clientes_stats[cliente_nome] = {
                    'total_contas': 0,
                    'valor_total': 0,
                    'valor_recebido': 0
                }
            clientes_stats[cliente_nome]['total_contas'] += 1
            clientes_stats[cliente_nome]['valor_total'] += float(conta.valor_total)
            clientes_stats[cliente_nome]['valor_recebido'] += float(conta.get_valor_recebido())
        
        return Response({
            'total': total,
            'pendentes': pendentes,
            'recebidas': recebidas,
            'vencidas': vencidas,
            'canceladas': canceladas,
            'valor_total': valor_total,
            'valor_recebido': valor_recebido,
            'valor_pendente': valor_pendente,
            'clientes': clientes_stats
        })



