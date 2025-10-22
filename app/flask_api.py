#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask API para funcionalidades específicas do Sistema Administrativo-Financeiro
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)

# Configurações
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads/pdfs'

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica se a API está funcionando"""
    return jsonify({
        'status': 'ok',
        'message': 'Sistema Administrativo-Financeiro API está funcionando',
        'version': '1.0.0'
    })

@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    """Endpoint para upload de PDFs de notas fiscais"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if file and file.filename.lower().endswith('.pdf'):
            # Aqui será implementada a lógica de processamento
            return jsonify({
                'message': 'Arquivo recebido com sucesso',
                'filename': file.filename,
                'status': 'processing'
            })
        else:
            return jsonify({'error': 'Apenas arquivos PDF são permitidos'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/process-pdf', methods=['POST'])
def process_pdf():
    """Endpoint para processar PDF com Gemini"""
    try:
        data = request.get_json()
        
        if not data or 'pdf_content' not in data:
            return jsonify({'error': 'Conteúdo do PDF não fornecido'}), 400
        
        # Aqui será implementada a integração com Gemini
        # Por enquanto, retorna uma resposta mock
        return jsonify({
            'status': 'success',
            'extracted_data': {
                'fornecedor': {
                    'razao_social': 'Exemplo Ltda',
                    'fantasia': 'Exemplo',
                    'cnpj': '12.345.678/0001-90'
                },
                'faturado': {
                    'nome_completo': 'João Silva',
                    'cpf': '123.456.789-00'
                },
                'nota_fiscal': {
                    'numero': '12345',
                    'data_emissao': '2024-01-15',
                    'descricao_produtos': 'Produto exemplo'
                },
                'parcelas': {
                    'quantidade': 1,
                    'data_vencimento': '2024-02-15',
                    'valor_total': 1000.00
                },
                'classificacao': {
                    'tipo_despesa': 'MANUTENÇÃO E OPERAÇÃO'
                }
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/classify-expense', methods=['POST'])
def classify_expense():
    """Endpoint para classificar despesas automaticamente"""
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({'error': 'Descrição não fornecida'}), 400
        
        description = data['description'].lower()
        
        # Lógica de classificação baseada nas categorias do projeto
        categories = {
            'insumos_agricolas': ['semente', 'fertilizante', 'defensivo', 'corretivo'],
            'manutencao_operacao': ['oleo', 'diesel', 'combustivel', 'peca', 'parafuso', 'manutencao', 'pneu', 'filtro'],
            'recursos_humanos': ['mao de obra', 'salario', 'encargo'],
            'servicos_operacionais': ['frete', 'transporte', 'colheita', 'secagem', 'armazenagem'],
            'infraestrutura_utilidades': ['energia', 'eletrica', 'arrendamento', 'construcao', 'reforma'],
            'administrativas': ['honorario', 'contabil', 'advocaticio', 'agronomico', 'bancario'],
            'seguros_protecao': ['seguro', 'agricola', 'ativo', 'maquina', 'veiculo'],
            'impostos_taxas': ['itr', 'iptu', 'ipva', 'incra', 'ccir'],
            'investimentos': ['maquina', 'implemento', 'veiculo', 'imovel', 'infraestrutura']
        }
        
        classification = 'ADMINISTRATIVAS'  # Default
        
        for category, keywords in categories.items():
            if any(keyword in description for keyword in keywords):
                classification = category.upper().replace('_', ' ')
                break
        
        return jsonify({
            'status': 'success',
            'classification': classification,
            'confidence': 0.85
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Criar diretório de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Executar a aplicação Flask
    app.run(debug=True, host='0.0.0.0', port=5000)


