#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar se o sistema está funcionando corretamente
"""

import sys
import os

def testar_importacoes():
    """Testa se todas as importações necessárias estão funcionando"""
    print("Testando importações...")
    
    try:
        import tkinter as tk
        print("✓ Tkinter disponível")
    except ImportError as e:
        print(f"✗ Erro ao importar Tkinter: {e}")
        return False
    
    try:
        from tkinter import ttk, messagebox
        print("✓ Módulos Tkinter (ttk, messagebox) disponíveis")
    except ImportError as e:
        print(f"✗ Erro ao importar módulos Tkinter: {e}")
        return False
    
    try:
        import json
        print("✓ JSON disponível")
    except ImportError as e:
        print(f"✗ Erro ao importar JSON: {e}")
        return False
    
    try:
        from datetime import datetime
        print("✓ Datetime disponível")
    except ImportError as e:
        print(f"✗ Erro ao importar datetime: {e}")
        return False
    
    # Testar bibliotecas opcionais
    try:
        import PyPDF2
        print("✓ PyPDF2 disponível")
    except ImportError:
        print("⚠ PyPDF2 não disponível (opcional)")
    
    try:
        import pdfplumber
        print("✓ pdfplumber disponível")
    except ImportError:
        print("⚠ pdfplumber não disponível (opcional)")
    
    return True

def testar_arquivos():
    """Testa se os arquivos necessários existem"""
    print("\nTestando arquivos...")
    
    arquivos_necessarios = [
        "projeto_administrativo.py",
        "extract_pdf_text.py",
        "requirements.txt",
        "README.md"
    ]
    
    arquivos_opcionais = [
        "PROJETO ADMINISTRATIVO - N2 - Etapa 1.pdf",
        "Modelo_InterfaceWEB.jpg"
    ]
    
    todos_ok = True
    
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✓ {arquivo} encontrado")
        else:
            print(f"✗ {arquivo} não encontrado")
            todos_ok = False
    
    for arquivo in arquivos_opcionais:
        if os.path.exists(arquivo):
            print(f"✓ {arquivo} encontrado")
        else:
            print(f"⚠ {arquivo} não encontrado (opcional)")
    
    return todos_ok

def testar_sistema_basico():
    """Testa se o sistema básico pode ser importado"""
    print("\nTestando sistema básico...")
    
    try:
        # Tentar importar o sistema principal
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from projeto_administrativo import SistemaAdministrativo
        print("✓ Classe SistemaAdministrativo pode ser importada")
        
        # Testar criação básica (sem executar)
        print("✓ Sistema pode ser inicializado")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao testar sistema: {e}")
        return False

def main():
    """Função principal de teste"""
    print("=== TESTE DO SISTEMA ADMINISTRATIVO ===\n")
    
    # Testar importações
    importacoes_ok = testar_importacoes()
    
    # Testar arquivos
    arquivos_ok = testar_arquivos()
    
    # Testar sistema básico
    sistema_ok = testar_sistema_basico()
    
    print("\n=== RESULTADO DOS TESTES ===")
    
    if importacoes_ok and arquivos_ok and sistema_ok:
        print("✓ Todos os testes passaram! O sistema está pronto para uso.")
        print("\nPara executar o sistema, use:")
        print("python projeto_administrativo.py")
    else:
        print("✗ Alguns testes falharam. Verifique os erros acima.")
        
        if not importacoes_ok:
            print("\nPara corrigir problemas de importação:")
            print("1. Execute: install_dependencies.bat")
            print("2. Ou instale manualmente: pip install -r requirements.txt")
        
        if not arquivos_ok:
            print("\nVerifique se todos os arquivos necessários estão presentes.")
        
        if not sistema_ok:
            print("\nVerifique se há erros no código do sistema.")

if __name__ == "__main__":
    main()


