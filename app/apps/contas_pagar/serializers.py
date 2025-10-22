# -*- coding: utf-8 -*-
"""
Serializers do app Contas a Pagar
"""

from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from apps.fornecedores.serializers import FornecedorListSerializer
from apps.faturados.serializers import FaturadoListSerializer
from apps.tipos_despesa.serializers import TipoDespesaListSerializer
from apps.parcelas.serializers import ParcelaListSerializer
from .models import ContaPagar


class ContaPagarSerializer(BaseModelSerializer):
    """Serializer para Conta a Pagar"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    fornecedor_nome = serializers.CharField(source='fornecedor.razao_social', read_only=True)
    faturado_nome = serializers.CharField(source='faturado.nome_completo', read_only=True)
    valor_pago = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    valor_pendente = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    is_paga = serializers.BooleanField(read_only=True)
    is_vencida = serializers.BooleanField(read_only=True)
    
    # Relacionamentos
    fornecedor = FornecedorListSerializer(read_only=True)
    faturado = FaturadoListSerializer(read_only=True)
    tipos_despesa = TipoDespesaListSerializer(many=True, read_only=True)
    parcelas = ParcelaListSerializer(many=True, read_only=True)
    
    class Meta:
        model = ContaPagar
        fields = BaseModelSerializer.Meta.fields + [
            'fornecedor', 'fornecedor_nome', 'faturado', 'faturado_nome',
            'numero_nota_fiscal', 'data_emissao', 'descricao_produtos',
            'valor_total', 'quantidade_parcelas', 'status', 'status_display',
            'observacoes', 'tipos_despesa', 'parcelas',
            'valor_pago', 'valor_pendente', 'is_paga', 'is_vencida'
        ]


class ContaPagarListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Contas a Pagar"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    fornecedor_nome = serializers.CharField(source='fornecedor.razao_social', read_only=True)
    faturado_nome = serializers.CharField(source='faturado.nome_completo', read_only=True)
    valor_pago = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    valor_pendente = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    is_vencida = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = ContaPagar
        fields = [
            'id', 'numero_nota_fiscal', 'fornecedor_nome', 'faturado_nome',
            'data_emissao', 'valor_total', 'valor_pago', 'valor_pendente',
            'status', 'status_display', 'is_vencida', 'ativo'
        ]


class ContaPagarCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de Conta a Pagar"""
    
    class Meta:
        model = ContaPagar
        fields = [
            'fornecedor', 'faturado', 'numero_nota_fiscal', 'data_emissao',
            'descricao_produtos', 'valor_total', 'quantidade_parcelas',
            'observacoes', 'tipos_despesa'
        ]
    
    def validate_data_emissao(self, value):
        """Validação da data de emissão"""
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError('Data de emissão não pode ser futura')
        return value


class ContaPagarUpdateSerializer(ContaPagarCreateSerializer):
    """Serializer para atualização de Conta a Pagar"""
    
    class Meta(ContaPagarCreateSerializer.Meta):
        fields = ContaPagarCreateSerializer.Meta.fields + ['status', 'ativo']


class ContaPagarClassificarSerializer(serializers.Serializer):
    """Serializer para classificação automática de contas a pagar"""
    
    conta_id = serializers.IntegerField()
    
    def validate_conta_id(self, value):
        """Validação do ID da conta"""
        try:
            conta = ContaPagar.objects.get(id=value)
            if not conta.ativo:
                raise serializers.ValidationError('Conta não está ativa')
        except ContaPagar.DoesNotExist:
            raise serializers.ValidationError('Conta não encontrada')
        return value



