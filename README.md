# Sistema Administrativo-Financeiro (N2)

Projeto Django com interface web e APIs para gestão financeira (fornecedores, clientes, contas, parcelas) e processamento de notas fiscais em PDF com IA (Gemini).

## Requisitos
- Python 3.11+ (Windows 10/11)
- Pip atualizado

## Quickstart
```bash
# 1) Instalar dependências
install_dependencies.bat
# ou
pip install -r requirements.txt

# 2) Iniciar o servidor
cd app
python manage.py migrate
python manage.py runserver
```

Acesse:
- Dashboard: http://localhost:8000/
- Fornecedores: http://localhost:8000/fornecedores/
- Processador de PDF: http://localhost:8000/pdf-processor/
- Admin: http://localhost:8000/admin/

## Estrutura Essencial
```
trabalho/
├─ app/                # Projeto Django (apps, templates, static)
├─ requirements.txt    # Dependências
├─ iniciar_sistema.bat # Launcher
├─ install_dependencies.bat
├─ DOCUMENTACAO_UNICA.md
└─ README.md
```

## IA e PDF (resumo)
- Extração real de texto com `pypdf`
- Prompt Gemini com instruções para não inventar dados
- Ação: POST /api/pdf-processor/processar/ (quando exposto)

## Documentação Completa
Consulte o documento consolidado:
- DOCUMENTACAO_UNICA.md

---

## Docker

Pré-requisitos:
- Docker e Docker Compose instalados

Comandos:
```bash
# 1) Build
docker compose build

# 2) Subir containers
docker compose up -d

# 3) Logs
docker compose logs -f web

# 4) Parar
docker compose down
```

Variáveis úteis (override via `docker-compose.yml` ou `-e`):
- `DEBUG=1`
- `ALLOWED_HOSTS=localhost,127.0.0.1`
- `GEMINI_API_KEY=...` (se usar IA)

Volumes mapeados:
- `./` → `/code` (código)
- `django_static` → `/code/app/staticfiles`
- `django_media` → `/code/app/media`
- `django_logs` → `/code/app/logs`

O app roda em `http://localhost:8000`.

