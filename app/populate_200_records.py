# -*- coding: utf-8 -*-
"""
Script para popular o banco de dados com 200 registros para testes
Execute: python manage.py shell < populate_200_records.py
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_admin.settings')
django.setup()

from apps.fornecedores.models import Fornecedor
from apps.clientes.models import Cliente
from apps.faturados.models import Faturado
from apps.tipos_despesa.models import TipoDespesa
from apps.tipos_receita.models import TipoReceita
from apps.contas_pagar.models import ContaPagar
from apps.contas_receber.models import ContaReceber
from apps.core.models import CategoriaDespesa

# Dados para geração
NOMES = ['João', 'Maria', 'José', 'Ana', 'Pedro', 'Paula', 'Carlos', 'Carla', 'Lucas', 'Lucia', 
         'Rafael', 'Rafaela', 'Bruno', 'Bruna', 'Diego', 'Diana', 'Felipe', 'Fernanda', 'Gabriel', 'Gabriela']
SOBRENOMES = ['Silva', 'Santos', 'Oliveira', 'Souza', 'Rodrigues', 'Ferreira', 'Alves', 'Pereira', 
              'Lima', 'Gomes', 'Costa', 'Ribeiro', 'Martins', 'Carvalho', 'Almeida', 'Lopes', 'Soares', 'Fernandes']
EMPRESAS = ['Tech', 'Solutions', 'Systems', 'Digital', 'Corp', 'Group', 'Services', 'Brasil', 'Global', 'Prime']
SEGMENTOS = ['Informática', 'Alimentação', 'Transporte', 'Consultoria', 'Marketing', 'Construção', 'Energia', 'Saúde']

def gerar_cpf():
    """Gera CPF formatado válido"""
    cpf = [random.randint(0, 9) for _ in range(9)]
    for _ in range(2):
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11
        cpf.append(11 - val if val > 1 else 0)
    return '{}.{}.{}-{}'.format(''.join(map(str, cpf[:3])), ''.join(map(str, cpf[3:6])), 
                                 ''.join(map(str, cpf[6:9])), ''.join(map(str, cpf[9:])))

def gerar_cnpj():
    """Gera CNPJ formatado"""
    cnpj = [random.randint(0, 9) for _ in range(8)] + [0, 0, 0, 1]
    for _ in range(2):
        val = sum([v * (i % 8 + 2) for i, v in enumerate(reversed(cnpj))]) % 11
        cnpj.append(11 - val if val > 1 else 0)
    return '{}.{}.{}/{}-{}'.format(''.join(map(str, cnpj[:2])), ''.join(map(str, cnpj[2:5])),
                                    ''.join(map(str, cnpj[5:8])), ''.join(map(str, cnpj[8:12])),
                                    ''.join(map(str, cnpj[12:])))

def gerar_telefone():
    """Gera telefone formatado"""
    ddd = random.choice(['11', '21', '31', '41', '51', '61', '71', '81'])
    return f'({ddd}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}'

def gerar_email(nome):
    """Gera email baseado no nome"""
    dominio = random.choice(['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com.br', 'empresa.com.br'])
    return f'{nome.lower().replace(" ", ".")}{random.randint(1, 999)}@{dominio}'

print("=" * 60)
print("INICIANDO POPULAÇÃO DO BANCO DE DADOS")
print("=" * 60)

# 1. Criar Tipos de Despesa (9 categorias)
print("\n[1/7] Criando Tipos de Despesa...")
tipos_despesa_data = [
    ('Salários e Encargos', 'DESP001', CategoriaDespesa.PESSOAL, '#e74c3c', 'salário, folha, encargos, férias, 13º'),
    ('Aluguel e Condomínio', 'DESP002', CategoriaDespesa.INSTALACOES, '#9b59b6', 'aluguel, condomínio, iptu'),
    ('Energia Elétrica', 'DESP003', CategoriaDespesa.UTILIDADES, '#f39c12', 'energia, luz, eletricidade'),
    ('Água e Esgoto', 'DESP004', CategoriaDespesa.UTILIDADES, '#3498db', 'água, esgoto, saneamento'),
    ('Internet e Telefone', 'DESP005', CategoriaDespesa.COMUNICACAO, '#1abc9c', 'internet, telefone, comunicação'),
    ('Material de Escritório', 'DESP006', CategoriaDespesa.MATERIAIS, '#e67e22', 'papel, caneta, material'),
    ('Combustível', 'DESP007', CategoriaDespesa.TRANSPORTE, '#34495e', 'combustível, gasolina, diesel'),
    ('Manutenção', 'DESP008', CategoriaDespesa.MANUTENCAO, '#7f8c8d', 'manutenção, reparo, conserto'),
    ('Marketing', 'DESP009', CategoriaDespesa.MARKETING, '#2ecc71', 'marketing, propaganda, publicidade'),
]

for nome, codigo, categoria, cor, palavras in tipos_despesa_data:
    TipoDespesa.objects.get_or_create(
        codigo=codigo,
        defaults={
            'nome': nome,
            'categoria': categoria,
            'cor': cor,
            'palavras_chave': palavras,
            'ativo': True
        }
    )
print(f"   Criados {TipoDespesa.objects.count()} tipos de despesa")

# 2. Criar Tipos de Receita
print("\n[2/7] Criando Tipos de Receita...")
tipos_receita_data = [
    ('Vendas de Produtos', 'REC001', '#27ae60'),
    ('Prestação de Serviços', 'REC002', '#2980b9'),
    ('Consultoria', 'REC003', '#8e44ad'),
    ('Aluguel de Equipamentos', 'REC004', '#f39c12'),
    ('Comissões', 'REC005', '#e74c3c'),
    ('Juros e Rendimentos', 'REC006', '#1abc9c'),
]

for nome, codigo, cor in tipos_receita_data:
    TipoReceita.objects.get_or_create(
        codigo=codigo,
        defaults={
            'nome': nome,
            'cor': cor,
            'descricao': f'Receitas provenientes de {nome.lower()}',
            'ativo': True
        }
    )
print(f"   Criados {TipoReceita.objects.count()} tipos de receita")

# 3. Criar Fornecedores (40 registros)
print("\n[3/7] Criando Fornecedores...")
for i in range(40):
    nome_empresa = f'{random.choice(NOMES)} {random.choice(EMPRESAS)} {random.choice(SEGMENTOS)}'
    try:
        Fornecedor.objects.create(
            razao_social=f'{nome_empresa} LTDA #{i+1}',
            fantasia=nome_empresa,
            cnpj=gerar_cnpj(),
            email=gerar_email(nome_empresa.split()[0]),
            telefone=gerar_telefone(),
            endereco=f'Rua {random.choice(SOBRENOMES)}, {random.randint(1, 999)} - Centro',
            ativo=True
        )
    except:
        pass
print(f"   Criados {Fornecedor.objects.count()} fornecedores")

# 4. Criar Clientes (40 registros)
print("\n[4/7] Criando Clientes...")
for i in range(40):
    nome = f'{random.choice(NOMES)} {random.choice(SOBRENOMES)}'
    try:
        Cliente.objects.create(
            nome=f'{nome} #{i+1}',
            cpf=gerar_cpf(),
            email=gerar_email(nome.split()[0]),
            telefone=gerar_telefone(),
            endereco=f'Rua {random.choice(SOBRENOMES)}, {random.randint(1, 999)}',
            data_nascimento=datetime.now().date() - timedelta(days=random.randint(7000, 25000)),
            ativo=True
        )
    except:
        pass
print(f"   Criados {Cliente.objects.count()} clientes")

# 5. Criar Faturados (40 registros)
print("\n[5/7] Criando Faturados...")
for i in range(40):
    nome = f'{random.choice(NOMES)} {random.choice(SOBRENOMES)}'
    try:
        Faturado.objects.create(
            nome_completo=f'{nome} #{i+1}',
            cpf=gerar_cpf(),
            email=gerar_email(nome.split()[0]),
            telefone=gerar_telefone(),
            endereco=f'Av. {random.choice(SOBRENOMES)}, {random.randint(1, 999)}',
            ativo=True
        )
    except:
        pass
print(f"   Criados {Faturado.objects.count()} faturados")

# 6. Criar Contas a Pagar (40 registros)
print("\n[6/7] Criando Contas a Pagar...")
fornecedores = list(Fornecedor.objects.filter(ativo=True))
faturados = list(Faturado.objects.filter(ativo=True))
tipos_despesa = list(TipoDespesa.objects.filter(ativo=True))

if fornecedores and faturados:
    for i in range(40):
        try:
            conta = ContaPagar.objects.create(
                fornecedor=random.choice(fornecedores),
                faturado=random.choice(faturados),
                numero_nota_fiscal=f'NF-{random.randint(10000, 99999)}',
                data_emissao=datetime.now().date() - timedelta(days=random.randint(1, 365)),
                descricao_produtos=f'Compra de {random.choice(["materiais", "equipamentos", "serviços", "produtos"])} diversos',
                valor_total=Decimal(str(random.randint(100, 50000) + random.random())).quantize(Decimal('0.01')),
                quantidade_parcelas=random.randint(1, 12),
                status=random.choice(['PENDENTE', 'PAGA', 'VENCIDA']),
                ativo=True
            )
            if tipos_despesa:
                conta.tipos_despesa.add(random.choice(tipos_despesa))
        except:
            pass
print(f"   Criados {ContaPagar.objects.count()} contas a pagar")

# 7. Criar Contas a Receber (40 registros)
print("\n[7/7] Criando Contas a Receber...")
clientes = list(Cliente.objects.filter(ativo=True))
tipos_receita = list(TipoReceita.objects.filter(ativo=True))

if clientes:
    for i in range(40):
        try:
            conta = ContaReceber.objects.create(
                cliente=random.choice(clientes),
                numero_documento=f'DOC-{random.randint(10000, 99999)}',
                data_emissao=datetime.now().date() - timedelta(days=random.randint(1, 365)),
                descricao=f'Venda de {random.choice(["produtos", "serviços", "consultoria", "equipamentos"])}',
                valor_total=Decimal(str(random.randint(500, 100000) + random.random())).quantize(Decimal('0.01')),
                quantidade_parcelas=random.randint(1, 12),
                status=random.choice(['PENDENTE', 'PAGA', 'VENCIDA']),
                ativo=True
            )
            if tipos_receita:
                conta.tipos_receita.add(random.choice(tipos_receita))
        except:
            pass
print(f"   Criados {ContaReceber.objects.count()} contas a receber")

print("\n" + "=" * 60)
print("POPULAÇÃO CONCLUÍDA COM SUCESSO!")
print("=" * 60)
print(f"\nResumo:")
print(f"  - Tipos de Despesa: {TipoDespesa.objects.count()}")
print(f"  - Tipos de Receita: {TipoReceita.objects.count()}")
print(f"  - Fornecedores: {Fornecedor.objects.count()}")
print(f"  - Clientes: {Cliente.objects.count()}")
print(f"  - Faturados: {Faturado.objects.count()}")
print(f"  - Contas a Pagar: {ContaPagar.objects.count()}")
print(f"  - Contas a Receber: {ContaReceber.objects.count()}")
print(f"\nTOTAL: {TipoDespesa.objects.count() + TipoReceita.objects.count() + Fornecedor.objects.count() + Cliente.objects.count() + Faturado.objects.count() + ContaPagar.objects.count() + ContaReceber.objects.count()} registros")

