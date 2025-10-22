# -*- coding: utf-8 -*-
"""
Views do app Contas a Pagar
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum
from django.utils import timezone

from .models import ContaPagar
from .serializers import (
    ContaPagarSerializer, ContaPagarListSerializer,
    ContaPagarCreateSerializer, ContaPagarUpdateSerializer,
    ContaPagarClassificarSerializer
)


class ContaPagarViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Contas a Pagar
    """
    queryset = ContaPagar.objects.all()
    serializer_class = ContaPagarSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'data_emissao', 'fornecedor', 'faturado', 'ativo']
    search_fields = ['numero_nota_fiscal', 'descricao_produtos', 'fornecedor__razao_social', 'faturado__nome_completo']
    ordering_fields = ['numero_nota_fiscal', 'data_emissao', 'valor_total', 'status']
    ordering = ['-data_emissao', '-criado_em']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada ação"""
        if self.action == 'list':
            return ContaPagarListSerializer
        elif self.action == 'create':
            return ContaPagarCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ContaPagarUpdateSerializer
        return ContaPagarSerializer
    
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
        serializer = ContaPagarListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inativas(self, request):
        """Lista apenas contas inativas"""
        queryset = self.get_queryset().filter(ativo=False)
        serializer = ContaPagarListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        """Lista contas pendentes"""
        queryset = self.get_queryset().filter(status='PENDENTE')
        serializer = ContaPagarListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pagas(self, request):
        """Lista contas pagas"""
        queryset = self.get_queryset().filter(status='PAGA')
        serializer = ContaPagarListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        """Lista contas vencidas"""
        queryset = self.get_queryset().filter(status='VENCIDA')
        serializer = ContaPagarListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_fornecedor(self, request):
        """Lista contas por fornecedor"""
        fornecedor_id = request.query_params.get('fornecedor_id')
        if fornecedor_id:
            queryset = self.get_queryset().filter(fornecedor_id=fornecedor_id)
        else:
            queryset = self.get_queryset()
        
        serializer = ContaPagarListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_faturado(self, request):
        """Lista contas por faturado"""
        faturado_id = request.query_params.get('faturado_id')
        if faturado_id:
            queryset = self.get_queryset().filter(faturado_id=faturado_id)
        else:
            queryset = self.get_queryset()
        
        serializer = ContaPagarListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def marcar_como_paga(self, request, pk=None):
        """Marca uma conta como paga"""
        conta = self.get_object()
        conta.marcar_como_paga()
        serializer = self.get_serializer(conta)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def classificar_automaticamente(self, request, pk=None):
        """Classifica automaticamente uma conta"""
        conta = self.get_object()
        conta.classificar_automaticamente()
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
    
    @action(detail=False, methods=['post'])
    def classificar_lote(self, request):
        """Classifica automaticamente múltiplas contas"""
        serializer = ContaPagarClassificarSerializer(data=request.data, many=True)
        if serializer.is_valid():
            contas_ids = [item['conta_id'] for item in serializer.validated_data]
            contas = ContaPagar.objects.filter(id__in=contas_ids)
            
            for conta in contas:
                conta.classificar_automaticamente()
            
            return Response({'message': f'{len(contas)} contas classificadas com sucesso'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas das contas a pagar"""
        total = self.get_queryset().count()
        pendentes = self.get_queryset().filter(status='PENDENTE').count()
        pagas = self.get_queryset().filter(status='PAGA').count()
        vencidas = self.get_queryset().filter(status='VENCIDA').count()
        canceladas = self.get_queryset().filter(status='CANCELADA').count()
        
        # Valores totais
        valor_total = self.get_queryset().aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        valor_pago = sum(conta.get_valor_pago() for conta in self.get_queryset())
        valor_pendente = valor_total - valor_pago
        
        # Estatísticas por fornecedor
        fornecedores_stats = {}
        for conta in self.get_queryset():
            fornecedor_nome = conta.fornecedor.razao_social
            if fornecedor_nome not in fornecedores_stats:
                fornecedores_stats[fornecedor_nome] = {
                    'total_contas': 0,
                    'valor_total': 0,
                    'valor_pago': 0
                }
            fornecedores_stats[fornecedor_nome]['total_contas'] += 1
            fornecedores_stats[fornecedor_nome]['valor_total'] += float(conta.valor_total)
            fornecedores_stats[fornecedor_nome]['valor_pago'] += float(conta.get_valor_pago())
        
        return Response({
            'total': total,
            'pendentes': pendentes,
            'pagas': pagas,
            'vencidas': vencidas,
            'canceladas': canceladas,
            'valor_total': valor_total,
            'valor_pago': valor_pago,
            'valor_pendente': valor_pendente,
            'fornecedores': fornecedores_stats
        })



