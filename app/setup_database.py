#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar o banco de dados PostgreSQL
"""

import os
import sys
import subprocess
from pathlib import Path

def check_postgresql():
    """Verifica se o PostgreSQL está instalado"""
    try:
        result = subprocess.run(['psql', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ PostgreSQL encontrado: {result.stdout.strip()}")
            return True
        else:
            print("✗ PostgreSQL não encontrado")
            return False
    except FileNotFoundError:
        print("✗ PostgreSQL não está no PATH")
        return False

def create_database():
    """Cria o banco de dados se não existir"""
    try:
        # Comando para criar o banco de dados
        cmd = [
            'psql', 
            '-U', 'postgres', 
            '-h', 'localhost',
            '-c', 'CREATE DATABASE sistema_admin;'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Banco de dados 'sistema_admin' criado com sucesso")
            return True
        elif "already exists" in result.stderr:
            print("✓ Banco de dados 'sistema_admin' já existe")
            return True
        else:
            print(f"✗ Erro ao criar banco de dados: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Erro ao executar comando: {e}")
        return False

def setup_django_database():
    """Configura o banco de dados do Django"""
    try:
        # Executar migrações
        print("Executando migrações do Django...")
        result = subprocess.run(['python', 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Migrações executadas com sucesso")
            return True
        else:
            print(f"✗ Erro nas migrações: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Erro ao executar migrações: {e}")
        return False

def create_superuser():
    """Cria um superusuário do Django"""
    try:
        print("Criando superusuário...")
        print("Usuário: admin")
        print("Email: admin@sistema.com")
        print("Senha: admin123")
        
        # Comando para criar superusuário
        cmd = [
            'python', 'manage.py', 'createsuperuser',
            '--username', 'admin',
            '--email', 'admin@sistema.com',
            '--noinput'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Superusuário criado com sucesso")
            # Definir senha
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(username='admin')
            user.set_password('admin123')
            user.save()
            print("✓ Senha definida: admin123")
            return True
        else:
            print(f"✗ Erro ao criar superusuário: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Erro ao criar superusuário: {e}")
        return False

def main():
    """Função principal"""
    print("=== CONFIGURAÇÃO DO BANCO DE DADOS ===")
    print()
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('manage.py'):
        print("✗ Arquivo manage.py não encontrado")
        print("Execute este script no diretório raiz do projeto Django")
        return
    
    # Verificar PostgreSQL
    if not check_postgresql():
        print("\nPara instalar o PostgreSQL:")
        print("1. Baixe em: https://www.postgresql.org/download/")
        print("2. Instale com as configurações padrão")
        print("3. Configure a senha do usuário 'postgres'")
        return
    
    print()
    
    # Criar banco de dados
    if not create_database():
        print("\nVerifique se:")
        print("1. PostgreSQL está rodando")
        print("2. Usuário 'postgres' existe")
        print("3. Senha está correta")
        return
    
    print()
    
    # Configurar Django
    if not setup_django_database():
        print("\nVerifique as configurações do banco no settings.py")
        return
    
    print()
    
    # Criar superusuário
    create_superuser()
    
    print()
    print("=== CONFIGURAÇÃO CONCLUÍDA ===")
    print("Banco de dados configurado com sucesso!")
    print()
    print("Para acessar o admin do Django:")
    print("1. Execute: python manage.py runserver")
    print("2. Acesse: http://localhost:8000/admin")
    print("3. Login: admin / admin123")

if __name__ == "__main__":
    main()



