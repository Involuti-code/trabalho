# Comandos Git para Enviar Atualizações ao GitHub

## Passo a Passo

### 1. Navegar para o diretório do projeto
```bash
cd C:\Users\Adailton\Desktop\trabalho
```

### 2. Verificar o status das alterações
```bash
git status
```

### 3. Adicionar todos os arquivos modificados e novos
```bash
# Adicionar arquivos modificados
git add .dockerignore
git add .gitignore
git add Dockerfile
git add docker-compose.yml
git add entrypoint.sh
git add requirements.txt
git add RAG_IMPLEMENTACAO.md

# Adicionar arquivos do Django
git add app/sistema_admin/settings.py
git add app/sistema_admin/urls.py
git add app/templates/base/base.html

# Adicionar novo app RAG completo
git add app/apps/rag/

# Adicionar templates do RAG
git add app/templates/rag/

# Adicionar migrations
git add app/apps/contas_pagar/migrations/
git add app/apps/contas_receber/migrations/
git add app/apps/parcelas/migrations/

# OU adicionar tudo de uma vez:
git add .
```

### 4. Verificar o que será commitado
```bash
git status
```

### 5. Fazer o commit com uma mensagem descritiva
```bash
git commit -m "Implementação RAG - Busca Inteligente com acesso completo ao banco de dados

- Adicionado app RAG com RAG Simples e RAG Embeddings
- Implementada busca em todas as tabelas do sistema
- Adicionado contexto explicativo do sistema para o LLM
- Incluída busca em: Clientes, Fornecedores, Faturados, Contas a Pagar/Receber, Parcelas, Tipos de Despesa/Receita, ProcessamentoPDF
- Adicionadas estatísticas automáticas para perguntas sobre quantidade
- Corrigidos problemas de contraste de texto na interface
- Adicionadas migrations para contas_receber e parcelas
- Atualizado requirements.txt com sentence-transformers e torch"
```

### 6. Enviar para o GitHub
```bash
git push origin main
```

## Comandos Alternativos (Mais Rápido)

Se quiser fazer tudo de uma vez:

```bash
cd C:\Users\Adailton\Desktop\trabalho
git add .
git commit -m "Implementação RAG - Busca Inteligente com acesso completo ao banco de dados"
git push origin main
```

## Se houver conflitos

Se o GitHub tiver alterações que você não tem localmente:

```bash
git pull origin main
# Resolver conflitos se houver
git add .
git commit -m "Resolvendo conflitos"
git push origin main
```

## Verificar se foi enviado

```bash
git log --oneline -5
```

