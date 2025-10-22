# -*- coding: utf-8 -*-
"""
Serializers do app Clientes
"""

from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from .models import Cliente


class ClienteSerializer(BaseModelSerializer):
    """Serializer para Cliente"""
    
    class Meta:
        model = Cliente
        fields = BaseModelSerializer.Meta.fields + [
            'nome', 'cpf', 'email', 'telefone', 'endereco',
            'data_nascimento', 'observacoes'
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


class ClienteListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Clientes"""
    
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'cpf', 'email', 'telefone', 'ativo']


class ClienteCreateSerializer(ClienteSerializer):
    """Serializer para criação de Cliente"""
    
    class Meta(ClienteSerializer.Meta):
        fields = [
            'nome', 'cpf', 'email', 'telefone', 'endereco',
            'data_nascimento', 'observacoes'
        ]


class ClienteUpdateSerializer(ClienteSerializer):
    """Serializer para atualização de Cliente"""
    
    class Meta(ClienteSerializer.Meta):
        fields = [
            'nome', 'cpf', 'email', 'telefone', 'endereco',
            'data_nascimento', 'observacoes', 'ativo'
        ]



