# -*- coding: utf-8 -*-
"""
Serializers do app Contas a Receber
"""

from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from apps.clientes.serializers import ClienteListSerializer
from apps.tipos_receita.serializers import TipoReceitaListSerializer
from apps.parcelas.serializers import ParcelaListSerializer
from .models import ContaReceber


class ContaReceberSerializer(BaseModelSerializer):
    """Serializer para Conta a Receber"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    valor_recebido = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    valor_pendente = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    is_recebida = serializers.BooleanField(read_only=True)
    is_vencida = serializers.BooleanField(read_only=True)
    
    # Relacionamentos
    cliente = ClienteListSerializer(read_only=True)
    tipos_receita = TipoReceitaListSerializer(many=True, read_only=True)
    parcelas = ParcelaListSerializer(many=True, read_only=True)
    
    class Meta:
        model = ContaReceber
        fields = BaseModelSerializer.Meta.fields + [
            'cliente', 'cliente_nome', 'numero_documento', 'data_emissao',
            'descricao', 'valor_total', 'quantidade_parcelas', 'status', 'status_display',
            'observacoes', 'tipos_receita', 'parcelas',
            'valor_recebido', 'valor_pendente', 'is_recebida', 'is_vencida'
        ]


class ContaReceberListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Contas a Receber"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    valor_recebido = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    valor_pendente = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    is_vencida = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = ContaReceber
        fields = [
            'id', 'numero_documento', 'cliente_nome', 'data_emissao',
            'valor_total', 'valor_recebido', 'valor_pendente',
            'status', 'status_display', 'is_vencida', 'ativo'
        ]


class ContaReceberCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de Conta a Receber"""
    
    class Meta:
        model = ContaReceber
        fields = [
            'cliente', 'numero_documento', 'data_emissao', 'descricao',
            'valor_total', 'quantidade_parcelas', 'observacoes', 'tipos_receita'
        ]
    
    def validate_data_emissao(self, value):
        """Validação da data de emissão"""
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError('Data de emissão não pode ser futura')
        return value


class ContaReceberUpdateSerializer(ContaReceberCreateSerializer):
    """Serializer para atualização de Conta a Receber"""
    
    class Meta(ContaReceberCreateSerializer.Meta):
        fields = ContaReceberCreateSerializer.Meta.fields + ['status', 'ativo']



