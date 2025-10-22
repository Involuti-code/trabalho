# -*- coding: utf-8 -*-
"""
Modelos do app Processador de PDF
"""

from django.db import models
from django.core.validators import FileExtensionValidator
from apps.core.models import BaseModel


class ProcessamentoPDF(BaseModel):
    """
    Modelo para armazenar informações sobre processamento de PDFs
    """
    
    arquivo_pdf = models.FileField(
        'Arquivo PDF',
        upload_to='uploads/pdfs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='Arquivo PDF da nota fiscal'
    )
    
    nome_arquivo = models.CharField(
        'Nome do Arquivo',
        max_length=255,
        help_text='Nome original do arquivo'
    )
    
    tamanho_arquivo = models.BigIntegerField(
        'Tamanho do Arquivo',
        help_text='Tamanho do arquivo em bytes'
    )
    
    status_processamento = models.CharField(
        'Status do Processamento',
        max_length=20,
        choices=[
            ('PENDENTE', 'Pendente'),
            ('PROCESSANDO', 'Processando'),
            ('SUCESSO', 'Sucesso'),
            ('ERRO', 'Erro'),
            ('DUPLICADO', 'Duplicado'),
        ],
        default='PENDENTE',
        help_text='Status do processamento'
    )
    
    dados_extraidos = models.JSONField(
        'Dados Extraídos',
        blank=True,
        null=True,
        help_text='Dados extraídos do PDF em formato JSON'
    )
    
    erro_processamento = models.TextField(
        'Erro no Processamento',
        blank=True,
        null=True,
        help_text='Mensagem de erro se houver'
    )
    
    data_processamento = models.DateTimeField(
        'Data do Processamento',
        blank=True,
        null=True,
        help_text='Data e hora do processamento'
    )
    
    tempo_processamento = models.DurationField(
        'Tempo de Processamento',
        blank=True,
        null=True,
        help_text='Tempo gasto no processamento'
    )

    class Meta:
        verbose_name = 'Processamento de PDF'
        verbose_name_plural = 'Processamentos de PDF'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['status_processamento']),
            models.Index(fields=['data_processamento']),
            models.Index(fields=['ativo']),
        ]

    def __str__(self):
        return f"Processamento - {self.nome_arquivo} - {self.status_processamento}"
    
    def get_status_processamento_display(self):
        """Retorna o display do status do processamento"""
        status_map = {
            'PENDENTE': 'Pendente',
            'PROCESSANDO': 'Processando',
            'SUCESSO': 'Sucesso',
            'ERRO': 'Erro',
            'DUPLICADO': 'Duplicado',
        }
        return status_map.get(self.status_processamento, self.status_processamento)

    def iniciar_processamento(self):
        """Marca o processamento como iniciado"""
        self.status_processamento = 'PROCESSANDO'
        self.save()

    def finalizar_processamento(self, dados_extraidos=None, erro=None, tempo_processamento=None):
        """Finaliza o processamento com sucesso ou erro"""
        from django.utils import timezone
        
        self.data_processamento = timezone.now()
        self.tempo_processamento = tempo_processamento
        
        if erro:
            self.status_processamento = 'ERRO'
            self.erro_processamento = erro
        else:
            self.status_processamento = 'SUCESSO'
            self.dados_extraidos = dados_extraidos
        
        self.save()

    def is_processado(self):
        """Verifica se o processamento foi concluído"""
        return self.status_processamento in ['SUCESSO', 'ERRO']

    def is_sucesso(self):
        """Verifica se o processamento foi bem-sucedido"""
        return self.status_processamento == 'SUCESSO'

    def is_erro(self):
        """Verifica se houve erro no processamento"""
        return self.status_processamento == 'ERRO'

    def get_dados_fornecedor(self):
        """Retorna dados do fornecedor extraídos"""
        if self.dados_extraidos and 'fornecedor' in self.dados_extraidos:
            return self.dados_extraidos['fornecedor']
        return None

    def get_dados_faturado(self):
        """Retorna dados do faturado extraídos"""
        if self.dados_extraidos and 'faturado' in self.dados_extraidos:
            return self.dados_extraidos['faturado']
        return None

    def get_dados_nota_fiscal(self):
        """Retorna dados da nota fiscal extraídos"""
        if self.dados_extraidos and 'nota_fiscal' in self.dados_extraidos:
            return self.dados_extraidos['nota_fiscal']
        return None

    def get_dados_parcelas(self):
        """Retorna dados das parcelas extraídas"""
        if self.dados_extraidos and 'parcelas' in self.dados_extraidos:
            return self.dados_extraidos['parcelas']
        return None

    def get_classificacao_despesa(self):
        """Retorna classificação da despesa extraída"""
        if self.dados_extraidos and 'classificacao' in self.dados_extraidos:
            return self.dados_extraidos['classificacao']
        return None



