# -*- coding: utf-8 -*-
"""
Modelos do app Parcelas
"""

from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import BaseModel, StatusParcela


class Parcela(BaseModel):
    """
    Modelo para Parcelas
    Uma conta pode ter uma ou mais parcelas com datas de vencimento distintas
    """
    
    numero_parcela = models.PositiveIntegerField(
        'Número da Parcela',
        validators=[MinValueValidator(1)],
        help_text='Número sequencial da parcela'
    )
    
    data_vencimento = models.DateField(
        'Data de Vencimento',
        help_text='Data de vencimento da parcela'
    )
    
    valor = models.DecimalField(
        'Valor',
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text='Valor da parcela'
    )
    
    status = models.CharField(
        'Status',
        max_length=20,
        choices=StatusParcela.choices,
        default=StatusParcela.PENDENTE,
        help_text='Status da parcela'
    )
    
    data_pagamento = models.DateField(
        'Data de Pagamento',
        blank=True,
        null=True,
        help_text='Data em que a parcela foi paga'
    )
    
    valor_pago = models.DecimalField(
        'Valor Pago',
        max_digits=15,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text='Valor efetivamente pago'
    )
    
    observacoes = models.TextField(
        'Observações',
        blank=True,
        null=True,
        help_text='Observações sobre a parcela'
    )

    class Meta:
        verbose_name = 'Parcela'
        verbose_name_plural = 'Parcelas'
        ordering = ['data_vencimento', 'numero_parcela']
        indexes = [
            models.Index(fields=['data_vencimento']),
            models.Index(fields=['status']),
            models.Index(fields=['numero_parcela']),
            models.Index(fields=['ativo']),
        ]

    def __str__(self):
        return f"Parcela {self.numero_parcela} - R$ {self.valor} - {self.data_vencimento}"

    def is_vencida(self):
        """Verifica se a parcela está vencida"""
        from django.utils import timezone
        return self.data_vencimento < timezone.now().date() and self.status == StatusParcela.PENDENTE

    def is_paga(self):
        """Verifica se a parcela está paga"""
        return self.status == StatusParcela.PAGA

    def is_pendente(self):
        """Verifica se a parcela está pendente"""
        return self.status == StatusParcela.PENDENTE

    def marcar_como_paga(self, valor_pago=None, data_pagamento=None):
        """Marca a parcela como paga"""
        from django.utils import timezone
        
        self.status = StatusParcela.PAGA
        self.data_pagamento = data_pagamento or timezone.now().date()
        self.valor_pago = valor_pago or self.valor
        self.save()

    def marcar_como_vencida(self):
        """Marca a parcela como vencida"""
        if self.is_vencida():
            self.status = StatusParcela.VENCIDA
            self.save()

    def clean(self):
        """Validações adicionais"""
        from django.core.exceptions import ValidationError
        
        # Validar se valor pago não excede o valor da parcela
        if self.valor_pago > self.valor:
            raise ValidationError({
                'valor_pago': 'Valor pago não pode ser maior que o valor da parcela'
            })
        
        # Validar se data de pagamento é posterior ao vencimento quando paga
        if self.status == StatusParcela.PAGA and self.data_pagamento:
            if self.data_pagamento < self.data_vencimento:
                raise ValidationError({
                    'data_pagamento': 'Data de pagamento não pode ser anterior ao vencimento'
                })

    def save(self, *args, **kwargs):
        """Override save para aplicar validações"""
        self.full_clean()
        super().save(*args, **kwargs)



