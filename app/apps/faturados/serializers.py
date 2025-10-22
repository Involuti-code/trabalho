# -*- coding: utf-8 -*-
"""
Serializers do app Faturados
"""

from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from .models import Faturado


class FaturadoSerializer(BaseModelSerializer):
    """Serializer para Faturado"""
    
    class Meta:
        model = Faturado
        fields = BaseModelSerializer.Meta.fields + [
            'nome_completo', 'cpf', 'email', 'telefone', 'endereco', 'observacoes'
        ]
    
    def validate_cpf(self, value):
        """Validação customizada do CPF"""
        if value:
            # Remove formatação
            cpf_limpo = value.replace('.', '').replace('-', '')
            
            # Verifica se tem 11 dígitos
            if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
                raise serializers.ValidationError('CPF deve conter 11 dígitos')
            
            # Verifica se não é uma sequência de números iguais
            if cpf_limpo == cpf_limpo[0] * 11:
                raise serializers.ValidationError('CPF inválido')
        
        return value


class FaturadoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Faturados"""
    
    class Meta:
        model = Faturado
        fields = ['id', 'nome_completo', 'cpf', 'email', 'telefone', 'ativo']


class FaturadoCreateSerializer(FaturadoSerializer):
    """Serializer para criação de Faturado"""
    
    class Meta(FaturadoSerializer.Meta):
        fields = [
            'nome_completo', 'cpf', 'email', 'telefone', 'endereco', 'observacoes'
        ]


class FaturadoUpdateSerializer(FaturadoSerializer):
    """Serializer para atualização de Faturado"""
    
    class Meta(FaturadoSerializer.Meta):
        fields = [
            'nome_completo', 'cpf', 'email', 'telefone', 'endereco', 'observacoes', 'ativo'
        ]



