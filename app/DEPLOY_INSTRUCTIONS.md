# Instruções de Deploy - Sistema Administrativo-Financeiro

## Requisitos do Projeto (Etapa 2)

### 1. Interfaces Gráficas Implementadas

- **MANTER CONTAS**
  - Contas a Pagar (`/contas-pagar/`)
  - Contas a Receber (`/contas-receber/`)

- **MANTER PESSOAS**
  - Fornecedores (`/fornecedores/`)
  - Clientes (`/clientes/`)
  - Faturados (`/faturados/`)

- **MANTER CLASSIFICAÇÃO**
  - Tipos de Receita (`/tipos-receita/`)
  - Tipos de Despesa (`/tipos-despesa/`)

### 2. Layout Implementado

- ✅ Tabela de registros vazia por padrão
- ✅ Carregar dados através de Busca ou botão TODOS
- ✅ TODOS carrega apenas status = ATIVO
- ✅ Indexação/ordenação por coluna na tabela (clique no cabeçalho)
- ✅ Busca por múltiplos elementos
- ✅ Duas ações na tabela: Editar / Excluir (Lógico)
- ✅ No CREATE campo STATUS oculto == ATIVO
- ✅ No UPDATE campo STATUS oculto
- ✅ No DELETE altera campo STATUS == INATIVO

---

## Deploy

### Opção 1: PythonAnywhere (Python Backend)

1. Criar conta em https://www.pythonanywhere.com
2. Fazer upload do projeto ou clonar do GitHub
3. Criar virtualenv:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 meuambiente
   pip install -r requirements.txt
   ```
4. Configurar WSGI file apontando para `sistema_admin.wsgi`
5. Configurar variáveis de ambiente (sem expor API keys!)
6. Executar migrações:
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

### Opção 2: Render (JavaScript Backend)

1. Criar conta em https://render.com
2. Conectar repositório GitHub
3. Criar novo Web Service
4. Configurar Build Command: `pip install -r requirements.txt`
5. Configurar Start Command: `gunicorn sistema_admin.wsgi:application`
6. Adicionar variáveis de ambiente

### Opção 3: Docker

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Executar migrações
docker-compose exec web python manage.py migrate

# Popular dados de teste
docker-compose exec web python manage.py shell < populate_200_records.py
```

---

## Popular Banco de Dados (200 registros)

```bash
cd app
python manage.py shell < populate_200_records.py
```

Este script cria:
- 9 Tipos de Despesa
- 6 Tipos de Receita
- 40 Fornecedores
- 40 Clientes
- 40 Faturados
- 40 Contas a Pagar
- 40 Contas a Receber

**Total: ~215 registros**

---

## Segurança - API Keys

⚠️ **IMPORTANTE**: Não subir API keys para o repositório!

### Recomendação: Solicitar chaves ao abrir o sistema

O sistema deve solicitar as chaves de API (Gemini, etc.) através de:
1. Variáveis de ambiente no servidor
2. Modal de configuração na primeira execução
3. Arquivo `.env` local (não versionado)

### Configuração de Variáveis de Ambiente

```bash
# .env (NÃO versionar este arquivo!)
GEMINI_API_KEY=sua_chave_aqui
SECRET_KEY=sua_secret_key_django
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com
```

---

## Credenciais de Acesso (Desenvolvimento)

- **URL**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/
- **Usuário**: admin
- **Senha**: admin (criar com `python manage.py createsuperuser`)

---

## Links do Projeto

- **GitHub**: [Adicionar link do repositório]
- **Servidor**: [Adicionar link do deploy]

---

## Comandos Úteis

```bash
# Iniciar servidor de desenvolvimento
python manage.py runserver

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Popular banco com dados de teste
python manage.py shell < populate_200_records.py
```

