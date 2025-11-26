# -*- coding: utf-8 -*-
"""
Serviço para integração com Google Gemini AI
"""

import json
import re
import requests
from pypdf import PdfReader
from typing import Dict, Any, Optional


class GeminiAIService:
    """
    Serviço para integração com Google Gemini AI
    """
    
    def __init__(self):
        import os
        from decouple import config
        self.api_key = config('GEMINI_API_KEY', default=os.environ.get('GEMINI_API_KEY', ''))
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    def extract_text_from_pdf_simple(self, pdf_file) -> str:
        """
        Extrai texto real do PDF usando pypdf
        """
        try:
            # Resetar posição do arquivo
            pdf_file.seek(0)
            
            # Ler o PDF com pypdf
            reader = PdfReader(pdf_file)
            
            text = ""
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Página {page_num + 1} ---\n"
                        text += page_text
                        text += "\n"
                except Exception as e:
                    print(f"Erro ao extrair texto da página {page_num + 1}: {str(e)}")
                    continue
            
            # Se não conseguiu extrair texto
            if not text.strip():
                print("Não foi possível extrair texto do PDF")
                return ""
            
            print(f"Texto extraído do PDF ({len(text)} caracteres):")
            print(text[:500] + "..." if len(text) > 500 else text)
            
            return text
            
        except Exception as e:
            print(f"Erro ao extrair texto do PDF: {str(e)}")
            # Se falhar, retornar texto vazio
            return ""
    
    def process_with_gemini(self, text: str) -> Dict[str, Any]:
        """
        Processa o texto com Google Gemini AI
        """
        try:
            prompt = """
            Você é um especialista em extrair dados de notas fiscais brasileiras e classificar despesas agrícolas. 

            INSTRUÇÕES CRÍTICAS:
            1. Analise APENAS o texto fornecido abaixo
            2. NÃO use informações de exemplo ou dados fictícios
            3. Extraia APENAS os dados que estão realmente no texto
            4. Se um valor não estiver no texto, use null
            5. Classifique automaticamente as despesas conforme as categorias fornecidas
            6. Retorne APENAS o JSON válido, sem texto adicional

            Formato JSON esperado:
            {
                "numero": "número da nota fiscal (se encontrado)",
                "serie": "série da nota fiscal (se encontrada)", 
                "dataEmissao": "data de emissão no formato YYYY-MM-DD (se encontrada)",
                "fornecedor": {
                    "nome": "nome da empresa fornecedora (se encontrado)",
                    "cnpj": "CNPJ do fornecedor (se encontrado)",
                    "endereco": "endereço completo do fornecedor (se encontrado)"
                },
                "cliente": {
                    "nome": "nome da empresa cliente (se encontrado)",
                    "cnpj": "CNPJ do cliente (se encontrado)", 
                    "endereco": "endereço completo do cliente (se encontrado)"
                },
                "itens": [
                    {
                        "descricao": "descrição do produto/serviço (se encontrada)",
                        "quantidade": número_da_quantidade (se encontrada),
                        "valorUnitario": valor_unitário_numerico (se encontrado),
                        "valorTotal": valor_total_numerico (se encontrado),
                        "categoria": "categoria da despesa (classificada automaticamente)"
                    }
                ],
                "totais": {
                    "subtotal": valor_subtotal_numerico (se encontrado),
                    "impostos": valor_impostos_numerico (se encontrado),
                    "total": valor_total_numerico (se encontrado)
                },
                "classificacao_geral": "categoria principal da nota fiscal (baseada nos itens)"
            }

            CATEGORIAS DE DESPESAS AGRÍCOLAS:
            Analise a descrição dos produtos/serviços e classifique automaticamente em uma das seguintes categorias:

            INSUMOS AGRÍCOLAS:
            - Sementes, Fertilizantes, Defensivos Agrícolas, Corretivos

            MANUTENÇÃO E OPERAÇÃO:
            - Combustíveis e Lubrificantes (Óleo Diesel, Gasolina, Óleo de Motor)
            - Peças, Parafusos, Componentes Mecânicos
            - Manutenção de Máquinas e Equipamentos
            - Pneus, Filtros, Correias
            - Ferramentas e Utensílios (Chaves de Fenda, Alicates, Martelos, Kits de Ferramentas)
            - Equipamentos de Manutenção (Multímetros, Ferramentas Elétricas, Kits de Reparo)

            RECURSOS HUMANOS:
            - Mão de Obra Temporária
            - Salários e Encargos

            SERVIÇOS OPERACIONAIS:
            - Frete e Transporte
            - Colheita Terceirizada
            - Secagem e Armazenagem
            - Pulverização e Aplicação

            INFRAESTRUTURA E UTILIDADES:
            - Energia Elétrica
            - Arrendamento de Terras
            - Construções e Reformas
            - Materiais de Construção
            - Material Hidráulico

            ADMINISTRATIVAS:
            - Honorários (Contábeis, Advocatícios, Agronômicos)
            - Despesas Bancárias e Financeiras

            SEGUROS E PROTEÇÃO:
            - Seguro Agrícola
            - Seguro de Ativos (Máquinas/Veículos)
            - Seguro Prestamista

            IMPOSTOS E TAXAS:
            - ITR, IPTU, IPVA, INCRA-CCIR

            INVESTIMENTOS:
            - Aquisição de Máquinas e Implementos
            - Aquisição de Veículos
            - Aquisição de Imóveis
            - Infraestrutura Rural

            OUTROS:
            - Para produtos/serviços que não se encaixam nas categorias acima

            REGRAS DE CLASSIFICAÇÃO:
            - Analise a descrição do produto/serviço
            - Classifique baseado no tipo de produto e uso agrícola
            - Se for um livro, revista, material de escritório, etc., classifique como "OUTROS"
            - Se for combustível, classifique como "MANUTENÇÃO E OPERAÇÃO"
            - Se for material de construção, classifique como "INFRAESTRUTURA E UTILIDADES"
            - Se for semente, fertilizante, defensivo, classifique como "INSUMOS AGRÍCOLAS"
            - Se for FERRAMENTA (chave de fenda, alicate, martelo, kit de ferramentas, multímetro), classifique como "MANUTENÇÃO E OPERAÇÃO"
            - Se for EQUIPAMENTO DE MANUTENÇÃO (ferramentas elétricas, kits de reparo, equipamentos de medição), classifique como "MANUTENÇÃO E OPERAÇÃO"
            - Se for PEÇA ou COMPONENTE MECÂNICO, classifique como "MANUTENÇÃO E OPERAÇÃO"

            REGRAS IMPORTANTES:
            - Use números decimais para valores monetários (ex: 25.50)
            - Para datas, use formato YYYY-MM-DD
            - Para CNPJ, mantenha a formatação com pontos e barras
            - Se não encontrar um campo, use null
            - NÃO invente dados que não estão no texto
            - Classifique TODOS os itens em uma categoria apropriada

            TEXTO DA NOTA FISCAL PARA ANÁLISE:
            """
            
            full_prompt = prompt + "\n" + text
            
            # Preparar dados para a API
            data = {
                "contents": [{
                    "parts": [{
                        "text": full_prompt
                    }]
                }]
            }
            
            # Fazer requisição para a API do Gemini
            headers = {
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            
            print(f"Fazendo requisição para: {url}")
            print(f"Dados: {data}")
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            print(f"Status da resposta: {response.status_code}")
            print(f"Resposta: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                
                # Extrair texto da resposta
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        response_text = candidate['content']['parts'][0]['text']
                        
                        print(f"Texto da IA: {response_text}")
                        
                        # Limpar a resposta para extrair apenas o JSON
                        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(0)
                            return json.loads(json_str)
                        else:
                            # Tentar parsear a resposta inteira como JSON
                            return json.loads(response_text)
                
                raise Exception("Resposta da IA não contém dados válidos")
            else:
                raise Exception(f"Erro na API do Gemini: {response.status_code} - {response.text}")
                
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao processar resposta da IA: {str(e)}")
        except requests.RequestException as e:
            raise Exception(f"Erro na comunicação com IA: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro geral na IA: {str(e)}")
    
    def process_pdf_with_ai(self, pdf_file) -> Dict[str, Any]:
        """
        Processa um PDF completo usando IA
        """
        try:
            # Extrair texto do PDF
            text = self.extract_text_from_pdf_simple(pdf_file)
            
            if not text.strip():
                return {
                    'success': False,
                    'error': "Não foi possível extrair texto do PDF. O arquivo pode estar corrompido ou ser uma imagem.",
                    'data': None
                }
            
            print(f"Texto extraído para processamento: {len(text)} caracteres")
            
            # Processar com IA
            extracted_data = self.process_with_gemini(text)
            
            return {
                'success': True,
                'data': extracted_data,
                'raw_text': text[:500] + "..." if len(text) > 500 else text,
                'message': 'Dados extraídos com sucesso usando Google Gemini AI!'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'data': None
            }
