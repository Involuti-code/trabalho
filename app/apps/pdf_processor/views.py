# -*- coding: utf-8 -*-
"""
Views do app Processador de PDF
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
import time

from .models import ProcessamentoPDF
from .serializers import (
    ProcessamentoPDFSerializer, ProcessamentoPDFListSerializer,
    ProcessamentoPDFCreateSerializer, ProcessarPDFSerializer,
    DadosExtraidosSerializer
)


class ProcessamentoPDFViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Processamento de PDF
    """
    queryset = ProcessamentoPDF.objects.all()
    serializer_class = ProcessamentoPDFSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status_processamento', 'data_processamento', 'ativo']
    search_fields = ['nome_arquivo', 'erro_processamento']
    ordering_fields = ['nome_arquivo', 'data_processamento', 'status_processamento']
    ordering = ['-criado_em']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada ação"""
        if self.action == 'list':
            return ProcessamentoPDFListSerializer
        elif self.action == 'create':
            return ProcessamentoPDFCreateSerializer
        return ProcessamentoPDFSerializer
    
    def get_queryset(self):
        """Filtra apenas processamentos ativos por padrão"""
        queryset = super().get_queryset()
        
        # Filtro para incluir inativos (parâmetro include_inactive)
        include_inactive = self.request.query_params.get('include_inactive', 'false').lower() == 'true'
        if not include_inactive:
            queryset = queryset.filter(ativo=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Lista apenas processamentos ativos"""
        queryset = self.get_queryset().filter(ativo=True)
        serializer = ProcessamentoPDFListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inativos(self, request):
        """Lista apenas processamentos inativos"""
        queryset = self.get_queryset().filter(ativo=False)
        serializer = ProcessamentoPDFListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        """Lista processamentos pendentes"""
        queryset = self.get_queryset().filter(status_processamento='PENDENTE')
        serializer = ProcessamentoPDFListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def processando(self, request):
        """Lista processamentos em andamento"""
        queryset = self.get_queryset().filter(status_processamento='PROCESSANDO')
        serializer = ProcessamentoPDFListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def sucesso(self, request):
        """Lista processamentos com sucesso"""
        queryset = self.get_queryset().filter(status_processamento='SUCESSO')
        serializer = ProcessamentoPDFListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def erro(self, request):
        """Lista processamentos com erro"""
        queryset = self.get_queryset().filter(status_processamento='ERRO')
        serializer = ProcessamentoPDFListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reprocessar(self, request, pk=None):
        """Reprocessa um PDF"""
        processamento = self.get_object()
        
        # Reset do status
        processamento.status_processamento = 'PENDENTE'
        processamento.erro_processamento = None
        processamento.dados_extraidos = None
        processamento.data_processamento = None
        processamento.tempo_processamento = None
        processamento.save()
        
        # Aqui seria chamado o processamento assíncrono
        # Por enquanto, apenas simula
        processamento.iniciar_processamento()
        
        serializer = self.get_serializer(processamento)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def dados_extraidos(self, request, pk=None):
        """Retorna os dados extraídos do PDF"""
        processamento = self.get_object()
        
        if not processamento.is_sucesso():
            return Response(
                {'error': 'PDF não foi processado com sucesso'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(processamento.dados_extraidos)
    
    @action(detail=True, methods=['get'])
    def fornecedor(self, request, pk=None):
        """Retorna dados do fornecedor extraídos"""
        processamento = self.get_object()
        dados_fornecedor = processamento.get_dados_fornecedor()
        
        if not dados_fornecedor:
            return Response(
                {'error': 'Dados do fornecedor não encontrados'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(dados_fornecedor)
    
    @action(detail=True, methods=['get'])
    def faturado(self, request, pk=None):
        """Retorna dados do faturado extraídos"""
        processamento = self.get_object()
        dados_faturado = processamento.get_dados_faturado()
        
        if not dados_faturado:
            return Response(
                {'error': 'Dados do faturado não encontrados'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(dados_faturado)
    
    @action(detail=True, methods=['get'])
    def nota_fiscal(self, request, pk=None):
        """Retorna dados da nota fiscal extraídos"""
        processamento = self.get_object()
        dados_nota = processamento.get_dados_nota_fiscal()
        
        if not dados_nota:
            return Response(
                {'error': 'Dados da nota fiscal não encontrados'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(dados_nota)
    
    @action(detail=True, methods=['get'])
    def parcelas(self, request, pk=None):
        """Retorna dados das parcelas extraídas"""
        processamento = self.get_object()
        dados_parcelas = processamento.get_dados_parcelas()
        
        if not dados_parcelas:
            return Response(
                {'error': 'Dados das parcelas não encontrados'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(dados_parcelas)
    
    @action(detail=True, methods=['get'])
    def classificacao(self, request, pk=None):
        """Retorna classificação da despesa extraída"""
        processamento = self.get_object()
        classificacao = processamento.get_classificacao_despesa()
        
        if not classificacao:
            return Response(
                {'error': 'Classificação não encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(classificacao)
    
    @action(detail=True, methods=['post'])
    def inativar(self, request, pk=None):
        """Inativa um processamento"""
        processamento = self.get_object()
        processamento.inativar()
        serializer = self.get_serializer(processamento)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reativar(self, request, pk=None):
        """Reativa um processamento"""
        processamento = self.get_object()
        processamento.reativar()
        serializer = self.get_serializer(processamento)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def processar(self, request):
        """Processa um PDF e retorna os dados extraídos"""
        serializer = ProcessarPDFSerializer(data=request.data)
        if serializer.is_valid():
            arquivo_pdf = serializer.validated_data['arquivo_pdf']
            
            # Criar registro de processamento
            processamento = ProcessamentoPDF.objects.create(
                arquivo_pdf=arquivo_pdf,
                nome_arquivo=arquivo_pdf.name,
                tamanho_arquivo=arquivo_pdf.size
            )
            
            # Simular processamento (aqui seria integrado com Gemini)
            processamento.iniciar_processamento()
            
            # Simular dados extraídos
            dados_extraidos = {
                'fornecedor': {
                    'razao_social': 'Fornecedor Exemplo Ltda',
                    'cnpj': '12.345.678/0001-90',
                    'email': 'contato@exemplo.com'
                },
                'faturado': {
                    'nome_completo': 'João Silva',
                    'cpf': '123.456.789-00'
                },
                'nota_fiscal': {
                    'numero': '12345',
                    'data_emissao': '2024-01-15',
                    'valor_total': 1500.00,
                    'descricao': 'Produtos agrícolas'
                },
                'parcelas': [
                    {
                        'numero': 1,
                        'data_vencimento': '2024-02-15',
                        'valor': 750.00
                    },
                    {
                        'numero': 2,
                        'data_vencimento': '2024-03-15',
                        'valor': 750.00
                    }
                ],
                'classificacao': {
                    'tipo_despesa': 'INSUMOS_AGRICOLAS',
                    'confianca': 0.85
                }
            }
            
            # Finalizar processamento
            tempo_processamento = timezone.timedelta(seconds=2.5)
            processamento.finalizar_processamento(
                dados_extraidos=dados_extraidos,
                tempo_processamento=tempo_processamento
            )
            
            response_serializer = self.get_serializer(processamento)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas dos processamentos"""
        total = self.get_queryset().count()
        pendentes = self.get_queryset().filter(status_processamento='PENDENTE').count()
        processando = self.get_queryset().filter(status_processamento='PROCESSANDO').count()
        sucesso = self.get_queryset().filter(status_processamento='SUCESSO').count()
        erro = self.get_queryset().filter(status_processamento='ERRO').count()
        
        # Tamanho total dos arquivos
        tamanho_total = sum(p.tamanho_arquivo for p in self.get_queryset() if p.tamanho_arquivo)
        tamanho_total_mb = round(tamanho_total / (1024 * 1024), 2)
        
        return Response({
            'total': total,
            'pendentes': pendentes,
            'processando': processando,
            'sucesso': sucesso,
            'erro': erro,
            'tamanho_total_mb': tamanho_total_mb
        })



