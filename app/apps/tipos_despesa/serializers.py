# -*- coding: utf-8 -*-
"""
Serializers do app Tipos de Despesa
"""

from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from .models import TipoDespesa


class TipoDespesaSerializer(BaseModelSerializer):
    """Serializer para Tipo de Despesa"""
    
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    palavras_chave_list = serializers.ListField(
        child=serializers.CharField(),
        source='get_palavras_chave_list',
        read_only=True
    )
    
    class Meta:
        model = TipoDespesa
        fields = BaseModelSerializer.Meta.fields + [
            'nome', 'codigo', 'descricao', 'categoria', 'categoria_display',
            'cor', 'palavras_chave', 'palavras_chave_list'
        ]
    
    def validate_cor(self, value):
        """Validação da cor"""
        if value and not value.startswith('#'):
            raise serializers.ValidationError('Cor deve começar com #')
        
        if value and len(value) != 7:
            raise serializers.ValidationError('Cor deve ter 7 caracteres (#RRGGBB)')
        
        return value


class TipoDespesaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Tipos de Despesa"""
    
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    
    class Meta:
        model = TipoDespesa
        fields = ['id', 'nome', 'codigo', 'categoria', 'categoria_display', 'cor', 'ativo']


class TipoDespesaCreateSerializer(TipoDespesaSerializer):
    """Serializer para criação de Tipo de Despesa"""
    
    class Meta(TipoDespesaSerializer.Meta):
        fields = ['nome', 'codigo', 'descricao', 'categoria', 'cor', 'palavras_chave']


class TipoDespesaUpdateSerializer(TipoDespesaSerializer):
    """Serializer para atualização de Tipo de Despesa"""
    
    class Meta(TipoDespesaSerializer.Meta):
        fields = ['nome', 'codigo', 'descricao', 'categoria', 'cor', 'palavras_chave', 'ativo']


class ClassificarDespesaSerializer(serializers.Serializer):
    """Serializer para classificação automática de despesas"""
    
    descricao = serializers.CharField(max_length=1000)
    
    def validate_descricao(self, value):
        """Validação da descrição"""
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError('Descrição deve ter pelo menos 3 caracteres')
        return value.strip()



