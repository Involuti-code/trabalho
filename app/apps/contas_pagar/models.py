# -*- coding: utf-8 -*-
"""
Modelos do app Contas a Pagar
"""

from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import BaseModel, StatusConta
from apps.fornecedores.models import Fornecedor
from apps.faturados.models import Faturado
from apps.tipos_despesa.models import TipoDespesa
from apps.parcelas.models import Parcela


class ContaPagar(BaseModel):
    """
    Modelo para Contas a Pagar
    Campos obrigatórios conforme especificação:
    - Fornecedor
    - Faturado
    - Número da Nota Fiscal
    - Data de Emissão
    - Descrição dos produtos
    - Quantidade de Parcelas
    - Data de Vencimento
    - Valor Total
    - Classificação da DESPESA
    """
    
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        related_name='contas_pagar',
        help_text='Fornecedor da conta'
    )
    
    faturado = models.ForeignKey(
        Faturado,
        on_delete=models.PROTECT,
        related_name='contas_pagar',
        help_text='Faturado da conta'
    )
    
    numero_nota_fiscal = models.CharField(
        'Número da Nota Fiscal',
        max_length=50,
        help_text='Número da nota fiscal'
    )
    
    data_emissao = models.DateField(
        'Data de Emissão',
        help_text='Data de emissão da nota fiscal'
    )
    
    descricao_produtos = models.TextField(
        'Descrição dos Produtos',
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
        related_name='contas_pagar',
        help_text='Parcelas da conta'
    )
    
    # Relacionamento com tipos de despesa (múltiplas classificações)
    tipos_despesa = models.ManyToManyField(
        TipoDespesa,
        related_name='contas_pagar',
        help_text='Classificação da despesa'
    )

    class Meta:
        verbose_name = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
        ordering = ['-data_emissao', '-criado_em']
        indexes = [
            models.Index(fields=['numero_nota_fiscal']),
            models.Index(fields=['data_emissao']),
            models.Index(fields=['status']),
            models.Index(fields=['fornecedor']),
            models.Index(fields=['faturado']),
            models.Index(fields=['ativo']),
        ]

    def __str__(self):
        return f"Conta a Pagar - {self.numero_nota_fiscal} - {self.fornecedor.razao_social}"

    def get_valor_pago(self):
        """Retorna o valor total pago"""
        return sum(parcela.valor_pago for parcela in self.parcelas.filter(status='PAGA'))

    def get_valor_pendente(self):
        """Retorna o valor pendente de pagamento"""
        return self.valor_total - self.get_valor_pago()

    def get_parcelas_pagas(self):
        """Retorna as parcelas pagas"""
        return self.parcelas.filter(status='PAGA')

    def get_parcelas_pendentes(self):
        """Retorna as parcelas pendentes"""
        return self.parcelas.filter(status='PENDENTE')

    def get_parcelas_vencidas(self):
        """Retorna as parcelas vencidas"""
        return self.parcelas.filter(status='VENCIDA')

    def is_paga(self):
        """Verifica se a conta está totalmente paga"""
        return self.get_valor_pendente() == 0

    def is_vencida(self):
        """Verifica se a conta tem parcelas vencidas"""
        return self.get_parcelas_vencidas().exists()

    def marcar_como_paga(self):
        """Marca a conta como paga"""
        if self.is_paga():
            self.status = StatusConta.PAGA
            self.save()

    def classificar_automaticamente(self):
        """Classifica automaticamente baseado na descrição dos produtos"""
        tipo_despesa = TipoDespesa.classificar_por_descricao(self.descricao_produtos)
        if tipo_despesa:
            self.tipos_despesa.add(tipo_despesa)

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
        """Override save para aplicar validações e classificação automática"""
        self.full_clean()
        super().save(*args, **kwargs)
        
        # Classificar automaticamente se não tiver classificação
        if not self.tipos_despesa.exists():
            self.classificar_automaticamente()



