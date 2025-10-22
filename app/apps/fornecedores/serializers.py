# -*- coding: utf-8 -*-
"""
Serializers do app Fornecedores
"""

from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from .models import Fornecedor


class FornecedorSerializer(BaseModelSerializer):
    """Serializer para Fornecedor"""
    
    nome_display = serializers.CharField(source='get_nome_display', read_only=True)
    
    class Meta:
        model = Fornecedor
        fields = BaseModelSerializer.Meta.fields + [
            'razao_social', 'fantasia', 'cnpj', 'email', 'telefone',
            'endereco', 'observacoes', 'nome_display'
        ]
    
    def validate_cnpj(self, value):
        """Validação customizada do CNPJ"""
        if value:
            # Remove formatação
            cnpj_limpo = value.replace('.', '').replace('/', '').replace('-', '')
            
            # Verifica se tem 14 dígitos
            if len(cnpj_limpo) != 14 or not cnpj_limpo.isdigit():
                raise serializers.ValidationError('CNPJ deve conter 14 dígitos')
            
            # Verifica se não é uma sequência de números iguais
            if cnpj_limpo == cnpj_limpo[0] * 14:
                raise serializers.ValidationError('CNPJ inválido')
        
        return value


class FornecedorListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Fornecedores"""
    
    nome_display = serializers.CharField(source='get_nome_display', read_only=True)
    
    class Meta:
        model = Fornecedor
        fields = ['id', 'razao_social', 'fantasia', 'cnpj', 'nome_display', 'ativo']


class FornecedorCreateSerializer(FornecedorSerializer):
    """Serializer para criação de Fornecedor"""
    
    class Meta(FornecedorSerializer.Meta):
        fields = [
            'razao_social', 'fantasia', 'cnpj', 'email', 'telefone',
            'endereco', 'observacoes'
        ]


class FornecedorUpdateSerializer(FornecedorSerializer):
    """Serializer para atualização de Fornecedor"""
    
    class Meta(FornecedorSerializer.Meta):
        fields = [
            'razao_social', 'fantasia', 'cnpj', 'email', 'telefone',
            'endereco', 'observacoes', 'ativo'
        ]



