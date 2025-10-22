# -*- coding: utf-8 -*-
"""
Modelos do app Contas a Receber
"""

from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import BaseModel, StatusConta
from apps.clientes.models import Cliente
from apps.tipos_receita.models import TipoReceita
from apps.parcelas.models import Parcela


class ContaReceber(BaseModel):
    """
    Modelo para Contas a Receber
    """
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='contas_receber',
        help_text='Cliente da conta'
    )
    
    numero_documento = models.CharField(
        'Número do Documento',
        max_length=50,
        help_text='Número do documento (nota fiscal, recibo, etc.)'
    )
    
    data_emissao = models.DateField(
        'Data de Emissão',
        help_text='Data de emissão do documento'
    )
    
    descricao = models.TextField(
        'Descrição',
        help_text='Descrição dos produtos/serviços'
    )
    
    valor_total = models.DecimalField(
        'Valor Total',
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text='Valor total da conta'
    )
    
    quantidade_parcelas = models.PositiveIntegerField(
        'Quantidade de Parcelas',
        default=1,
        validators=[MinValueValidator(1)],
        help_text='Quantidade de parcelas'
    )
    
    status = models.CharField(
        'Status',
        max_length=20,
        choices=StatusConta.choices,
        default=StatusConta.PENDENTE,
        help_text='Status da conta'
    )
    
    observacoes = models.TextField(
        'Observações',
        blank=True,
        null=True,
        help_text='Observações adicionais'
    )
    
    # Relacionamento com parcelas
    parcelas = models.ManyToManyField(
        Parcela,
        blank=True,
        related_name='contas_receber',
        help_text='Parcelas da conta'
    )
    
    # Relacionamento com tipos de receita (múltiplas classificações)
    tipos_receita = models.ManyToManyField(
        TipoReceita,
        related_name='contas_receber',
        help_text='Classificação da receita'
    )

    class Meta:
        verbose_name = 'Conta a Receber'
        verbose_name_plural = 'Contas a Receber'
        ordering = ['-data_emissao', '-criado_em']
        indexes = [
            models.Index(fields=['numero_documento']),
            models.Index(fields=['data_emissao']),
            models.Index(fields=['status']),
            models.Index(fields=['cliente']),
            models.Index(fields=['ativo']),
        ]

    def __str__(self):
        return f"Conta a Receber - {self.numero_documento} - {self.cliente.nome}"

    def get_valor_recebido(self):
        """Retorna o valor total recebido"""
        return sum(parcela.valor_pago for parcela in self.parcelas.filter(status='PAGA'))

    def get_valor_pendente(self):
        """Retorna o valor pendente de recebimento"""
        return self.valor_total - self.get_valor_recebido()

    def get_parcelas_pagas(self):
        """Retorna as parcelas pagas"""
        return self.parcelas.filter(status='PAGA')

    def get_parcelas_pendentes(self):
        """Retorna as parcelas pendentes"""
        return self.parcelas.filter(status='PENDENTE')

    def get_parcelas_vencidas(self):
        """Retorna as parcelas vencidas"""
        return self.parcelas.filter(status='VENCIDA')

    def is_recebida(self):
        """Verifica se a conta foi totalmente recebida"""
        return self.get_valor_pendente() == 0

    def is_vencida(self):
        """Verifica se a conta tem parcelas vencidas"""
        return self.get_parcelas_vencidas().exists()

    def marcar_como_recebida(self):
        """Marca a conta como recebida"""
        if self.is_recebida():
            self.status = StatusConta.PAGA
            self.save()

    def clean(self):
        """Validações adicionais"""
        from django.core.exceptions import ValidationError
        
        # Validar se data de emissão não é futura
        from django.utils import timezone
        if self.data_emissao > timezone.now().date():
            raise ValidationError({
                'data_emissao': 'Data de emissão não pode ser futura'
            })

    def save(self, *args, **kwargs):
        """Override save para aplicar validações"""
        self.full_clean()
        super().save(*args, **kwargs)



