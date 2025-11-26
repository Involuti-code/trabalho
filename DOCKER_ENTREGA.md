# Entrega Docker - Sistema Administrativo-Financeiro

## Arquivos Docker do Projeto

O projeto contém os seguintes arquivos para containerização:

| Arquivo | Descrição |
|---------|-----------|
| `Dockerfile` | Define a imagem Docker do projeto |
| `docker-compose.yml` | Orquestra os serviços (fácil execução) |
| `entrypoint.sh` | Script de inicialização do container |
| `.dockerignore` | Arquivos ignorados no build |

---

## Como Executar com Docker

### Pré-requisitos
- Docker instalado: https://www.docker.com/get-started
- Docker Compose instalado (geralmente vem junto)

### Passo 1: Clonar o repositório
```bash
git clone https://github.com/Involuti-code/trabalho.git
cd trabalho
```

### Passo 2: Construir e executar
```bash
docker-compose up --build
```

### Passo 3: Acessar o sistema
- **Sistema**: http://localhost:8000
- **Admin**: http://localhost:8000/admin

### Passo 4: Criar usuário administrador (em outro terminal)
```bash
docker-compose exec web python manage.py createsuperuser
```

### Passo 5: Popular banco com dados de teste (opcional)
```bash
docker-compose exec web python manage.py shell < populate_200_records.py
```

---

## Comandos Docker Úteis

```bash
# Iniciar em background
docker-compose up -d

# Parar os containers
docker-compose down

# Ver logs
docker-compose logs -f

# Acessar o shell do container
docker-compose exec web bash

# Rebuild após alterações
docker-compose up --build
```

---

## Estrutura dos Arquivos Docker

### Dockerfile
```dockerfile
FROM python:3.11-slim
# Imagem base Python 3.11

WORKDIR /code
# Diretório de trabalho

# Instala dependências do sistema
RUN apt-get update && apt-get install -y build-essential curl tzdata

# Instala dependências Python
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copia código do projeto
COPY . /code/

# Expõe porta 8000
EXPOSE 8000

# Script de entrada
ENTRYPOINT ["/entrypoint.sh"]
```

### docker-compose.yml
```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/code
    environment:
      - DEBUG=1
```

---

## Links do Projeto

- **GitHub**: https://github.com/Involuti-code/trabalho
- **Site Online**: https://involuti.pythonanywhere.com

---

## Credenciais de Acesso (Desenvolvimento)

- **Usuário**: admin (criar com createsuperuser)
- **Senha**: definida na criação

---

## Tecnologias Utilizadas

- Python 3.11
- Django 4.2.7
- SQLite (desenvolvimento)
- Bootstrap 5
- Docker & Docker Compose

