# -*- coding: utf-8 -*-
"""
Serviços para processamento de PDF com IA
"""

import json
import re
from typing import Dict, Any, Optional
from django.conf import settings
from .gemini_service import GeminiAIService


class PDFProcessorService:
    """
    Serviço para processamento de PDFs com IA
    """
    
    def __init__(self):
        # Por enquanto, vamos usar processamento local
        # A integração com Google Gemini será adicionada depois
        pass
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """
        Simula extração de texto do PDF
        Por enquanto, retorna um texto de exemplo
        """
        try:
            # Texto simulado de uma nota fiscal
            sample_text = """
            NOTA FISCAL ELETRÔNICA
            Número: 000123456
            Série: 001
            Data de Emissão: 15/01/2024
            
            EMISSOR:
            EMPRESA FORNECEDORA LTDA
            CNPJ: 12.345.678/0001-90
            Endereço: Rua das Empresas, 123 - São Paulo, SP
            
            DESTINATÁRIO:
            CLIENTE EXEMPLO S.A.
            CNPJ: 98.765.432/0001-10
            Endereço: Av. dos Clientes, 456 - Rio de Janeiro, RJ
            
            ITENS:
            Produto A - Qtd: 10 - Valor Unit: R$ 25,50 - Total: R$ 255,00
            Produto B - Qtd: 5 - Valor Unit: R$ 15,75 - Total: R$ 78,75
            
            TOTAIS:
            Subtotal: R$ 333,75
            Impostos: R$ 66,75
            Total: R$ 400,50
            """
            return sample_text
        except Exception as e:
            raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")
    
    def extract_data_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extrai dados estruturados do texto usando regex e análise local
        """
        try:
            # Padrões para extrair informações
            patterns = {
                'numero': r'(?:N[ºo°]|Número|NF|Nota Fiscal)[\s:]*(\d+)',
                'serie': r'(?:Série|Serie)[\s:]*(\d+)',
                'data': r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                'cnpj': r'(\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})',
                'valor': r'R\$\s*(\d+[.,]\d{2})',
            }
            
            extracted = {}
            
            # Extrair número da nota
            numero_match = re.search(patterns['numero'], text, re.IGNORECASE)
            if numero_match:
                extracted['numero'] = numero_match.group(1)
            else:
                extracted['numero'] = "000123456"  # Valor padrão
            
            # Extrair série
            serie_match = re.search(patterns['serie'], text, re.IGNORECASE)
            if serie_match:
                extracted['serie'] = serie_match.group(1)
            else:
                extracted['serie'] = "001"  # Valor padrão
            
            # Extrair data
            data_match = re.search(patterns['data'], text)
            if data_match:
                extracted['dataEmissao'] = data_match.group(1)
            else:
                extracted['dataEmissao'] = "2024-01-15"  # Valor padrão
            
            # Extrair CNPJs
            cnpj_matches = re.findall(patterns['cnpj'], text)
            if len(cnpj_matches) >= 2:
                extracted['fornecedor_cnpj'] = cnpj_matches[0]
                extracted['cliente_cnpj'] = cnpj_matches[1]
            else:
                extracted['fornecedor_cnpj'] = "12.345.678/0001-90"
                extracted['cliente_cnpj'] = "98.765.432/0001-10"
            
            # Extrair valores
            valor_matches = re.findall(patterns['valor'], text)
            if valor_matches:
                # Converter vírgula para ponto
                valores = [float(v.replace(',', '.')) for v in valor_matches]
                extracted['valores'] = valores
            else:
                extracted['valores'] = [400.50, 333.75, 66.75]
            
            return extracted
            
        except Exception as e:
            raise Exception(f"Erro ao extrair dados do texto: {str(e)}")
    
    def create_structured_data(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria estrutura JSON a partir dos dados extraídos
        """
        try:
            # Dados estruturados baseados no que foi extraído
            structured_data = {
                "numero": extracted_data.get('numero', '000123456'),
                "serie": extracted_data.get('serie', '001'),
                "dataEmissao": extracted_data.get('dataEmissao', '2024-01-15'),
                "fornecedor": {
                    "nome": "EMPRESA FORNECEDORA LTDA",
                    "cnpj": extracted_data.get('fornecedor_cnpj', '12.345.678/0001-90'),
                    "endereco": "Rua das Empresas, 123 - São Paulo, SP"
                },
                "cliente": {
                    "nome": "CLIENTE EXEMPLO S.A.",
                    "cnpj": extracted_data.get('cliente_cnpj', '98.765.432/0001-10'),
                    "endereco": "Av. dos Clientes, 456 - Rio de Janeiro, RJ"
                },
                "itens": [
                    {
                        "descricao": "Produto A",
                        "quantidade": 10,
                        "valorUnitario": 25.50,
                        "valorTotal": 255.00
                    },
                    {
                        "descricao": "Produto B",
                        "quantidade": 5,
                        "valorUnitario": 15.75,
                        "valorTotal": 78.75
                    }
                ],
                "totais": {
                    "subtotal": 333.75,
                    "impostos": 66.75,
                    "total": 400.50
                }
            }
            
            # Se encontrou valores reais, usar eles
            if 'valores' in extracted_data and len(extracted_data['valores']) >= 3:
                valores = extracted_data['valores']
                structured_data['totais']['total'] = max(valores)
                structured_data['totais']['subtotal'] = max(valores) * 0.83
                structured_data['totais']['impostos'] = max(valores) * 0.17
            
            return structured_data
            
        except Exception as e:
            raise Exception(f"Erro ao criar dados estruturados: {str(e)}")
    
    def process_pdf(self, pdf_file) -> Dict[str, Any]:
        """
        Processa um PDF completo usando APENAS IA (Google Gemini)
        """
        try:
            # Usar APENAS IA - sem fallback
            gemini_service = GeminiAIService()
            ai_result = gemini_service.process_pdf_with_ai(pdf_file)
            
            if ai_result['success']:
                return ai_result
            else:
                # Se IA falhar, retornar erro (sem fallback)
                return {
                    'success': False,
                    'error': f"Erro na IA: {ai_result['error']}",
                    'data': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Erro no processamento: {str(e)}",
                'data': None
            }