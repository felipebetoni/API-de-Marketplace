# Instalação Local (sem Docker)

## Pré-requisitos

- Python 3.11 ou superior
- PostgreSQL 12 ou superior
- pip (gerenciador de pacotes Python)

## Passo 1: Clonar o Repositório

```bash
cd "API de Marketplace"
```

## Passo 2: Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

## Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

## Passo 4: Configurar Banco de Dados

### Opção A: PostgreSQL Local

```bash
# Windows/Mac/Linux - abra um terminal PostgreSQL

# Crie banco e usuário:
psql -U postgres

CREATE USER marketplace_user WITH PASSWORD 'marketplace_pass';
CREATE DATABASE marketplace_db OWNER marketplace_user;

# Dê permissões:
GRANT ALL PRIVILEGES ON DATABASE marketplace_db TO marketplace_user;

# Saia
\q
```

### Opção B: Docker Apenas para Banco

```bash
docker run -d \
  --name marketplace_db \
  -e POSTGRES_USER=marketplace_user \
  -e POSTGRES_PASSWORD=marketplace_pass \
  -e POSTGRES_DB=marketplace_db \
  -p 5432:5432 \
  postgres:15-alpine
```

## Passo 5: Configurar Variáveis de Ambiente

```bash
# Copie o template
cp .env.example .env

# Edite .env com suas credenciais
# Verifique DATABASE_URL:
# DATABASE_URL=postgresql://marketplace_user:marketplace_pass@localhost:5432/marketplace_db
```

## Passo 6: Iniciar a Aplicação

```bash
# Terminal 1 - API
uvicorn app.main:app --reload

# Saída esperada:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

## Passo 7: Testar

```bash
# Abra outro terminal

# Terminal 2 - Testes
curl http://localhost:8000/health

# Resposta esperada:
# {"status":"healthy"}
```

## 📚 Acessar Documentação

- **Swagger UI (interactive)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **JSON Schema**: http://localhost:8000/openapi.json

## ⚙️ Desenvolvimento

### Hot Reload Ativo

O comando `--reload` recarrega a aplicação quando há mudanças nos arquivos.

### Estrutura de Pastas Esperada

```
app/
├── main.py
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
├── models/
├── schemas/
├── routes/
├── services/
└── dependencies/
```

### Testes Manuais

```bash
# Registrar usuário
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email":"user@test.com",
    "username":"testuser",
    "password":"TestPass123!"
  }'

# Fazer login
curl -X POST http://localhost:8000/auth/login \
  -d "username=testuser&password=TestPass123!"
```

## 🐛 Debugging

### Ver Variáveis Carregadas

```python
# Em app/core/config.py
from app.core.config import settings
print(settings.database_url)
print(settings.secret_key)
```

### Ativar Modo Debug

Edite `.env`:
```
DEBUG=True
```

### Ver Queries SQL

Edite `app/core/database.py`:
```python
engine = create_engine(settings.database_url, echo=True)  # Mostra SQL
```

## 🛑 Parar a Aplicação

```bash
# No terminal onde rodou uvicorn
Ctrl + C
```

## 🧹 Limpar Ambiente

```bash
# Desativar venv
deactivate

# Remover venv (opcional)
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows
```

## 📝 Resumo dos Comandos

```bash
# Criar venv
python -m venv venv

# Ativar venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Iniciar API
uvicorn app.main:app --reload

# Acessar docs
# http://localhost:8000/docs
```

## ⚠️ Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Verifique se venv está ativo
which python  # Deve mostrar caminho dentro de venv/

# Reinstale dependências
pip install -r requirements.txt
```

### "Could not connect to PostgreSQL"
```bash
# Verifique conexão
psql -U marketplace_user -d marketplace_db -h localhost

# Ou com Docker
docker logs marketplace_db

# Verifique DATABASE_URL em .env
```

### "Port 8000 already in use"
```bash
# Use outra porta
uvicorn app.main:app --reload --port 8001
```

## 🎓 Próximos Passos

1. Leia [GUIA_USO.md](GUIA_USO.md) para aprender a usar a API
2. Explore [ARQUITETURA.md](ARQUITETURA.md) para entender a estrutura
3. Veja [EXEMPLOS_REQUESTS.md](EXEMPLOS_REQUESTS.md) para exemplos práticos
4. Se houver problemas, consulte [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
