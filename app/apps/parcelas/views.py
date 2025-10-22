# -*- coding: utf-8 -*-
"""
Views do app Parcelas
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Parcela
from .serializers import (
    ParcelaSerializer, ParcelaListSerializer,
    ParcelaCreateSerializer, ParcelaUpdateSerializer,
    ParcelaPagamentoSerializer
)


class ParcelaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Parcelas
    """
    queryset = Parcela.objects.all()
    serializer_class = ParcelaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'data_vencimento', 'data_pagamento', 'ativo']
    search_fields = ['observacoes']
    ordering_fields = ['numero_parcela', 'data_vencimento', 'valor', 'status']
    ordering = ['data_vencimento', 'numero_parcela']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada ação"""
        if self.action == 'list':
            return ParcelaListSerializer
        elif self.action == 'create':
            return ParcelaCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ParcelaUpdateSerializer
        return ParcelaSerializer
    
    def get_queryset(self):
        """Filtra apenas parcelas ativas por padrão"""
        queryset = super().get_queryset()
        
        # Filtro para incluir inativas (parâmetro include_inactive)
        include_inactive = self.request.query_params.get('include_inactive', 'false').lower() == 'true'
        if not include_inactive:
            queryset = queryset.filter(ativo=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def ativas(self, request):
        """Lista apenas parcelas ativas"""
        queryset = self.get_queryset().filter(ativo=True)
        serializer = ParcelaListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inativas(self, request):
        """Lista apenas parcelas inativas"""
        queryset = self.get_queryset().filter(ativo=False)
        serializer = ParcelaListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        """Lista parcelas pendentes"""
        queryset = self.get_queryset().filter(status='PENDENTE')
        serializer = ParcelaListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pagas(self, request):
        """Lista parcelas pagas"""
        queryset = self.get_queryset().filter(status='PAGA')
        serializer = ParcelaListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        """Lista parcelas vencidas"""
        queryset = self.get_queryset().filter(status='VENCIDA')
        serializer = ParcelaListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def a_vencer(self, request):
        """Lista parcelas a vencer em X dias"""
        dias = int(request.query_params.get('dias', 30))
        data_limite = timezone.now().date() + timezone.timedelta(days=dias)
        
        queryset = self.get_queryset().filter(
            status='PENDENTE',
            data_vencimento__lte=data_limite,
            data_vencimento__gte=timezone.now().date()
        )
        serializer = ParcelaListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def marcar_como_paga(self, request, pk=None):
        """Marca uma parcela como paga"""
        parcela = self.get_object()
        serializer = ParcelaPagamentoSerializer(data=request.data)
        
        if serializer.is_valid():
            valor_pago = serializer.validated_data.get('valor_pago', parcela.valor)
            data_pagamento = serializer.validated_data.get('data_pagamento', timezone.now().date())
            
            parcela.marcar_como_paga(valor_pago, data_pagamento)
            response_serializer = self.get_serializer(parcela)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def marcar_como_vencida(self, request, pk=None):
        """Marca uma parcela como vencida"""
        parcela = self.get_object()
        parcela.marcar_como_vencida()
        serializer = self.get_serializer(parcela)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def inativar(self, request, pk=None):
        """Inativa uma parcela"""
        parcela = self.get_object()
        parcela.inativar()
        serializer = self.get_serializer(parcela)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reativar(self, request, pk=None):
        """Reativa uma parcela"""
        parcela = self.get_object()
        parcela.reativar()
        serializer = self.get_serializer(parcela)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas das parcelas"""
        total = self.get_queryset().count()
        pendentes = self.get_queryset().filter(status='PENDENTE').count()
        pagas = self.get_queryset().filter(status='PAGA').count()
        vencidas = self.get_queryset().filter(status='VENCIDA').count()
        canceladas = self.get_queryset().filter(status='CANCELADA').count()
        
        # Valor total pendente
        valor_pendente = sum(
            parcela.valor for parcela in self.get_queryset().filter(status='PENDENTE')
        )
        
        # Valor total pago
        valor_pago = sum(
            parcela.valor_pago for parcela in self.get_queryset().filter(status='PAGA')
        )
        
        return Response({
            'total': total,
            'pendentes': pendentes,
            'pagas': pagas,
            'vencidas': vencidas,
            'canceladas': canceladas,
            'valor_pendente': valor_pendente,
            'valor_pago': valor_pago
        })



