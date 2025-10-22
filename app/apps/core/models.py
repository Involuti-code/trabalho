# -*- coding: utf-8 -*-
"""
Modelos base do Sistema Administrativo-Financeiro
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """
    Modelo base com campos comuns a todos os modelos
    """
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    ativo = models.BooleanField('Ativo', default=True)
    criado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='%(class)s_criado_por'
    )
    atualizado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='%(class)s_atualizado_por'
    )

    class Meta:
        abstract = True

    def inativar(self):
        """Inativa o registro (não exclui)"""
        self.ativo = False
        self.save()

    def reativar(self):
        """Reativa um registro inativo"""
        self.ativo = True
        self.save()

    def __str__(self):
        return f"{self.__class__.__name__} - {self.id}"


class CategoriaDespesa(models.TextChoices):
    """
    Categorias de despesas conforme especificado no projeto
    """
    INSUMOS_AGRICOLAS = 'INSUMOS_AGRICOLAS', 'Insumos Agrícolas'
    MANUTENCAO_OPERACAO = 'MANUTENCAO_OPERACAO', 'Manutenção e Operação'
    RECURSOS_HUMANOS = 'RECURSOS_HUMANOS', 'Recursos Humanos'
    SERVICOS_OPERACIONAIS = 'SERVICOS_OPERACIONAIS', 'Serviços Operacionais'
    INFRAESTRUTURA_UTILIDADES = 'INFRAESTRUTURA_UTILIDADES', 'Infraestrutura e Utilidades'
    ADMINISTRATIVAS = 'ADMINISTRATIVAS', 'Administrativas'
    SEGUROS_PROTECAO = 'SEGUROS_PROTECAO', 'Seguros e Proteção'
    IMPOSTOS_TAXAS = 'IMPOSTOS_TAXAS', 'Impostos e Taxas'
    INVESTIMENTOS = 'INVESTIMENTOS', 'Investimentos'


class StatusConta(models.TextChoices):
    """
    Status das contas a pagar e receber
    """
    PENDENTE = 'PENDENTE', 'Pendente'
    PAGA = 'PAGA', 'Paga'
    VENCIDA = 'VENCIDA', 'Vencida'
    CANCELADA = 'CANCELADA', 'Cancelada'


class StatusParcela(models.TextChoices):
    """
    Status das parcelas
    """
    PENDENTE = 'PENDENTE', 'Pendente'
    PAGA = 'PAGA', 'Paga'
    VENCIDA = 'VENCIDA', 'Vencida'
    CANCELADA = 'CANCELADA', 'Cancelada'



