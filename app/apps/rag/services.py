# -*- coding: utf-8 -*-
"""
Serviços RAG - Retrieval-Augmented Generation
"""

import json
import time
import requests
from typing import Dict, Any, List, Optional
from django.db.models import Q
from django.db import models

# Importar modelos do banco de dados
from apps.clientes.models import Cliente
from apps.fornecedores.models import Fornecedor
from apps.contas_pagar.models import ContaPagar
from apps.contas_receber.models import ContaReceber
from apps.parcelas.models import Parcela
from apps.tipos_despesa.models import TipoDespesa
from apps.tipos_receita.models import TipoReceita
from apps.faturados.models import Faturado
from apps.pdf_processor.models import ProcessamentoPDF


class GeminiService:
    """
    Serviço para integração com Google Gemini AI
    Reutiliza a mesma API já configurada no projeto
    """
    
    def __init__(self):
        import os
        from decouple import config
        self.api_key = config('GEMINI_API_KEY', default=os.environ.get('GEMINI_API_KEY', ''))
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    def generate_response(self, prompt: str) -> str:
        """
        Gera resposta usando Gemini AI
        """
        try:
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            
            response = requests.post(url, json=data, headers=headers, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        return candidate['content']['parts'][0]['text']
                
                raise Exception("Resposta da IA não contém dados válidos")
            else:
                raise Exception(f"Erro na API do Gemini: {response.status_code} - {response.text}")
                
        except Exception as e:
            raise Exception(f"Erro ao gerar resposta: {str(e)}")


class RAGSimpleService:
    """
    Serviço RAG Simples - Busca por palavras-chave no banco de dados
    """
    
    def __init__(self):
        self.gemini_service = GeminiService()
    
    def _buscar_clientes(self, query: str) -> List[Dict]:
        """Busca clientes por palavras-chave"""
        try:
            palavras = query.lower().split()
            q_objects = Q()
            
            # Termos relacionados a clientes
            termos_clientes = ['cliente', 'clientes', 'pessoa', 'cpf']
            tem_termo_relacionado = any(termo in query.lower() for termo in termos_clientes)
            
            for palavra in palavras:
                if len(palavra) > 2:  # Ignorar palavras muito curtas
                    q_objects |= Q(nome__icontains=palavra) | Q(cpf__icontains=palavra) | Q(email__icontains=palavra)
            
            # Se tiver termo relacionado mas não encontrou nada, buscar alguns clientes
            if tem_termo_relacionado and not q_objects:
                clientes = Cliente.objects.filter(ativo=True)[:10]
            else:
                clientes = Cliente.objects.filter(q_objects, ativo=True)[:10]
            
            resultados = []
            for cliente in clientes:
                resultados.append({
                    'tipo': 'Cliente',
                    'id': cliente.id,
                    'nome': cliente.nome,
                    'cpf': cliente.cpf,
                    'email': cliente.email,
                    'telefone': cliente.telefone,
                    'endereco': cliente.endereco,
                })
            
            return resultados
        except Exception as e:
            print(f"Erro ao buscar clientes: {str(e)}")
            return []
    
    def _buscar_fornecedores(self, query: str) -> List[Dict]:
        """Busca fornecedores por palavras-chave"""
        try:
            palavras = query.lower().split()
            q_objects = Q()
            
            # Termos relacionados a fornecedores
            termos_fornecedores = ['fornecedor', 'fornecedores', 'empresa', 'cnpj', 'fornecedor']
            tem_termo_relacionado = any(termo in query.lower() for termo in termos_fornecedores)
            
            for palavra in palavras:
                if len(palavra) > 2:  # Ignorar palavras muito curtas
                    q_objects |= Q(razao_social__icontains=palavra) | Q(fantasia__icontains=palavra) | Q(cnpj__icontains=palavra)
            
            # Se tiver termo relacionado mas não encontrou nada, buscar alguns fornecedores
            if tem_termo_relacionado and not q_objects:
                fornecedores = Fornecedor.objects.filter(ativo=True)[:10]
            else:
                fornecedores = Fornecedor.objects.filter(q_objects, ativo=True)[:10]
            
            resultados = []
            for fornecedor in fornecedores:
                resultados.append({
                    'tipo': 'Fornecedor',
                    'id': fornecedor.id,
                    'razao_social': fornecedor.razao_social,
                    'fantasia': fornecedor.fantasia,
                    'cnpj': fornecedor.cnpj,
                    'email': fornecedor.email,
                    'telefone': fornecedor.telefone,
                })
            
            return resultados
        except Exception as e:
            print(f"Erro ao buscar fornecedores: {str(e)}")
            return []
    
    def _buscar_contas_pagar(self, query: str) -> List[Dict]:
        """Busca contas a pagar por palavras-chave"""
        try:
            palavras = query.lower().split()
            q_objects = Q()
            
            # Termos relacionados a contas a pagar (incluindo parcelas)
            termos_contas = ['pagar', 'pagamento', 'conta', 'nota', 'fiscal', 'fornecedor', 'despesa', 'parcela', 'parcelas', 'vencimento', 'vencida']
            tem_termo_relacionado = any(termo in query.lower() for termo in termos_contas)
            
            # Se tiver termo relacionado a parcelas/pagamentos, buscar todas as contas
            if tem_termo_relacionado:
                contas = ContaPagar.objects.filter(ativo=True).select_related('fornecedor', 'faturado').prefetch_related('parcelas')[:20]
            else:
                for palavra in palavras:
                    if len(palavra) > 2:  # Ignorar palavras muito curtas
                        q_objects |= Q(numero_nota_fiscal__icontains=palavra) | Q(descricao_produtos__icontains=palavra) | Q(fornecedor__razao_social__icontains=palavra)
                
                contas = ContaPagar.objects.filter(q_objects, ativo=True).select_related('fornecedor', 'faturado').prefetch_related('parcelas')[:20]
            
            resultados = []
            for conta in contas:
                # Buscar parcelas relacionadas
                parcelas_info = []
                for parcela in conta.parcelas.all()[:5]:  # Limitar a 5 parcelas
                    parcelas_info.append({
                        'numero': parcela.numero_parcela,
                        'valor': float(parcela.valor),
                        'vencimento': str(parcela.data_vencimento),
                        'status': parcela.status,
                        'valor_pago': float(parcela.valor_pago),
                    })
                
                resultado = {
                    'tipo': 'Conta a Pagar',
                    'id': conta.id,
                    'numero_nota_fiscal': conta.numero_nota_fiscal,
                    'fornecedor': conta.fornecedor.razao_social,
                    'data_emissao': str(conta.data_emissao),
                    'valor_total': float(conta.valor_total),
                    'status': conta.status,
                    'quantidade_parcelas': conta.quantidade_parcelas,
                    'descricao': conta.descricao_produtos[:200],
                }
                
                if parcelas_info:
                    resultado['parcelas'] = parcelas_info
                
                resultados.append(resultado)
            
            return resultados
        except Exception as e:
            print(f"Erro ao buscar contas a pagar: {str(e)}")
            return []
    
    def _buscar_contas_receber(self, query: str) -> List[Dict]:
        """Busca contas a receber por palavras-chave"""
        try:
            palavras = query.lower().split()
            q_objects = Q()
            
            # Termos relacionados a contas a receber (incluindo parcelas)
            termos_contas = ['receber', 'recebimento', 'conta', 'cliente', 'receita', 'parcela', 'parcelas', 'vencimento', 'vencida']
            tem_termo_relacionado = any(termo in query.lower() for termo in termos_contas)
            
            # Se tiver termo relacionado, buscar todas as contas
            if tem_termo_relacionado:
                contas = ContaReceber.objects.filter(ativo=True).select_related('cliente').prefetch_related('parcelas')[:20]
            else:
                for palavra in palavras:
                    if len(palavra) > 2:  # Ignorar palavras muito curtas
                        q_objects |= Q(numero_documento__icontains=palavra) | Q(descricao__icontains=palavra) | Q(cliente__nome__icontains=palavra)
                
                contas = ContaReceber.objects.filter(q_objects, ativo=True).select_related('cliente').prefetch_related('parcelas')[:20]
            
            resultados = []
            for conta in contas:
                # Buscar parcelas relacionadas
                parcelas_info = []
                for parcela in conta.parcelas.all()[:5]:  # Limitar a 5 parcelas
                    parcelas_info.append({
                        'numero': parcela.numero_parcela,
                        'valor': float(parcela.valor),
                        'vencimento': str(parcela.data_vencimento),
                        'status': parcela.status,
                        'valor_pago': float(parcela.valor_pago),
                    })
                
                resultado = {
                    'tipo': 'Conta a Receber',
                    'id': conta.id,
                    'numero_documento': conta.numero_documento,
                    'cliente': conta.cliente.nome,
                    'data_emissao': str(conta.data_emissao),
                    'valor_total': float(conta.valor_total),
                    'status': conta.status,
                    'quantidade_parcelas': conta.quantidade_parcelas,
                    'descricao': conta.descricao[:200],
                }
                
                if parcelas_info:
                    resultado['parcelas'] = parcelas_info
                
                resultados.append(resultado)
            
            return resultados
        except Exception as e:
            # Se a tabela não existir ou houver erro, retornar lista vazia
            print(f"Erro ao buscar contas a receber: {str(e)}")
            return []
    
    def _buscar_faturados(self, query: str) -> List[Dict]:
        """Busca faturados por palavras-chave"""
        try:
            palavras = query.lower().split()
            q_objects = Q()
            
            # Termos relacionados a faturados
            termos_faturados = ['faturado', 'faturados', 'cpf', 'pessoa']
            tem_termo_relacionado = any(termo in query.lower() for termo in termos_faturados)
            
            for palavra in palavras:
                if len(palavra) > 2:
                    q_objects |= Q(nome_completo__icontains=palavra) | Q(cpf__icontains=palavra) | Q(email__icontains=palavra)
            
            if tem_termo_relacionado and not q_objects:
                faturados = Faturado.objects.filter(ativo=True)[:10]
            else:
                faturados = Faturado.objects.filter(q_objects, ativo=True)[:10]
            
            resultados = []
            for faturado in faturados:
                resultados.append({
                    'tipo': 'Faturado',
                    'id': faturado.id,
                    'nome_completo': faturado.nome_completo,
                    'cpf': faturado.cpf,
                    'email': faturado.email,
                    'telefone': faturado.telefone,
                    'endereco': faturado.endereco,
                })
            
            return resultados
        except Exception as e:
            print(f"Erro ao buscar faturados: {str(e)}")
            return []
    
    def _buscar_tipos_despesa(self, query: str) -> List[Dict]:
        """Busca tipos de despesa por palavras-chave"""
        try:
            palavras = query.lower().split()
            q_objects = Q()
            
            # Termos relacionados a tipos de despesa
            termos_despesa = ['despesa', 'despesas', 'categoria', 'classificação', 'classificacao', 'tipo']
            tem_termo_relacionado = any(termo in query.lower() for termo in termos_despesa)
            
            for palavra in palavras:
                if len(palavra) > 2:
                    q_objects |= Q(nome__icontains=palavra) | Q(descricao__icontains=palavra) | Q(codigo__icontains=palavra) | Q(categoria__icontains=palavra)
            
            if tem_termo_relacionado and not q_objects:
                tipos = TipoDespesa.objects.filter(ativo=True)[:20]
            else:
                tipos = TipoDespesa.objects.filter(q_objects, ativo=True)[:20]
            
            resultados = []
            for tipo in tipos:
                resultados.append({
                    'tipo': 'Tipo de Despesa',
                    'id': tipo.id,
                    'nome': tipo.nome,
                    'codigo': tipo.codigo,
                    'categoria': tipo.get_categoria_display(),
                    'descricao': tipo.descricao[:200] if tipo.descricao else None,
                })
            
            return resultados
        except Exception as e:
            print(f"Erro ao buscar tipos de despesa: {str(e)}")
            return []
    
    def _buscar_tipos_receita(self, query: str) -> List[Dict]:
        """Busca tipos de receita por palavras-chave"""
        try:
            palavras = query.lower().split()
            q_objects = Q()
            
            # Termos relacionados a tipos de receita
            termos_receita = ['receita', 'receitas', 'categoria', 'classificação', 'classificacao', 'tipo']
            tem_termo_relacionado = any(termo in query.lower() for termo in termos_receita)
            
            for palavra in palavras:
                if len(palavra) > 2:
                    q_objects |= Q(nome__icontains=palavra) | Q(descricao__icontains=palavra) | Q(codigo__icontains=palavra)
            
            if tem_termo_relacionado and not q_objects:
                tipos = TipoReceita.objects.filter(ativo=True)[:20]
            else:
                tipos = TipoReceita.objects.filter(q_objects, ativo=True)[:20]
            
            resultados = []
            for tipo in tipos:
                resultados.append({
                    'tipo': 'Tipo de Receita',
                    'id': tipo.id,
                    'nome': tipo.nome,
                    'codigo': tipo.codigo,
                    'descricao': tipo.descricao[:200] if tipo.descricao else None,
                })
            
            return resultados
        except Exception as e:
            print(f"Erro ao buscar tipos de receita: {str(e)}")
            return []
    
    def _buscar_processamentos_pdf(self, query: str) -> List[Dict]:
        """Busca processamentos de PDF por palavras-chave"""
        try:
            palavras = query.lower().split()
            q_objects = Q()
            
            # Termos relacionados a PDFs
            termos_pdf = ['pdf', 'pdfs', 'processado', 'processados', 'processamento', 'nota', 'fiscal', 'boleto', 'boletos']
            tem_termo_relacionado = any(termo in query.lower() for termo in termos_pdf)
            
            for palavra in palavras:
                if len(palavra) > 2:
                    q_objects |= Q(nome_arquivo__icontains=palavra) | Q(status_processamento__icontains=palavra)
            
            if tem_termo_relacionado:
                if q_objects:
                    processamentos = ProcessamentoPDF.objects.filter(q_objects, ativo=True).order_by('-criado_em')[:20]
                else:
                    processamentos = ProcessamentoPDF.objects.filter(ativo=True).order_by('-criado_em')[:20]
            else:
                processamentos = ProcessamentoPDF.objects.filter(q_objects, ativo=True).order_by('-criado_em')[:20]
            
            resultados = []
            for proc in processamentos:
                resultado = {
                    'tipo': 'Processamento PDF',
                    'id': proc.id,
                    'nome_arquivo': proc.nome_arquivo,
                    'status': proc.get_status_processamento_display(),
                    'data_processamento': str(proc.data_processamento) if proc.data_processamento else None,
                    'tamanho_arquivo': f"{proc.tamanho_arquivo / 1024:.2f} KB" if proc.tamanho_arquivo else None,
                }
                
                # Adicionar informações dos dados extraídos se disponível
                if proc.dados_extraidos:
                    if 'fornecedor' in proc.dados_extraidos:
                        resultado['fornecedor_extraido'] = proc.dados_extraidos['fornecedor'].get('nome', 'N/A')
                    if 'numero' in proc.dados_extraidos:
                        resultado['numero_nota'] = proc.dados_extraidos.get('numero', 'N/A')
                    if 'totais' in proc.dados_extraidos and 'total' in proc.dados_extraidos['totais']:
                        resultado['valor_total'] = proc.dados_extraidos['totais']['total']
                
                resultados.append(resultado)
            
            return resultados
        except Exception as e:
            print(f"Erro ao buscar processamentos PDF: {str(e)}")
            return []
    
    def _buscar_parcelas(self, query: str) -> List[Dict]:
        """Busca parcelas por palavras-chave"""
        try:
            palavras = query.lower().split()
            q_objects = Q()
            
            # Termos relacionados a parcelas
            termos_parcelas = ['parcela', 'parcelas', 'vencimento', 'vencida', 'pagar', 'pagamento', 'pendente']
            tem_termo_relacionado = any(termo in query.lower() for termo in termos_parcelas)
            
            # Se tiver termo relacionado a parcelas, buscar todas ou filtrar
            if tem_termo_relacionado:
                for palavra in palavras:
                    if len(palavra) > 2:
                        q_objects |= Q(status__icontains=palavra) | Q(observacoes__icontains=palavra)
                
                if q_objects:
                    parcelas = Parcela.objects.filter(q_objects, ativo=True).order_by('-data_vencimento')[:20]
                else:
                    # Se não houver filtro específico mas tiver termo relacionado, buscar todas
                    parcelas = Parcela.objects.filter(ativo=True).order_by('-data_vencimento')[:20]
            else:
                return []  # Se não tiver termo relacionado, não buscar parcelas
            
            resultados = []
            for parcela in parcelas:
                resultados.append({
                    'tipo': 'Parcela',
                    'id': parcela.id,
                    'numero_parcela': parcela.numero_parcela,
                    'valor': float(parcela.valor),
                    'valor_pago': float(parcela.valor_pago),
                    'data_vencimento': str(parcela.data_vencimento),
                    'data_pagamento': str(parcela.data_pagamento) if parcela.data_pagamento else None,
                    'status': parcela.status,
                    'observacoes': parcela.observacoes[:100] if parcela.observacoes else None,
                })
            
            return resultados
        except Exception as e:
            print(f"Erro ao buscar parcelas: {str(e)}")
            return []
    
    def _get_contexto_sistema(self) -> str:
        """
        Retorna contexto explicativo sobre o sistema
        """
        return """=== CONTEXTO DO SISTEMA ADMINISTRATIVO-FINANCEIRO ===

Este é um sistema administrativo-financeiro para gestão de despesas e receitas, especialmente focado em operações agrícolas.

FUNCIONALIDADES PRINCIPAIS:

1. PROCESSAMENTO DE PDFs:
   - O sistema processa PDFs de notas fiscais e boletos usando Inteligência Artificial (Google Gemini)
   - Os PDFs são extraídos, analisados e classificados automaticamente
   - Os dados extraídos são armazenados em ProcessamentoPDF

2. CLASSIFICAÇÕES E ENTIDADES DO SISTEMA:

   a) FORNECEDORES:
      - Empresas que fornecem produtos/serviços
      - Campos: Razão Social, Nome Fantasia, CNPJ, Email, Telefone, Endereço
      - Relacionado com: Contas a Pagar

   b) CLIENTES:
      - Pessoas físicas que compram produtos/serviços
      - Campos: Nome, CPF, Email, Telefone, Endereço, Data de Nascimento
      - Relacionado com: Contas a Receber

   c) FATURADOS:
      - Pessoas físicas para quem as notas fiscais são emitidas
      - Campos: Nome Completo, CPF, Email, Telefone, Endereço
      - Relacionado com: Contas a Pagar

   d) TIPOS DE DESPESA:
      - Classificação das despesas em categorias:
        * INSUMOS_AGRICOLAS: Sementes, Fertilizantes, Defensivos, Corretivos
        * MANUTENCAO_OPERACAO: Combustíveis, Peças, Manutenção, Ferramentas
        * RECURSOS_HUMANOS: Mão de Obra, Salários, Encargos
        * SERVICOS_OPERACIONAIS: Frete, Colheita, Secagem, Pulverização
        * INFRAESTRUTURA_UTILIDADES: Energia, Arrendamento, Construções
        * ADMINISTRATIVAS: Honorários, Despesas Bancárias
        * SEGUROS_PROTECAO: Seguro Agrícola, Seguro de Ativos
        * IMPOSTOS_TAXAS: ITR, IPTU, IPVA, INCRA-CCIR
        * INVESTIMENTOS: Máquinas, Veículos, Imóveis, Infraestrutura
        * OUTROS: Outras despesas não categorizadas
      - Relacionado com: Contas a Pagar

   e) TIPOS DE RECEITA:
      - Classificação das receitas
      - Campos: Nome, Descrição, Código
      - Relacionado com: Contas a Receber

   f) CONTAS A PAGAR:
      - Notas fiscais e faturas que a empresa deve pagar
      - Campos: Fornecedor, Faturado, Número da Nota Fiscal, Data de Emissão, 
                Descrição dos Produtos, Valor Total, Quantidade de Parcelas, Status
      - Status: PENDENTE, PAGA, VENCIDA, CANCELADA
      - Relacionado com: Fornecedor, Faturado, Parcelas, Tipos de Despesa

   g) CONTAS A RECEBER:
      - Documentos e faturas que a empresa deve receber
      - Campos: Cliente, Número do Documento, Data de Emissão, Descrição,
                Valor Total, Quantidade de Parcelas, Status
      - Status: PENDENTE, PAGA, VENCIDA, CANCELADA
      - Relacionado com: Cliente, Parcelas, Tipos de Receita

   h) PARCELAS:
      - Divisão de contas em múltiplas parcelas com datas de vencimento distintas
      - Campos: Número da Parcela, Data de Vencimento, Valor, Status,
                Data de Pagamento, Valor Pago
      - Status: PENDENTE, PAGA, VENCIDA, CANCELADA
      - Relacionado com: Contas a Pagar, Contas a Receber

   i) PROCESSAMENTO DE PDF:
      - Registro de todos os PDFs processados pelo sistema
      - Campos: Nome do Arquivo, Tamanho, Status do Processamento,
                Dados Extraídos (JSON), Erro (se houver), Data de Processamento
      - Status: PENDENTE, PROCESSANDO, SUCESSO, ERRO, DUPLICADO
      - Os dados extraídos incluem: Fornecedor, Cliente, Nota Fiscal, Itens, Parcelas, Classificação

3. FLUXO DE TRABALHO:
   - PDF de nota fiscal/boleto é enviado ao sistema
   - IA extrai dados do PDF (fornecedor, valores, produtos, parcelas)
   - Sistema classifica automaticamente a despesa
   - Dados são armazenados em Contas a Pagar com Parcelas associadas
   - Sistema permite consulta e gestão de todas as informações

4. CONSULTAS DISPONÍVEIS:
   - Quantidade de registros em cada tabela
   - Valores totais a pagar/receber
   - Parcelas pendentes/vencidas
   - Status de processamento de PDFs
   - Classificações de despesas/receitas
   - Informações de fornecedores/clientes/faturados

===========================================
"""
    
    def buscar_contexto(self, query: str) -> str:
        """
        Busca contexto no banco de dados usando palavras-chave
        """
        # Contexto inicial do sistema
        contexto = self._get_contexto_sistema() + "\n"
        
        resultados = []
        
        # Buscar em todas as tabelas
        resultados.extend(self._buscar_clientes(query))
        resultados.extend(self._buscar_fornecedores(query))
        resultados.extend(self._buscar_contas_pagar(query))
        resultados.extend(self._buscar_contas_receber(query))
        resultados.extend(self._buscar_parcelas(query))
        resultados.extend(self._buscar_faturados(query))
        resultados.extend(self._buscar_tipos_despesa(query))
        resultados.extend(self._buscar_tipos_receita(query))
        resultados.extend(self._buscar_processamentos_pdf(query))
        
        # Adicionar estatísticas gerais se a pergunta for sobre quantidade
        termos_quantidade = ['quantos', 'quantas', 'quantidade', 'total', 'qtd', 'contar', 'contagem']
        if any(termo in query.lower() for termo in termos_quantidade):
            try:
                contexto += "=== ESTATÍSTICAS GERAIS DO BANCO DE DADOS ===\n\n"
                contexto += f"- Total de Clientes: {Cliente.objects.filter(ativo=True).count()}\n"
                contexto += f"- Total de Fornecedores: {Fornecedor.objects.filter(ativo=True).count()}\n"
                contexto += f"- Total de Faturados: {Faturado.objects.filter(ativo=True).count()}\n"
                contexto += f"- Total de Contas a Pagar: {ContaPagar.objects.filter(ativo=True).count()}\n"
                contexto += f"- Total de Contas a Receber: {ContaReceber.objects.filter(ativo=True).count()}\n"
                contexto += f"- Total de Parcelas: {Parcela.objects.filter(ativo=True).count()}\n"
                contexto += f"- Total de Tipos de Despesa: {TipoDespesa.objects.filter(ativo=True).count()}\n"
                contexto += f"- Total de Tipos de Receita: {TipoReceita.objects.filter(ativo=True).count()}\n"
                contexto += f"- Total de PDFs Processados: {ProcessamentoPDF.objects.filter(ativo=True).count()}\n"
                contexto += f"- PDFs com Sucesso: {ProcessamentoPDF.objects.filter(ativo=True, status_processamento='SUCESSO').count()}\n"
                contexto += f"- PDFs com Erro: {ProcessamentoPDF.objects.filter(ativo=True, status_processamento='ERRO').count()}\n"
                contexto += f"- PDFs Pendentes: {ProcessamentoPDF.objects.filter(ativo=True, status_processamento='PENDENTE').count()}\n"
                contexto += "\n"
            except Exception as e:
                print(f"Erro ao calcular estatísticas: {str(e)}")
        
        # Adicionar dados encontrados
        if resultados:
            contexto += "=== DADOS ENCONTRADOS NO BANCO DE DADOS ===\n\n"
            for i, resultado in enumerate(resultados[:30], 1):  # Limitar a 30 resultados
                contexto += f"{i}. {resultado['tipo']}:\n"
                for chave, valor in resultado.items():
                    if chave != 'tipo':
                        if isinstance(valor, list):
                            contexto += f"   - {chave}:\n"
                            for item in valor:
                                if isinstance(item, dict):
                                    contexto += f"     * {item}\n"
                                else:
                                    contexto += f"     * {item}\n"
                        else:
                            contexto += f"   - {chave}: {valor}\n"
                contexto += "\n"
        else:
            contexto += "Nenhum resultado específico encontrado no banco de dados para a consulta.\n"
        
        return contexto
    
    def processar_consulta(self, pergunta: str) -> Dict[str, Any]:
        """
        Processa uma consulta usando RAG simples
        """
        inicio = time.time()
        
        try:
            # 1. Buscar contexto no banco de dados
            contexto = self.buscar_contexto(pergunta)
            
            # 2. Criar prompt para o LLM
            prompt = f"""Você é um assistente especializado em análise de dados financeiros e administrativos de um sistema agrícola.

{contexto}

Pergunta do usuário: {pergunta}

INSTRUÇÕES PARA RESPOSTA:
1. Use o contexto do sistema fornecido acima para entender a estrutura e funcionamento
2. Analise os dados encontrados no banco de dados
3. Se a pergunta for sobre quantidade, calcule e apresente números exatos
4. Se a pergunta for sobre valores, apresente totais e detalhes quando relevante
5. Se a pergunta for sobre status ou classificações, explique claramente
6. Se não houver dados suficientes, explique o que seria necessário e o que foi encontrado
7. Sempre mencione as fontes dos dados (tabelas/entidades) quando relevante
8. Seja claro, detalhado e útil na resposta

Resposta:"""
            
            # 3. Gerar resposta com LLM
            resposta = self.gemini_service.generate_response(prompt)
            
            tempo_resposta = time.time() - inicio
            
            return {
                'success': True,
                'resposta': resposta,
                'contexto': contexto,
                'tempo_resposta': tempo_resposta,
                'tipo_rag': 'SIMPLES'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'tempo_resposta': time.time() - inicio,
                'tipo_rag': 'SIMPLES'
            }


class RAGEmbeddingsService:
    """
    Serviço RAG com Embeddings - Busca semântica usando embeddings
    """
    
    def __init__(self):
        self.gemini_service = GeminiService()
        self._model = None
    
    def _get_embedding_model(self):
        """
        Obtém o modelo de embeddings
        Usa sentence-transformers se disponível, senão usa busca simples
        """
        try:
            if self._model is None:
                try:
                    from sentence_transformers import SentenceTransformer
                    # Usar modelo multilíngue para português
                    self._model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
                except ImportError:
                    # Se não tiver sentence-transformers, usar busca simples
                    self._model = 'simple'
            return self._model
        except Exception:
            return 'simple'
    
    def _gerar_embedding(self, texto: str) -> List[float]:
        """
        Gera embedding para um texto
        """
        model = self._get_embedding_model()
        
        if model == 'simple':
            # Fallback: retornar None para usar busca simples
            return None
        
        try:
            embedding = model.encode(texto, convert_to_numpy=True)
            return embedding.tolist()
        except Exception:
            return None
    
    def _calcular_similaridade(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calcula similaridade de cosseno entre dois embeddings
        """
        try:
            import numpy as np
            
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return float(dot_product / (norm1 * norm2))
        except Exception:
            return 0.0
    
    def _buscar_semanticamente(self, query: str, limite: int = 10) -> List[Dict]:
        """
        Busca semântica no banco de dados usando embeddings
        """
        # Gerar embedding da query
        query_embedding = self._gerar_embedding(query)
        
        if query_embedding is None:
            # Fallback para busca simples
            rag_simple = RAGSimpleService()
            contexto = rag_simple.buscar_contexto(query)
            return contexto
        
        resultados_com_similaridade = []
        
        # Buscar clientes
        try:
            clientes = Cliente.objects.filter(ativo=True)[:50]
            for cliente in clientes:
                texto = f"{cliente.nome} {cliente.cpf} {cliente.email or ''} {cliente.endereco or ''}"
                texto_embedding = self._gerar_embedding(texto)
                if texto_embedding:
                    similaridade = self._calcular_similaridade(query_embedding, texto_embedding)
                    resultados_com_similaridade.append({
                        'similaridade': similaridade,
                        'tipo': 'Cliente',
                        'dados': {
                            'id': cliente.id,
                            'nome': cliente.nome,
                            'cpf': cliente.cpf,
                            'email': cliente.email,
                            'telefone': cliente.telefone,
                        }
                    })
        except Exception as e:
            print(f"Erro ao buscar clientes (embeddings): {str(e)}")
        
        # Buscar fornecedores
        try:
            fornecedores = Fornecedor.objects.filter(ativo=True)[:50]
            for fornecedor in fornecedores:
                texto = f"{fornecedor.razao_social} {fornecedor.fantasia or ''} {fornecedor.cnpj}"
                texto_embedding = self._gerar_embedding(texto)
                if texto_embedding:
                    similaridade = self._calcular_similaridade(query_embedding, texto_embedding)
                    resultados_com_similaridade.append({
                        'similaridade': similaridade,
                        'tipo': 'Fornecedor',
                        'dados': {
                            'id': fornecedor.id,
                            'razao_social': fornecedor.razao_social,
                            'fantasia': fornecedor.fantasia,
                            'cnpj': fornecedor.cnpj,
                        }
                    })
        except Exception as e:
            print(f"Erro ao buscar fornecedores (embeddings): {str(e)}")
        
        # Buscar contas a pagar
        try:
            contas_pagar = ContaPagar.objects.filter(ativo=True).select_related('fornecedor').prefetch_related('parcelas')[:50]
            for conta in contas_pagar:
                texto = f"{conta.numero_nota_fiscal} {conta.descricao_produtos} {conta.fornecedor.razao_social} conta pagar pagamento despesa"
                texto_embedding = self._gerar_embedding(texto)
                if texto_embedding:
                    similaridade = self._calcular_similaridade(query_embedding, texto_embedding)
                    parcelas_info = [{'numero': p.numero_parcela, 'valor': float(p.valor), 'vencimento': str(p.data_vencimento), 'status': p.status} for p in conta.parcelas.all()[:3]]
                    dados = {
                        'id': conta.id,
                        'numero_nota_fiscal': conta.numero_nota_fiscal,
                        'fornecedor': conta.fornecedor.razao_social,
                        'valor_total': float(conta.valor_total),
                        'status': conta.status,
                        'quantidade_parcelas': conta.quantidade_parcelas,
                    }
                    if parcelas_info:
                        dados['parcelas'] = parcelas_info
                    resultados_com_similaridade.append({
                        'similaridade': similaridade,
                        'tipo': 'Conta a Pagar',
                        'dados': dados
                    })
        except Exception as e:
            print(f"Erro ao buscar contas a pagar (embeddings): {str(e)}")
        
        # Buscar contas a receber
        try:
            contas_receber = ContaReceber.objects.filter(ativo=True).select_related('cliente').prefetch_related('parcelas')[:50]
            for conta in contas_receber:
                texto = f"{conta.numero_documento} {conta.descricao} {conta.cliente.nome} conta receber recebimento"
                texto_embedding = self._gerar_embedding(texto)
                if texto_embedding:
                    similaridade = self._calcular_similaridade(query_embedding, texto_embedding)
                    parcelas_info = [{'numero': p.numero_parcela, 'valor': float(p.valor), 'vencimento': str(p.data_vencimento), 'status': p.status} for p in conta.parcelas.all()[:3]]
                    dados = {
                        'id': conta.id,
                        'numero_documento': conta.numero_documento,
                        'cliente': conta.cliente.nome,
                        'valor_total': float(conta.valor_total),
                        'status': conta.status,
                        'quantidade_parcelas': conta.quantidade_parcelas,
                    }
                    if parcelas_info:
                        dados['parcelas'] = parcelas_info
                    resultados_com_similaridade.append({
                        'similaridade': similaridade,
                        'tipo': 'Conta a Receber',
                        'dados': dados
                    })
        except Exception as e:
            print(f"Erro ao buscar contas a receber (embeddings): {str(e)}")
        
        # Buscar parcelas diretamente
        try:
            parcelas = Parcela.objects.filter(ativo=True).order_by('-data_vencimento')[:50]
            for parcela in parcelas:
                texto = f"parcela {parcela.numero_parcela} vencimento {parcela.data_vencimento} valor {parcela.valor} status {parcela.status} pagamento"
                texto_embedding = self._gerar_embedding(texto)
                if texto_embedding:
                    similaridade = self._calcular_similaridade(query_embedding, texto_embedding)
                    resultados_com_similaridade.append({
                        'similaridade': similaridade,
                        'tipo': 'Parcela',
                        'dados': {
                            'id': parcela.id,
                            'numero_parcela': parcela.numero_parcela,
                            'valor': float(parcela.valor),
                            'valor_pago': float(parcela.valor_pago),
                            'data_vencimento': str(parcela.data_vencimento),
                            'data_pagamento': str(parcela.data_pagamento) if parcela.data_pagamento else None,
                            'status': parcela.status,
                        }
                    })
        except Exception as e:
            print(f"Erro ao buscar parcelas (embeddings): {str(e)}")
        
        # Buscar faturados
        try:
            faturados = Faturado.objects.filter(ativo=True)[:50]
            for faturado in faturados:
                texto = f"faturado {faturado.nome_completo} {faturado.cpf} pessoa física"
                texto_embedding = self._gerar_embedding(texto)
                if texto_embedding:
                    similaridade = self._calcular_similaridade(query_embedding, texto_embedding)
                    resultados_com_similaridade.append({
                        'similaridade': similaridade,
                        'tipo': 'Faturado',
                        'dados': {
                            'id': faturado.id,
                            'nome_completo': faturado.nome_completo,
                            'cpf': faturado.cpf,
                        }
                    })
        except Exception as e:
            print(f"Erro ao buscar faturados (embeddings): {str(e)}")
        
        # Buscar tipos de despesa
        try:
            tipos_despesa = TipoDespesa.objects.filter(ativo=True)[:50]
            for tipo in tipos_despesa:
                texto = f"tipo despesa {tipo.nome} categoria {tipo.get_categoria_display()} classificação"
                texto_embedding = self._gerar_embedding(texto)
                if texto_embedding:
                    similaridade = self._calcular_similaridade(query_embedding, texto_embedding)
                    resultados_com_similaridade.append({
                        'similaridade': similaridade,
                        'tipo': 'Tipo de Despesa',
                        'dados': {
                            'id': tipo.id,
                            'nome': tipo.nome,
                            'categoria': tipo.get_categoria_display(),
                        }
                    })
        except Exception as e:
            print(f"Erro ao buscar tipos de despesa (embeddings): {str(e)}")
        
        # Buscar tipos de receita
        try:
            tipos_receita = TipoReceita.objects.filter(ativo=True)[:50]
            for tipo in tipos_receita:
                texto = f"tipo receita {tipo.nome} classificação"
                texto_embedding = self._gerar_embedding(texto)
                if texto_embedding:
                    similaridade = self._calcular_similaridade(query_embedding, texto_embedding)
                    resultados_com_similaridade.append({
                        'similaridade': similaridade,
                        'tipo': 'Tipo de Receita',
                        'dados': {
                            'id': tipo.id,
                            'nome': tipo.nome,
                        }
                    })
        except Exception as e:
            print(f"Erro ao buscar tipos de receita (embeddings): {str(e)}")
        
        # Buscar processamentos PDF
        try:
            processamentos = ProcessamentoPDF.objects.filter(ativo=True).order_by('-criado_em')[:50]
            for proc in processamentos:
                texto = f"pdf processado {proc.nome_arquivo} status {proc.get_status_processamento_display()} nota fiscal boleto"
                texto_embedding = self._gerar_embedding(texto)
                if texto_embedding:
                    similaridade = self._calcular_similaridade(query_embedding, texto_embedding)
                    resultados_com_similaridade.append({
                        'similaridade': similaridade,
                        'tipo': 'Processamento PDF',
                        'dados': {
                            'id': proc.id,
                            'nome_arquivo': proc.nome_arquivo,
                            'status': proc.get_status_processamento_display(),
                        }
                    })
        except Exception as e:
            print(f"Erro ao buscar processamentos PDF (embeddings): {str(e)}")
        
        # Ordenar por similaridade e retornar os melhores
        resultados_com_similaridade.sort(key=lambda x: x['similaridade'], reverse=True)
        
        # Obter contexto do sistema
        contexto_sistema = RAGSimpleService()._get_contexto_sistema()
        
        # Formatar contexto
        contexto = contexto_sistema + "\n=== DADOS ENCONTRADOS NO BANCO DE DADOS (ordenados por relevância semântica) ===\n\n"
        resultados_relevantes = [r for r in resultados_com_similaridade if r['similaridade'] > 0.3]
        
        if resultados_relevantes:
            for i, item in enumerate(resultados_relevantes[:limite], 1):
                contexto += f"{i}. {item['tipo']} (similaridade: {item['similaridade']:.2f}):\n"
                for chave, valor in item['dados'].items():
                    if isinstance(valor, list):
                        contexto += f"   - {chave}:\n"
                        for subitem in valor:
                            contexto += f"     * {subitem}\n"
                    else:
                        contexto += f"   - {chave}: {valor}\n"
                contexto += "\n"
        else:
            contexto += "Nenhum resultado relevante encontrado no banco de dados para a consulta.\n"
        
        return contexto
    
    def processar_consulta(self, pergunta: str) -> Dict[str, Any]:
        """
        Processa uma consulta usando RAG com embeddings
        """
        inicio = time.time()
        
        try:
            # 1. Buscar contexto usando embeddings
            contexto = self._buscar_semanticamente(pergunta)
            
            # 2. Criar prompt para o LLM
            prompt = f"""Você é um assistente especializado em análise de dados financeiros e administrativos de um sistema agrícola.

{contexto}

Pergunta do usuário: {pergunta}

INSTRUÇÕES PARA RESPOSTA:
1. Use o contexto do sistema fornecido acima para entender a estrutura e funcionamento
2. Analise os dados encontrados no banco de dados (ordenados por relevância semântica)
3. Se a pergunta for sobre quantidade, calcule e apresente números exatos
4. Se a pergunta for sobre valores, apresente totais e detalhes quando relevante
5. Se a pergunta for sobre status ou classificações, explique claramente
6. Se não houver dados suficientes, explique o que seria necessário e o que foi encontrado
7. Sempre mencione as fontes dos dados (tabelas/entidades) quando relevante
8. Seja claro, detalhado e útil na resposta

Resposta:"""
            
            # 3. Gerar resposta com LLM
            resposta = self.gemini_service.generate_response(prompt)
            
            tempo_resposta = time.time() - inicio
            
            return {
                'success': True,
                'resposta': resposta,
                'contexto': contexto,
                'tempo_resposta': tempo_resposta,
                'tipo_rag': 'EMBEDDINGS'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'tempo_resposta': time.time() - inicio,
                'tipo_rag': 'EMBEDDINGS'
            }

