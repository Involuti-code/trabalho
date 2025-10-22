# -*- coding: utf-8 -*-
"""
Serializers do app Parcelas
"""

from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from .models import Parcela


class ParcelaSerializer(BaseModelSerializer):
    """Serializer para Parcela"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_vencida = serializers.BooleanField(read_only=True)
    is_paga = serializers.BooleanField(read_only=True)
    is_pendente = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Parcela
        fields = BaseModelSerializer.Meta.fields + [
            'numero_parcela', 'data_vencimento', 'valor', 'status', 'status_display',
            'data_pagamento', 'valor_pago', 'observacoes',
            'is_vencida', 'is_paga', 'is_pendente'
        ]
    
    def validate(self, data):
        """Validações gerais"""
        # Validar se valor pago não excede o valor da parcela
        if 'valor_pago' in data and 'valor' in data:
            if data['valor_pago'] > data['valor']:
                raise serializers.ValidationError({
                    'valor_pago': 'Valor pago não pode ser maior que o valor da parcela'
                })
        
        # Validar se data de pagamento é posterior ao vencimento quando paga
        if 'status' in data and data['status'] == 'PAGA':
            if 'data_pagamento' in data and 'data_vencimento' in data:
                if data['data_pagamento'] < data['data_vencimento']:
                    raise serializers.ValidationError({
                        'data_pagamento': 'Data de pagamento não pode ser anterior ao vencimento'
                    })
        
        return data


class ParcelaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Parcelas"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_vencida = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Parcela
        fields = [
            'id', 'numero_parcela', 'data_vencimento', 'valor', 'status',
            'status_display', 'data_pagamento', 'valor_pago', 'is_vencida', 'ativo'
        ]


class ParcelaCreateSerializer(ParcelaSerializer):
    """Serializer para criação de Parcela"""
    
    class Meta(ParcelaSerializer.Meta):
        fields = [
            'numero_parcela', 'data_vencimento', 'valor', 'status',
            'data_pagamento', 'valor_pago', 'observacoes'
        ]


class ParcelaUpdateSerializer(ParcelaSerializer):
    """Serializer para atualização de Parcela"""
    
    class Meta(ParcelaSerializer.Meta):
        fields = [
            'numero_parcela', 'data_vencimento', 'valor', 'status',
            'data_pagamento', 'valor_pago', 'observacoes', 'ativo'
        ]


class ParcelaPagamentoSerializer(serializers.Serializer):
    """Serializer para marcar parcela como paga"""
    
    valor_pago = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    data_pagamento = serializers.DateField(required=False)
    
    def validate_valor_pago(self, value):
        """Validação do valor pago"""
        if value and value <= 0:
            raise serializers.ValidationError('Valor pago deve ser maior que zero')
        return value



