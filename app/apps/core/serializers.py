# -*- coding: utf-8 -*-
"""
Serializers base do Sistema Administrativo-Financeiro
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CategoriaDespesa, StatusConta, StatusParcela


class UserSerializer(serializers.ModelSerializer):
    """Serializer para usuários"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class BaseModelSerializer(serializers.ModelSerializer):
    """Serializer base com campos comuns"""
    
    criado_por_nome = serializers.CharField(source='criado_por.username', read_only=True)
    atualizado_por_nome = serializers.CharField(source='atualizado_por.username', read_only=True)
    
    class Meta:
        abstract = True
        fields = [
            'id', 'criado_em', 'atualizado_em', 'ativo',
            'criado_por', 'criado_por_nome',
            'atualizado_por', 'atualizado_por_nome'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class CategoriaDespesaSerializer(serializers.Serializer):
    """Serializer para categorias de despesa"""
    
    value = serializers.CharField()
    label = serializers.CharField()
    
    def to_representation(self, instance):
        return {
            'value': instance[0],
            'label': instance[1]
        }


class StatusContaSerializer(serializers.Serializer):
    """Serializer para status de conta"""
    
    value = serializers.CharField()
    label = serializers.CharField()
    
    def to_representation(self, instance):
        return {
            'value': instance[0],
            'label': instance[1]
        }


class StatusParcelaSerializer(serializers.Serializer):
    """Serializer para status de parcela"""
    
    value = serializers.CharField()
    label = serializers.CharField()
    
    def to_representation(self, instance):
        return {
            'value': instance[0],
            'label': instance[1]
        }



