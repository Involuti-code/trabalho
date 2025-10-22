# -*- coding: utf-8 -*-
"""
Views do app Tipos de Despesa
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import TipoDespesa
from .serializers import (
    TipoDespesaSerializer, TipoDespesaListSerializer,
    TipoDespesaCreateSerializer, TipoDespesaUpdateSerializer,
    ClassificarDespesaSerializer
)


class TipoDespesaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Tipos de Despesa
    """
    queryset = TipoDespesa.objects.all()
    serializer_class = TipoDespesaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'ativo', 'criado_em']
    search_fields = ['nome', 'codigo', 'descricao', 'palavras_chave']
    ordering_fields = ['nome', 'codigo', 'categoria', 'criado_em']
    ordering = ['categoria', 'nome']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada ação"""
        if self.action == 'list':
            return TipoDespesaListSerializer
        elif self.action == 'create':
            return TipoDespesaCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TipoDespesaUpdateSerializer
        return TipoDespesaSerializer
    
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
        serializer = TipoDespesaListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inativos(self, request):
        """Lista apenas tipos inativos"""
        queryset = self.get_queryset().filter(ativo=False)
        serializer = TipoDespesaListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """Lista tipos agrupados por categoria"""
        categoria = request.query_params.get('categoria')
        if categoria:
            queryset = self.get_queryset().filter(categoria=categoria)
        else:
            queryset = self.get_queryset()
        
        serializer = TipoDespesaListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def inativar(self, request, pk=None):
        """Inativa um tipo de despesa"""
        tipo = self.get_object()
        tipo.inativar()
        serializer = self.get_serializer(tipo)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reativar(self, request, pk=None):
        """Reativa um tipo de despesa"""
        tipo = self.get_object()
        tipo.reativar()
        serializer = self.get_serializer(tipo)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def classificar(self, request):
        """Classifica automaticamente uma despesa baseada na descrição"""
        serializer = ClassificarDespesaSerializer(data=request.data)
        if serializer.is_valid():
            descricao = serializer.validated_data['descricao']
            tipo_despesa = TipoDespesa.classificar_por_descricao(descricao)
            
            if tipo_despesa:
                tipo_serializer = TipoDespesaListSerializer(tipo_despesa)
                return Response({
                    'classificacao': tipo_serializer.data,
                    'confianca': 'alta' if len(tipo_despesa.get_palavras_chave_list()) > 0 else 'baixa'
                })
            else:
                return Response({
                    'classificacao': None,
                    'confianca': 'nenhuma',
                    'mensagem': 'Nenhuma classificação encontrada para esta descrição'
                })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas dos tipos de despesa"""
        total = self.get_queryset().count()
        ativos = self.get_queryset().filter(ativo=True).count()
        inativos = self.get_queryset().filter(ativo=False).count()
        
        # Estatísticas por categoria
        categorias = {}
        for categoria, _ in TipoDespesa.CategoriaDespesa.choices:
            count = self.get_queryset().filter(categoria=categoria).count()
            categorias[categoria] = count
        
        return Response({
            'total': total,
            'ativos': ativos,
            'inativos': inativos,
            'por_categoria': categorias
        })



