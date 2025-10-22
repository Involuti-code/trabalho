# -*- coding: utf-8 -*-
"""
Serializers do app Processador de PDF
"""

from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from .models import ProcessamentoPDF


class ProcessamentoPDFSerializer(BaseModelSerializer):
    """Serializer para Processamento de PDF"""
    
    status_display = serializers.CharField(source='get_status_processamento_display', read_only=True)
    tamanho_arquivo_mb = serializers.SerializerMethodField()
    tempo_processamento_segundos = serializers.SerializerMethodField()
    
    class Meta:
        model = ProcessamentoPDF
        fields = BaseModelSerializer.Meta.fields + [
            'arquivo_pdf', 'nome_arquivo', 'tamanho_arquivo', 'tamanho_arquivo_mb',
            'status_processamento', 'status_display', 'dados_extraidos',
            'erro_processamento', 'data_processamento', 'tempo_processamento',
            'tempo_processamento_segundos'
        ]
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + [
            'tamanho_arquivo', 'status_processamento', 'dados_extraidos',
            'erro_processamento', 'data_processamento', 'tempo_processamento'
        ]
    
    def get_tamanho_arquivo_mb(self, obj):
        """Retorna o tamanho do arquivo em MB"""
        if obj.tamanho_arquivo:
            return round(obj.tamanho_arquivo / (1024 * 1024), 2)
        return 0
    
    def get_tempo_processamento_segundos(self, obj):
        """Retorna o tempo de processamento em segundos"""
        if obj.tempo_processamento:
            return obj.tempo_processamento.total_seconds()
        return None


class ProcessamentoPDFListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Processamentos de PDF"""
    
    status_display = serializers.CharField(source='get_status_processamento_display', read_only=True)
    tamanho_arquivo_mb = serializers.SerializerMethodField()
    
    class Meta:
        model = ProcessamentoPDF
        fields = [
            'id', 'nome_arquivo', 'tamanho_arquivo_mb', 'status_processamento',
            'status_display', 'data_processamento', 'ativo'
        ]
    
    def get_tamanho_arquivo_mb(self, obj):
        """Retorna o tamanho do arquivo em MB"""
        if obj.tamanho_arquivo:
            return round(obj.tamanho_arquivo / (1024 * 1024), 2)
        return 0


class ProcessamentoPDFCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de Processamento de PDF"""
    
    class Meta:
        model = ProcessamentoPDF
        fields = ['arquivo_pdf']
    
    def validate_arquivo_pdf(self, value):
        """Validação do arquivo PDF"""
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError('Apenas arquivos PDF são permitidos')
        
        # Verificar tamanho do arquivo (16MB)
        if value.size > 16 * 1024 * 1024:
            raise serializers.ValidationError('Arquivo muito grande. Máximo 16MB')
        
        return value


class DadosExtraidosSerializer(serializers.Serializer):
    """Serializer para dados extraídos do PDF"""
    
    fornecedor = serializers.DictField(required=False)
    faturado = serializers.DictField(required=False)
    nota_fiscal = serializers.DictField(required=False)
    parcelas = serializers.DictField(required=False)
    classificacao = serializers.DictField(required=False)


class ProcessarPDFSerializer(serializers.Serializer):
    """Serializer para processamento de PDF"""
    
    arquivo_pdf = serializers.FileField()
    
    def validate_arquivo_pdf(self, value):
        """Validação do arquivo PDF"""
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError('Apenas arquivos PDF são permitidos')
        
        # Verificar tamanho do arquivo (16MB)
        if value.size > 16 * 1024 * 1024:
            raise serializers.ValidationError('Arquivo muito grande. Máximo 16MB')
        
        return value



