#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arquivo de configuração do Sistema Administrativo
"""

# Configurações da Interface
INTERFACE_CONFIG = {
    'titulo': 'Sistema Administrativo - N2',
    'largura': 800,
    'altura': 600,
    'cor_fundo': '#f0f0f0',
    'fonte_titulo': ('Arial', 16, 'bold'),
    'fonte_normal': ('Arial', 10),
    'fonte_pequena': ('Arial', 8)
}

# Configurações de Cores
CORES = {
    'primaria': '#2196F3',
    'secundaria': '#4CAF50',
    'sucesso': '#4CAF50',
    'aviso': '#FF9800',
    'erro': '#F44336',
    'info': '#2196F3',
    'neutro': '#607D8B'
}

# Configurações do Banco de Dados
DATABASE_CONFIG = {
    'tipo': 'json',  # 'json', 'sqlite', 'mysql', 'postgresql'
    'arquivo': 'dados_sistema.json',
    'backup_automatico': True,
    'intervalo_backup': 300  # segundos
}

# Configurações de Log
LOG_CONFIG = {
    'ativo': True,
    'arquivo': 'sistema.log',
    'nivel': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'formato': '%(asctime)s - %(levelname)s - %(message)s'
}

# Configurações de Validação
VALIDACAO_CONFIG = {
    'email_regex': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'telefone_regex': r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
    'cpf_regex': r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
    'cnpj_regex': r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$'
}

# Configurações de Relatórios
RELATORIO_CONFIG = {
    'formato_data': '%d/%m/%Y',
    'formato_data_hora': '%d/%m/%Y %H:%M:%S',
    'itens_por_pagina': 20,
    'diretorio_relatorios': 'relatorios'
}

# Configurações de Segurança
SEGURANCA_CONFIG = {
    'senha_minima': 6,
    'tentativas_login': 3,
    'bloqueio_temporario': 300,  # segundos
    'criptografia': True
}

# Configurações de Backup
BACKUP_CONFIG = {
    'ativo': True,
    'diretorio': 'backups',
    'frequencia': 'diario',  # 'diario', 'semanal', 'mensal'
    'manter_backups': 30  # dias
}

# Configurações de Notificações
NOTIFICACAO_CONFIG = {
    'email_ativo': False,
    'smtp_server': '',
    'smtp_port': 587,
    'email_remetente': '',
    'senha_email': '',
    'notificacoes_sistema': True
}

# Configurações de Exportação
EXPORTACAO_CONFIG = {
    'formatos_suportados': ['csv', 'xlsx', 'pdf', 'json'],
    'diretorio_exportacao': 'exportacoes',
    'incluir_cabecalho': True,
    'separador_csv': ';'
}

# Configurações de Importação
IMPORTACAO_CONFIG = {
    'formatos_suportados': ['csv', 'xlsx', 'json'],
    'diretorio_importacao': 'importacoes',
    'validar_dados': True,
    'criar_backup': True
}

# Configurações de Performance
PERFORMANCE_CONFIG = {
    'cache_ativo': True,
    'tamanho_cache': 100,  # MB
    'timeout_operacoes': 30,  # segundos
    'threading_ativo': True
}

# Configurações de Idioma
IDIOMA_CONFIG = {
    'idioma_padrao': 'pt_BR',
    'formatos_data': {
        'pt_BR': '%d/%m/%Y',
        'en_US': '%m/%d/%Y',
        'es_ES': '%d/%m/%Y'
    },
    'formatos_moeda': {
        'pt_BR': 'R$ {:.2f}',
        'en_US': '${:.2f}',
        'es_ES': '€ {:.2f}'
    }
}

# Configurações de Tema
TEMA_CONFIG = {
    'tema_ativo': 'claro',  # 'claro', 'escuro'
    'cores_claro': {
        'fundo': '#ffffff',
        'texto': '#000000',
        'borda': '#cccccc',
        'destaque': '#2196F3'
    },
    'cores_escuro': {
        'fundo': '#2b2b2b',
        'texto': '#ffffff',
        'borda': '#555555',
        'destaque': '#4CAF50'
    }
}

def obter_configuracao(secao, chave, valor_padrao=None):
    """
    Obtém uma configuração específica
    
    Args:
        secao (str): Nome da seção de configuração
        chave (str): Nome da chave
        valor_padrao: Valor padrão se não encontrar
    
    Returns:
        Valor da configuração ou valor padrão
    """
    try:
        configs = globals()
        if secao in configs:
            secao_config = configs[secao]
            if chave in secao_config:
                return secao_config[chave]
        return valor_padrao
    except Exception:
        return valor_padrao

def definir_configuracao(secao, chave, valor):
    """
    Define uma configuração específica
    
    Args:
        secao (str): Nome da seção de configuração
        chave (str): Nome da chave
        valor: Valor a ser definido
    """
    try:
        configs = globals()
        if secao in configs:
            configs[secao][chave] = valor
    except Exception as e:
        print(f"Erro ao definir configuração: {e}")

def carregar_configuracao_arquivo(arquivo='config.json'):
    """
    Carrega configurações de um arquivo JSON
    
    Args:
        arquivo (str): Caminho do arquivo de configuração
    """
    try:
        import json
        with open(arquivo, 'r', encoding='utf-8') as f:
            configs = json.load(f)
        
        # Aplica as configurações carregadas
        for secao, valores in configs.items():
            if secao in globals():
                globals()[secao].update(valores)
        
        print(f"Configurações carregadas de {arquivo}")
    except FileNotFoundError:
        print(f"Arquivo de configuração {arquivo} não encontrado")
    except Exception as e:
        print(f"Erro ao carregar configurações: {e}")

def salvar_configuracao_arquivo(arquivo='config.json'):
    """
    Salva configurações em um arquivo JSON
    
    Args:
        arquivo (str): Caminho do arquivo de configuração
    """
    try:
        import json
        
        # Coleta todas as configurações
        configs = {}
        for nome in globals():
            if nome.endswith('_CONFIG'):
                configs[nome] = globals()[nome]
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(configs, f, ensure_ascii=False, indent=2)
        
        print(f"Configurações salvas em {arquivo}")
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")

if __name__ == "__main__":
    # Teste das configurações
    print("Configurações do Sistema Administrativo")
    print("=" * 40)
    
    print(f"Título: {obter_configuracao('INTERFACE_CONFIG', 'titulo')}")
    print(f"Largura: {obter_configuracao('INTERFACE_CONFIG', 'largura')}")
    print(f"Altura: {obter_configuracao('INTERFACE_CONFIG', 'altura')}")
    print(f"Cor Primária: {obter_configuracao('CORES', 'primaria')}")
    print(f"Tipo de Banco: {obter_configuracao('DATABASE_CONFIG', 'tipo')}")

