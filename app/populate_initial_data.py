#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para popular o banco de dados com dados iniciais
"""

import os
import sys
import django
from datetime import date, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_admin.settings')
django.setup()

from apps.tipos_despesa.models import TipoDespesa
from apps.tipos_receita.models import TipoReceita
from apps.fornecedores.models import Fornecedor
from apps.clientes.models import Cliente
from apps.faturados.models import Faturado


def criar_tipos_despesa():
    """Cria os tipos de despesa conforme especificação do projeto"""
    print("Criando tipos de despesa...")
    
    tipos_despesa = [
        # INSUMOS AGRÍCOLAS
        {
            'nome': 'Sementes',
            'codigo': 'INS001',
            'categoria': 'INSUMOS_AGRICOLAS',
            'palavras_chave': 'semente, sementes, plantio, cultivar',
            'cor': '#28a745'
        },
        {
            'nome': 'Fertilizantes',
            'codigo': 'INS002',
            'categoria': 'INSUMOS_AGRICOLAS',
            'palavras_chave': 'fertilizante, adubo, nutriente, NPK',
            'cor': '#28a745'
        },
        {
            'nome': 'Defensivos Agrícolas',
            'codigo': 'INS003',
            'categoria': 'INSUMOS_AGRICOLAS',
            'palavras_chave': 'defensivo, agrotóxico, pesticida, herbicida, fungicida',
            'cor': '#28a745'
        },
        
        # MANUTENÇÃO E OPERAÇÃO
        {
            'nome': 'Combustíveis e Lubrificantes',
            'codigo': 'MAN001',
            'categoria': 'MANUTENCAO_OPERACAO',
            'palavras_chave': 'combustível, diesel, gasolina, óleo, lubrificante',
            'cor': '#dc3545'
        },
        {
            'nome': 'Peças e Componentes Mecânicos',
            'codigo': 'MAN002',
            'categoria': 'MANUTENCAO_OPERACAO',
            'palavras_chave': 'peça, parafuso, componente, mecânico, reparo',
            'cor': '#dc3545'
        },
        {
            'nome': 'Manutenção de Máquinas',
            'codigo': 'MAN003',
            'categoria': 'MANUTENCAO_OPERACAO',
            'palavras_chave': 'manutenção, máquina, equipamento, conserto',
            'cor': '#dc3545'
        },
        {
            'nome': 'Pneus e Filtros',
            'codigo': 'MAN004',
            'categoria': 'MANUTENCAO_OPERACAO',
            'palavras_chave': 'pneu, filtro, correia, borracha',
            'cor': '#dc3545'
        },
        
        # RECURSOS HUMANOS
        {
            'nome': 'Mão de Obra Temporária',
            'codigo': 'RH001',
            'categoria': 'RECURSOS_HUMANOS',
            'palavras_chave': 'mão de obra, temporário, funcionário, trabalhador',
            'cor': '#17a2b8'
        },
        {
            'nome': 'Salários e Encargos',
            'codigo': 'RH002',
            'categoria': 'RECURSOS_HUMANOS',
            'palavras_chave': 'salário, encargo, funcionário, empregado',
            'cor': '#17a2b8'
        },
        
        # SERVIÇOS OPERACIONAIS
        {
            'nome': 'Frete e Transporte',
            'codigo': 'SER001',
            'categoria': 'SERVICOS_OPERACIONAIS',
            'palavras_chave': 'frete, transporte, entrega, logística',
            'cor': '#ffc107'
        },
        {
            'nome': 'Colheita Terceirizada',
            'codigo': 'SER002',
            'categoria': 'SERVICOS_OPERACIONAIS',
            'palavras_chave': 'colheita, terceirizado, colheita',
            'cor': '#ffc107'
        },
        
        # INFRAESTRUTURA E UTILIDADES
        {
            'nome': 'Energia Elétrica',
            'codigo': 'INF001',
            'categoria': 'INFRAESTRUTURA_UTILIDADES',
            'palavras_chave': 'energia, elétrica, luz, eletricidade',
            'cor': '#6f42c1'
        },
        {
            'nome': 'Arrendamento de Terras',
            'codigo': 'INF002',
            'categoria': 'INFRAESTRUTURA_UTILIDADES',
            'palavras_chave': 'arrendamento, terra, propriedade, aluguel',
            'cor': '#6f42c1'
        },
        {
            'nome': 'Construções e Reformas',
            'codigo': 'INF003',
            'categoria': 'INFRAESTRUTURA_UTILIDADES',
            'palavras_chave': 'construção, reforma, obra, material hidráulico',
            'cor': '#6f42c1'
        },
        
        # ADMINISTRATIVAS
        {
            'nome': 'Honorários Contábeis',
            'codigo': 'ADM001',
            'categoria': 'ADMINISTRATIVAS',
            'palavras_chave': 'honorário, contábil, contador, escrituração',
            'cor': '#6c757d'
        },
        {
            'nome': 'Despesas Bancárias',
            'codigo': 'ADM002',
            'categoria': 'ADMINISTRATIVAS',
            'palavras_chave': 'bancário, banco, tarifa, taxa',
            'cor': '#6c757d'
        },
        
        # SEGUROS E PROTEÇÃO
        {
            'nome': 'Seguro Agrícola',
            'codigo': 'SEG001',
            'categoria': 'SEGUROS_PROTECAO',
            'palavras_chave': 'seguro, agrícola, proteção, cobertura',
            'cor': '#fd7e14'
        },
        
        # IMPOSTOS E TAXAS
        {
            'nome': 'ITR',
            'codigo': 'IMP001',
            'categoria': 'IMPOSTOS_TAXAS',
            'palavras_chave': 'ITR, imposto, rural, territorial',
            'cor': '#e83e8c'
        },
        {
            'nome': 'IPTU',
            'codigo': 'IMP002',
            'categoria': 'IMPOSTOS_TAXAS',
            'palavras_chave': 'IPTU, imposto, predial, territorial',
            'cor': '#e83e8c'
        },
        
        # INVESTIMENTOS
        {
            'nome': 'Aquisição de Máquinas',
            'codigo': 'INV001',
            'categoria': 'INVESTIMENTOS',
            'palavras_chave': 'máquina, implemento, aquisição, compra',
            'cor': '#20c997'
        },
        {
            'nome': 'Aquisição de Veículos',
            'codigo': 'INV002',
            'categoria': 'INVESTIMENTOS',
            'palavras_chave': 'veículo, carro, caminhão, trator',
            'cor': '#20c997'
        },
    ]
    
    for tipo_data in tipos_despesa:
        tipo, created = TipoDespesa.objects.get_or_create(
            codigo=tipo_data['codigo'],
            defaults=tipo_data
        )
        if created:
            print(f"  ✓ Criado: {tipo.nome}")
        else:
            print(f"  - Já existe: {tipo.nome}")


def criar_tipos_receita():
    """Cria tipos de receita básicos"""
    print("Criando tipos de receita...")
    
    tipos_receita = [
        {
            'nome': 'Venda de Produtos Agrícolas',
            'codigo': 'REC001',
            'descricao': 'Receita com venda de produtos agrícolas',
            'cor': '#28a745'
        },
        {
            'nome': 'Prestação de Serviços',
            'codigo': 'REC002',
            'descricao': 'Receita com prestação de serviços',
            'cor': '#007bff'
        },
        {
            'nome': 'Arrendamento',
            'codigo': 'REC003',
            'descricao': 'Receita com arrendamento de terras',
            'cor': '#ffc107'
        },
        {
            'nome': 'Outras Receitas',
            'codigo': 'REC004',
            'descricao': 'Outras receitas diversas',
            'cor': '#6c757d'
        },
    ]
    
    for tipo_data in tipos_receita:
        tipo, created = TipoReceita.objects.get_or_create(
            codigo=tipo_data['codigo'],
            defaults=tipo_data
        )
        if created:
            print(f"  ✓ Criado: {tipo.nome}")
        else:
            print(f"  - Já existe: {tipo.nome}")


def criar_dados_exemplo():
    """Cria dados de exemplo para teste"""
    print("Criando dados de exemplo...")
    
    # Fornecedores de exemplo
    fornecedores = [
        {
            'razao_social': 'Agro Fornecedores Ltda',
            'fantasia': 'Agro Fornecedores',
            'cnpj': '12.345.678/0001-90',
            'email': 'contato@agrofornecedores.com',
            'telefone': '(11) 99999-9999'
        },
        {
            'razao_social': 'Máquinas e Implementos S.A.',
            'fantasia': 'Máquinas S.A.',
            'cnpj': '98.765.432/0001-10',
            'email': 'vendas@maquinassa.com',
            'telefone': '(11) 88888-8888'
        },
        {
            'razao_social': 'Combustíveis do Campo Ltda',
            'fantasia': 'Combustíveis Campo',
            'cnpj': '11.222.333/0001-44',
            'email': 'vendas@combustiveiscampo.com',
            'telefone': '(11) 77777-7777'
        }
    ]
    
    for fornecedor_data in fornecedores:
        fornecedor, created = Fornecedor.objects.get_or_create(
            cnpj=fornecedor_data['cnpj'],
            defaults=fornecedor_data
        )
        if created:
            print(f"  ✓ Fornecedor criado: {fornecedor.razao_social}")
        else:
            print(f"  - Fornecedor já existe: {fornecedor.razao_social}")
    
    # Clientes de exemplo
    clientes = [
        {
            'nome': 'João Silva',
            'cpf': '123.456.789-00',
            'email': 'joao.silva@email.com',
            'telefone': '(11) 99999-1111'
        },
        {
            'nome': 'Maria Santos',
            'cpf': '987.654.321-00',
            'email': 'maria.santos@email.com',
            'telefone': '(11) 99999-2222'
        }
    ]
    
    for cliente_data in clientes:
        cliente, created = Cliente.objects.get_or_create(
            cpf=cliente_data['cpf'],
            defaults=cliente_data
        )
        if created:
            print(f"  ✓ Cliente criado: {cliente.nome}")
        else:
            print(f"  - Cliente já existe: {cliente.nome}")
    
    # Faturados de exemplo
    faturados = [
        {
            'nome_completo': 'João Silva',
            'cpf': '123.456.789-00',
            'email': 'joao.silva@email.com',
            'telefone': '(11) 99999-1111'
        },
        {
            'nome_completo': 'Maria Santos',
            'cpf': '987.654.321-00',
            'email': 'maria.santos@email.com',
            'telefone': '(11) 99999-2222'
        }
    ]
    
    for faturado_data in faturados:
        faturado, created = Faturado.objects.get_or_create(
            cpf=faturado_data['cpf'],
            defaults=faturado_data
        )
        if created:
            print(f"  ✓ Faturado criado: {faturado.nome_completo}")
        else:
            print(f"  - Faturado já existe: {faturado.nome_completo}")


def main():
    """Função principal"""
    print("=== POPULANDO BANCO DE DADOS COM DADOS INICIAIS ===")
    print()
    
    try:
        # Criar tipos de despesa
        criar_tipos_despesa()
        print()
        
        # Criar tipos de receita
        criar_tipos_receita()
        print()
        
        # Criar dados de exemplo
        criar_dados_exemplo()
        print()
        
        print("=== POPULAÇÃO CONCLUÍDA COM SUCESSO ===")
        print()
        print("Dados criados:")
        print(f"- {TipoDespesa.objects.count()} tipos de despesa")
        print(f"- {TipoReceita.objects.count()} tipos de receita")
        print(f"- {Fornecedor.objects.count()} fornecedores")
        print(f"- {Cliente.objects.count()} clientes")
        print(f"- {Faturado.objects.count()} faturados")
        
    except Exception as e:
        print(f"Erro ao popular banco de dados: {e}")
        return False
    
    return True


if __name__ == "__main__":
    main()



