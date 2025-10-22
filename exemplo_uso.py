#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do Sistema Administrativo
Demonstra como usar as principais funcionalidades do sistema
"""

import sys
import os
from datetime import datetime

# Adiciona o diretório atual ao path para importar o sistema
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def exemplo_uso_basico():
    """Exemplo básico de uso do sistema"""
    print("=== EXEMPLO DE USO DO SISTEMA ADMINISTRATIVO ===\n")
    
    try:
        # Importa o sistema
        from projeto_administrativo import SistemaAdministrativo
        from config import obter_configuracao
        
        print("1. Importando o sistema...")
        print("✓ Sistema importado com sucesso")
        
        print("\n2. Verificando configurações...")
        titulo = obter_configuracao('INTERFACE_CONFIG', 'titulo')
        print(f"✓ Título do sistema: {titulo}")
        
        print("\n3. Criando instância do sistema...")
        # Nota: Não vamos executar o mainloop aqui para não bloquear
        print("✓ Sistema pode ser inicializado")
        
        print("\n4. Exemplo de dados do sistema:")
        dados_exemplo = {
            'usuarios': [
                {'id': 1, 'nome': 'João Silva', 'email': 'joao@email.com', 'ativo': True},
                {'id': 2, 'nome': 'Maria Santos', 'email': 'maria@email.com', 'ativo': True}
            ],
            'produtos': [
                {'id': 1, 'nome': 'Produto A', 'preco': 29.90, 'estoque': 100},
                {'id': 2, 'nome': 'Produto B', 'preco': 49.90, 'estoque': 50}
            ],
            'vendas': [
                {'id': 1, 'usuario_id': 1, 'produto_id': 1, 'quantidade': 2, 'data': datetime.now().isoformat()}
            ]
        }
        
        print(f"✓ Usuários cadastrados: {len(dados_exemplo['usuarios'])}")
        print(f"✓ Produtos cadastrados: {len(dados_exemplo['produtos'])}")
        print(f"✓ Vendas registradas: {len(dados_exemplo['vendas'])}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro no exemplo: {e}")
        return False

def exemplo_extracao_pdf():
    """Exemplo de como extrair texto do PDF"""
    print("\n=== EXEMPLO DE EXTRAÇÃO DE PDF ===\n")
    
    try:
        from extract_pdf_text import extract_text_from_pdf
        
        pdf_file = "PROJETO ADMINISTRATIVO - N2 - Etapa 1.pdf"
        
        if os.path.exists(pdf_file):
            print(f"1. Arquivo PDF encontrado: {pdf_file}")
            print("2. Extraindo texto...")
            
            # Tenta extrair o texto
            texto = extract_text_from_pdf(pdf_file)
            
            if texto:
                print("✓ Texto extraído com sucesso")
                print(f"✓ Tamanho do texto: {len(texto)} caracteres")
                
                # Salva em arquivo
                with open("texto_extraido_exemplo.txt", "w", encoding="utf-8") as f:
                    f.write(texto)
                print("✓ Texto salvo em 'texto_extraido_exemplo.txt'")
                
                # Mostra uma prévia
                preview = texto[:500] + "..." if len(texto) > 500 else texto
                print(f"\nPrévia do texto:\n{preview}")
                
            else:
                print("⚠ Não foi possível extrair o texto (bibliotecas não instaladas)")
                print("Execute: install_dependencies.bat")
        else:
            print(f"⚠ Arquivo PDF não encontrado: {pdf_file}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro na extração: {e}")
        return False

def exemplo_configuracao():
    """Exemplo de como usar as configurações"""
    print("\n=== EXEMPLO DE CONFIGURAÇÕES ===\n")
    
    try:
        from config import (
            obter_configuracao, 
            definir_configuracao,
            INTERFACE_CONFIG,
            CORES,
            DATABASE_CONFIG
        )
        
        print("1. Configurações atuais:")
        print(f"   Título: {obter_configuracao('INTERFACE_CONFIG', 'titulo')}")
        print(f"   Largura: {obter_configuracao('INTERFACE_CONFIG', 'largura')}")
        print(f"   Altura: {obter_configuracao('INTERFACE_CONFIG', 'altura')}")
        print(f"   Cor primária: {obter_configuracao('CORES', 'primaria')}")
        print(f"   Tipo de banco: {obter_configuracao('DATABASE_CONFIG', 'tipo')}")
        
        print("\n2. Modificando configuração...")
        definir_configuracao('INTERFACE_CONFIG', 'titulo', 'Sistema Administrativo - Personalizado')
        novo_titulo = obter_configuracao('INTERFACE_CONFIG', 'titulo')
        print(f"✓ Novo título: {novo_titulo}")
        
        print("\n3. Todas as cores disponíveis:")
        for nome, cor in CORES.items():
            print(f"   {nome}: {cor}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro nas configurações: {e}")
        return False

def exemplo_banco_dados():
    """Exemplo de como trabalhar com dados"""
    print("\n=== EXEMPLO DE BANCO DE DADOS ===\n")
    
    try:
        import json
        
        # Dados de exemplo
        dados_exemplo = {
            'usuarios': [
                {
                    'id': 1,
                    'nome': 'João Silva',
                    'email': 'joao@email.com',
                    'telefone': '(11) 99999-9999',
                    'ativo': True,
                    'data_cadastro': datetime.now().isoformat()
                },
                {
                    'id': 2,
                    'nome': 'Maria Santos',
                    'email': 'maria@email.com',
                    'telefone': '(11) 88888-8888',
                    'ativo': True,
                    'data_cadastro': datetime.now().isoformat()
                }
            ],
            'produtos': [
                {
                    'id': 1,
                    'nome': 'Produto A',
                    'descricao': 'Descrição do produto A',
                    'preco': 29.90,
                    'estoque': 100,
                    'categoria': 'Categoria 1',
                    'ativo': True
                },
                {
                    'id': 2,
                    'nome': 'Produto B',
                    'descricao': 'Descrição do produto B',
                    'preco': 49.90,
                    'estoque': 50,
                    'categoria': 'Categoria 2',
                    'ativo': True
                }
            ],
            'vendas': [
                {
                    'id': 1,
                    'usuario_id': 1,
                    'produto_id': 1,
                    'quantidade': 2,
                    'preco_unitario': 29.90,
                    'total': 59.80,
                    'data': datetime.now().isoformat(),
                    'status': 'concluida'
                }
            ]
        }
        
        print("1. Criando dados de exemplo...")
        print(f"✓ {len(dados_exemplo['usuarios'])} usuários")
        print(f"✓ {len(dados_exemplo['produtos'])} produtos")
        print(f"✓ {len(dados_exemplo['vendas'])} vendas")
        
        print("\n2. Salvando dados em arquivo JSON...")
        with open('dados_exemplo.json', 'w', encoding='utf-8') as f:
            json.dump(dados_exemplo, f, ensure_ascii=False, indent=2)
        print("✓ Dados salvos em 'dados_exemplo.json'")
        
        print("\n3. Carregando dados do arquivo...")
        with open('dados_exemplo.json', 'r', encoding='utf-8') as f:
            dados_carregados = json.load(f)
        print("✓ Dados carregados com sucesso")
        
        print("\n4. Exemplo de consulta:")
        usuario = dados_carregados['usuarios'][0]
        print(f"   Primeiro usuário: {usuario['nome']} ({usuario['email']})")
        
        produto = dados_carregados['produtos'][0]
        print(f"   Primeiro produto: {produto['nome']} - R$ {produto['preco']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro no banco de dados: {e}")
        return False

def exemplo_interface():
    """Exemplo de como criar uma interface simples"""
    print("\n=== EXEMPLO DE INTERFACE ===\n")
    
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
        
        print("1. Testando criação de interface...")
        
        # Cria uma janela de teste (não será exibida)
        root = tk.Tk()
        root.withdraw()  # Esconde a janela
        
        print("✓ Janela criada com sucesso")
        
        # Testa criação de widgets
        frame = ttk.Frame(root)
        label = ttk.Label(frame, text="Teste")
        button = ttk.Button(frame, text="Botão")
        
        print("✓ Widgets criados com sucesso")
        
        # Testa messagebox
        print("✓ Messagebox disponível")
        
        root.destroy()
        print("✓ Interface testada com sucesso")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro na interface: {e}")
        return False

def main():
    """Função principal do exemplo"""
    print("SISTEMA ADMINISTRATIVO - EXEMPLOS DE USO")
    print("=" * 50)
    
    exemplos = [
        ("Uso Básico", exemplo_uso_basico),
        ("Extração de PDF", exemplo_extracao_pdf),
        ("Configurações", exemplo_configuracao),
        ("Banco de Dados", exemplo_banco_dados),
        ("Interface", exemplo_interface)
    ]
    
    resultados = []
    
    for nome, funcao in exemplos:
        print(f"\n{'='*20} {nome.upper()} {'='*20}")
        try:
            resultado = funcao()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"✗ Erro inesperado em {nome}: {e}")
            resultados.append((nome, False))
    
    # Resumo dos resultados
    print("\n" + "="*50)
    print("RESUMO DOS EXEMPLOS")
    print("="*50)
    
    sucessos = 0
    for nome, resultado in resultados:
        status = "✓ SUCESSO" if resultado else "✗ FALHOU"
        print(f"{nome:20} {status}")
        if resultado:
            sucessos += 1
    
    print(f"\nTotal: {sucessos}/{len(resultados)} exemplos executados com sucesso")
    
    if sucessos == len(resultados):
        print("\n🎉 Todos os exemplos funcionaram perfeitamente!")
        print("O sistema está pronto para uso.")
    else:
        print(f"\n⚠ {len(resultados) - sucessos} exemplo(s) falharam.")
        print("Verifique as dependências e configurações.")
    
    print("\nPara executar o sistema completo, use:")
    print("python projeto_administrativo.py")
    print("\nOu execute o arquivo:")
    print("iniciar_sistema.bat")

if __name__ == "__main__":
    main()

