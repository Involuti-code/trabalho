# -*- coding: utf-8 -*-
"""
Serviço de processamento de PDF com IA
"""

import os
import json
import base64
from typing import Dict, Any, Optional
import PyPDF2
import pdfplumber
import google.generativeai as genai
from decouple import config
from django.conf import settings


class PDFProcessor:
    """
    Classe para processamento de PDFs com extração de dados usando IA
    """
    
    def __init__(self):
        """Inicializa o processador de PDF"""
        self.api_key = config('GEMINI_API_KEY', default='')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """
        Extrai texto do PDF usando pdfplumber
        """
        try:
            text = ""
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")
    
    def process_pdf_with_ai(self, pdf_text: str) -> Dict[str, Any]:
        """
        Processa o texto do PDF usando Google Gemini AI
        """
        if not self.model:
            raise Exception("API key do Gemini não configurada")
        
        try:
            prompt = """
            Você é um especialista em extrair dados de notas fiscais. 
            Analise o texto da nota fiscal abaixo e extraia as seguintes informações em formato JSON:

            {
                "numero": "número da nota fiscal",
                "serie": "série da nota fiscal",
                "dataEmissao": "data de emissão (formato YYYY-MM-DD)",
                "fornecedor": {
                    "nome": "nome/razão social do fornecedor",
                    "cnpj": "CNPJ do fornecedor",
                    "endereco": "endereço completo do fornecedor"
                },
                "cliente": {
                    "nome": "nome/razão social do cliente",
                    "cnpj": "CNPJ do cliente",
                    "endereco": "endereço completo do cliente"
                },
                "itens": [
                    {
                        "descricao": "descrição do produto/serviço",
                        "quantidade": "quantidade (número)",
                        "valorUnitario": "valor unitário (número)",
                        "valorTotal": "valor total do item (número)"
                    }
                ],
                "totais": {
                    "subtotal": "subtotal (número)",
                    "impostos": "total de impostos (número)",
                    "total": "valor total da nota (número)"
                }
            }

            IMPORTANTE:
            - Retorne APENAS o JSON válido, sem texto adicional
            - Use números para valores monetários (sem R$, vírgulas ou pontos)
            - Se alguma informação não estiver disponível, use null
            - Mantenha a estrutura exata do JSON

            Texto da nota fiscal:
            """
            
            full_prompt = prompt + "\n\n" + pdf_text
            
            response = self.model.generate_content(full_prompt)
            
            # Extrair JSON da resposta
            response_text = response.text.strip()
            
            # Limpar a resposta para extrair apenas o JSON
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            # Parse do JSON
            try:
                extracted_data = json.loads(response_text)
                return extracted_data
            except json.JSONDecodeError:
                # Tentar extrair JSON da resposta
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    extracted_data = json.loads(json_match.group())
                    return extracted_data
                else:
                    raise Exception("Não foi possível extrair JSON válido da resposta da IA")
                    
        except Exception as e:
            raise Exception(f"Erro ao processar PDF com IA: {str(e)}")
    
    def process_pdf_file(self, pdf_file) -> Dict[str, Any]:
        """
        Processa um arquivo PDF completo
        """
        try:
            # Extrair texto do PDF
            pdf_text = self.extract_text_from_pdf(pdf_file)
            
            if not pdf_text.strip():
                raise Exception("Não foi possível extrair texto do PDF")
            
            # Processar com IA
            extracted_data = self.process_pdf_with_ai(pdf_text)
            
            return {
                'success': True,
                'data': extracted_data,
                'text_extracted': pdf_text[:500] + "..." if len(pdf_text) > 500 else pdf_text
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'data': None
            }
    
    def validate_pdf_file(self, pdf_file) -> Dict[str, Any]:
        """
        Valida se o arquivo PDF é válido
        """
        try:
            # Verificar extensão
            if not pdf_file.name.lower().endswith('.pdf'):
                return {'valid': False, 'error': 'Apenas arquivos PDF são permitidos'}
            
            # Verificar tamanho (16MB)
            if pdf_file.size > 16 * 1024 * 1024:
                return {'valid': False, 'error': 'Arquivo muito grande. Máximo 16MB'}
            
            # Verificar se é um PDF válido
            try:
                pdf_file.seek(0)
                PyPDF2.PdfReader(pdf_file)
                pdf_file.seek(0)
            except Exception:
                return {'valid': False, 'error': 'Arquivo PDF inválido ou corrompido'}
            
            return {'valid': True, 'error': None}
            
        except Exception as e:
            return {'valid': False, 'error': f'Erro na validação: {str(e)}'}


