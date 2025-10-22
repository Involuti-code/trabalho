# 📚 Documentação Única do Projeto

## Sumário
- Visão Geral
- Tecnologias e Arquitetura
- Estrutura do Projeto
- Status do Sistema e Módulos
- APIs REST Implementadas (Resumo)
- Interface Web (Resumo)
- IA e Processamento de PDF
- Classificação de Despesas Agrícolas (Regras)
- Correções Importantes (Erros resolvidos)
- Instalação e Execução
- Comandos Úteis
- Próximos Passos

---

## Visão Geral
Sistema administrativo-financeiro para gestão de fornecedores, clientes, contas a pagar/receber, parcelas e processamento de notas fiscais em PDF com IA (Gemini). Inclui interface web (Django), APIs REST e componentes de processamento.

---

## Tecnologias e Arquitetura
- Backend: Django 4.2.x, Django REST Framework
- IA: Google Gemini; extração de texto com pypdf
- Infra: SQLite (desenvolvimento), pronto para PostgreSQL
- Frontend: Templates Django + Bootstrap 5 + Chart.js
- Extras: Flask para endpoints específicos (opcional)

---

## Estrutura do Projeto (alto nível)
```
trabalho/
├─ app/
│  ├─ sistema_admin/ (settings, urls)
│  ├─ apps/ (core, fornecedores, clientes, faturados, tipos_receita, tipos_despesa, contas_pagar, contas_receber, parcelas, pdf_processor, pdf_extractor)
│  ├─ templates/ e static/
│  ├─ flask_api.py (API auxiliar)
│  ├─ setup_database.py, manage.py
│  └─ db.sqlite3
├─ scripts: install_dependencies.bat, iniciar_sistema.bat
├─ utils e serviços auxiliares
└─ DOCUMENTACAO_UNICA.md, README.md
```

---

## Status do Sistema e Módulos
- Modelos Django implementados para 9+ apps (cadastros, financeiro e PDF)
- Admin configurado, validações, índices e relacionamentos
- APIs REST completas para: core, fornecedores, clientes, faturados, tipos de receita/despesa, parcelas, contas a pagar/receber, pdf_processor
- Interface web com dashboard, fornecedores e processador de PDF

---

## APIs REST Implementadas (Resumo)
- Base URL: `http://localhost:8000/api/`
- Recursos com CRUD, filtros, busca, ordenação e ações customizadas
- Exemplos:
  - Fornecedores: `/api/fornecedores/`, `/api/fornecedores/buscar/?q=`
  - Contas a pagar: `/api/contas-pagar/pendentes/`, `/api/contas-pagar/classificar-lote/`
  - Tipos de despesa: `/api/tipos-despesa/classificar/`
  - PDF: `/api/pdf-processor/processar/`

---

## Interface Web (Resumo)
- Páginas: Dashboard (`/`), Fornecedores (`/fornecedores/`), Processador de PDF (`/pdf-processor/`), Admin (`/admin/`)
- Recursos: gráficos (Chart.js), tabelas, upload drag & drop, modais, paginação, validações e tema responsivo

---

## IA e Processamento de PDF
- Extração real com `pypdf` (sem texto simulado)
- Prompt Gemini revisado com instruções críticas (não inventar dados; usar null quando ausente)
- Logs de debug habilitados e tratamento de erros
- Quando necessário, processamento local por regras/regex como fallback (onde aplicável)

---

## Classificação de Despesas Agrícolas (Regras)
Categorias suportadas para classificação automática a partir da descrição dos itens:
- Insumos Agrícolas
- Manutenção e Operação (inclui combustíveis, peças, ferramentas, multímetro, kits)
- Recursos Humanos
- Serviços Operacionais
- Infraestrutura e Utilidades
- Administrativas
- Seguros e Proteção
- Impostos e Taxas
- Investimentos
- Outros

Ajustes aplicados: reforço de palavras-chave para ferramentas e equipamentos de manutenção para evitar classificação em “Outros”.

---

## Correções Importantes (Erros resolvidos)
- Template: adicionado `{% load static %}` em `templates/base/base.html`
- Login 404: incluídas URLs de autenticação e removido `@login_required` onde não necessário
- Dependências: inclusão de `requests` no `requirements.txt`
- Extração PDF: troca para `pypdf` e envio somente de texto real à IA

---

## Instalação e Execução
Pré-requisitos: Python 3.11+ (ou 3.7+), pip

1) Instalar dependências
```bash
install_dependencies.bat
# ou
pip install -r requirements.txt
```

2) Preparar banco e executar
```bash
cd app
python manage.py migrate
python manage.py runserver
```

3) Acessos principais
- Dashboard: `http://localhost:8000/`
- Fornecedores: `http://localhost:8000/fornecedores/`
- PDF: `http://localhost:8000/pdf-processor/`
- Admin: `http://localhost:8000/admin/`

---

## Comandos Úteis
```bash
# Django
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py test

# Flask auxiliar (quando usado)
python flask_api.py
```

---

## Próximos Passos
- Expandir autenticação e permissões
- Melhorar validação de dados extraídos
- Otimizar prompts e cache de resultados IA
- Produção: PostgreSQL, Nginx/ASGI, monitoramento e logs
