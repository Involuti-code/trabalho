# -*- coding: utf-8 -*-
"""
Serializers do app Tipos de Receita
"""

from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from .models import TipoReceita


class TipoReceitaSerializer(BaseModelSerializer):
    """Serializer para Tipo de Receita"""
    
    class Meta:
        model = TipoReceita
        fields = BaseModelSerializer.Meta.fields + [
            'nome', 'codigo', 'descricao', 'cor'
        ]
    
    def validate_cor(self, value):
        """Validação da cor"""
        if value and not value.startswith('#'):
            raise serializers.ValidationError('Cor deve começar com #')
        
        if value and len(value) != 7:
            raise serializers.ValidationError('Cor deve ter 7 caracteres (#RRGGBB)')
        
        return value


class TipoReceitaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Tipos de Receita"""
    
    class Meta:
        model = TipoReceita
        fields = ['id', 'nome', 'codigo', 'cor', 'ativo']


class TipoReceitaCreateSerializer(TipoReceitaSerializer):
    """Serializer para criação de Tipo de Receita"""
    
    class Meta(TipoReceitaSerializer.Meta):
        fields = ['nome', 'codigo', 'descricao', 'cor']


class TipoReceitaUpdateSerializer(TipoReceitaSerializer):
    """Serializer para atualização de Tipo de Receita"""
    
    class Meta(TipoReceitaSerializer.Meta):
        fields = ['nome', 'codigo', 'descricao', 'cor', 'ativo']



