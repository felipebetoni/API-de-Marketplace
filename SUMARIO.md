# 📋 Sumário do Projeto

## ✨ O que foi desenvolvido

Uma **API de Marketplace profissional** completa, pronta para produção, demonstrando as melhores práticas de desenvolvimento backend com **Python + FastAPI**.

## 📦 O que inclui

### ✅ Core Funcionalidades
- ✔ **Autenticação JWT** - Token Bearer com expiração
- ✔ **CRUD Usuarios** - Registro, login, perfil
- ✔ **CRUD Produtos** - Criar, listar, atualizar, deletar
- ✔ **CRUD Pedidos** - Criar pedidos, acompanhar status
- ✔ **Validação Pydantic** - Validação robusta de dados
- ✔ **Banco PostgreSQL** - Relacionamentos SQL
- ✔ **Segurança** - Hash bcrypt, proteção SQL injection

### ✅ DevOps & Deployment
- ✔ **Docker** - Containerização da API
- ✔ **Docker Compose** - Orquestração completa (API + DB + Nginx)
- ✔ **Nginx** - Reverse proxy, cache, load balancing
- ✔ **Health Checks** - Monitoramento de containers

### ✅ Documentação
- ✔ **README.md** - Visão geral completa
- ✔ **ARQUITETURA.md** - Design e estrutura
- ✔ **GUIA_USO.md** - Exemplos práticos
- ✔ **EXEMPLOS_REQUESTS.md** - cURL e Postman
- ✔ **INSTALACAO_LOCAL.md** - Setup sem Docker
- ✔ **TROUBLESHOOTING.md** - Solução de problemas

### ✅ Ferramentas & Configuração
- ✔ **requirements.txt** - Dependências Python
- ✔ **Dockerfile** - Imagem Docker
- ✔ **docker-compose.yml** - Stack completo
- ✔ **.env.example** - Template variáveis
- ✔ **.gitignore** - Segurança git
- ✔ **start.sh / start.bat** - Scripts rápidos

## 🏗️ Arquitetura

```
┌─────────────────┐
│   Cliente HTTP  │
└────────┬────────┘
         │
    ┌────▼────┐
    │  Nginx  │  (Reverse Proxy)
    └────┬────┘
         │
    ┌────▼────┐
    │  FastAPI │  (API)
    └────┬────┘
         │
    ┌────▼────┐
    │PostgreSQL│  (Banco)
    └─────────┘
```

### Stack Técnico

| Camada | Tecnologia |
|--------|-----------|
| **Web Server** | Nginx |
| **Framework** | FastAPI |
| **Async** | Uvicorn |
| **ORM** | SQLAlchemy |
| **Database** | PostgreSQL |
| **Auth** | JWT + bcrypt |
| **Validation** | Pydantic |
| **Containerization** | Docker |

## 📁 Estrutura de Arquivos

```
API de Marketplace/
├── 📄 README.md                 # Visão geral
├── 📄 GUIA_USO.md              # Como usar
├── 📄 ARQUITETURA.md           # Design
├── 📄 EXEMPLOS_REQUESTS.md     # Exemplos
├── 📄 INSTALACAO_LOCAL.md      # Setup local
├── 📄 TROUBLESHOOTING.md       # Problemas
├── 📄 requirements.txt          # Dependências
├── 📄 Dockerfile               # Imagem Docker
├── 📄 docker-compose.yml       # Orquestração
├── 📄 .env.example             # Template .env
├── 📄 .gitignore               # Git
├── 📄 start.sh                 # Script Linux/Mac
├── 📄 start.bat                # Script Windows
│
├── 📁 app/                     # Código principal
│   ├── main.py                 # App FastAPI
│   ├── core/
│   │   ├── config.py           # Configurações
│   │   ├── security.py         # JWT + Password
│   │   └── database.py         # Conexão DB
│   ├── models/
│   │   └── __init__.py         # User, Product, Order
│   ├── schemas/
│   │   └── __init__.py         # Pydantic models
│   ├── routes/
│   │   ├── auth.py             # /auth endpoints
│   │   ├── users.py            # /users endpoints
│   │   ├── products.py         # /products endpoints
│   │   └── orders.py           # /orders endpoints
│   ├── services/
│   │   └── crud.py             # Lógica negócio
│   └── dependencies/
│       └── auth.py             # Middleware auth
│
└── 📁 nginx/                   # Configuração Nginx
    ├── nginx.conf
    └── conf.d/
        └── default.conf
```

## 🚀 Quick Start

### Com Docker (Recomendado)
```bash
cd "API de Marketplace"
docker-compose up -d
# API em http://localhost
# Docs em http://localhost/docs
```

### Sem Docker
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🔌 Endpoints Principais

### Autenticação
```
POST   /auth/register      - Criar conta
POST   /auth/login        - Fazer login
```

### Usuários
```
GET    /users/me          - Dados do usuário
GET    /users/{id}        - Dados de outro usuário
```

### Produtos
```
POST   /products          - Criar produto
GET    /products          - Listar todos
GET    /products/{id}     - Ver produto
GET    /products/my-products - Meus produtos
PUT    /products/{id}     - Atualizar
DELETE /products/{id}     - Deletar
```

### Pedidos
```
POST   /orders            - Criar pedido
GET    /orders            - Meus pedidos
GET    /orders/{id}       - Ver pedido
PATCH  /orders/{id}/status - Atualizar status
POST   /orders/{id}/cancel - Cancelar
```

## 🔒 Segurança Implementada

✅ **Passwords**: Hashing com bcrypt (não plaintext)  
✅ **JWT**: Token Bearer com expiração configurável  
✅ **SQL Injection**: Protegido por ORM (SQLAlchemy)  
✅ **CORS**: Habilitado para desenvolvimento  
✅ **Validação**: Pydantic em todos os inputs  
✅ **Authorization**: Checagem de propriedade de recurso  

## 📊 Banco de Dados

### Tabelas
- `users` - Usuários do sistema
- `products` - Produtos à venda
- `orders` - Pedidos dos clientes
- `order_items` - Itens de cada pedido

### Relacionamentos
```
User (1) ──────→ (N) Product
User (1) ──────→ (N) Order
Order (1) ─────→ (N) OrderItem
Product (1) ───→ (N) OrderItem
```

## 🧪 Como Testar

### 1. Criar conta
```bash
curl -X POST http://localhost/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email":"user@example.com",
    "username":"usuario",
    "password":"Senha123!"
  }'
```

### 2. Fazer login
```bash
curl -X POST http://localhost/auth/login \
  -d "username=usuario&password=Senha123!"
```

### 3. Criar produto
```bash
curl -X POST http://localhost/products \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"iPhone","price":3000,"stock":10}'
```

### 4. Criar pedido
```bash
curl -X POST http://localhost/orders \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"product_id":1,"quantity":2}]}'
```

## 📈 Escalabilidade

O projeto é escalável para:
- ✅ Redis cache
- ✅ Fila de jobs (Celery)
- ✅ Elasticsearch
- ✅ Kubernetes
- ✅ Microserviços
- ✅ Load balancing

## 📚 Documentação Integrada

### OpenAPI
```
GET /openapi.json   - Especificação OpenAPI 3.0
GET /docs          - Swagger UI (interativo)
GET /redoc         - ReDoc (alternativo)
```

## 🔧 Desenvolvimento

### Adicionar Nova Rota

1. Crie função em `app/routes/`
2. Defina schema em `app/schemas/`
3. Implemente lógica em `app/services/`
4. Inclua em `app/main.py`

Exemplo:
```python
# routes/exemplo.py
@router.get("/exemplo")
async def meu_endpoint(db: Session = Depends(get_db)):
    return {"mensagem": "Olá"}
```

## 📝 Variáveis de Ambiente

```env
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=sua-chave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=Marketplace API
DEBUG=False
```

## ✨ Diferenciais

1. **Arquitetura Limpa** - Separação clara de responsabilidades
2. **Validação Robusta** - Pydantic em todos os inputs
3. **Segurança First** - JWT, bcrypt, SQL injection protection
4. **Containerização** - Docker + Compose prontos
5. **Documentação Completa** - 6 arquivos README
6. **DevOps Ready** - Healthchecks, reverse proxy
7. **Extensível** - Fácil de adicionar features
8. **Production Ready** - Erros tratados, logs, validation

## 🎓 Aprenda com este Projeto

- ✔ FastAPI moderno
- ✔ SQLAlchemy ORM
- ✔ JWT Authentication
- ✔ Docker & Compose
- ✔ Nginx configuration
- ✔ PostgreSQL relational
- ✔ RESTful APIs
- ✔ Clean architecture

## 🚀 Próximos Passos

1. **Rodou localmente?** Execute `docker-compose up -d`
2. **Explorou a API?** Acesse `/docs`
3. **Criou uma conta?** Teste os endpoints
4. **Quer customizar?** Edite `app/` conforme necessário

## 📞 Suporte

- Erro? Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Como usar? Leia [GUIA_USO.md](GUIA_USO.md)
- Entender arquitetura? Estude [ARQUITETURA.md](ARQUITETURA.md)

---

**Desenvolvido com ❤️ como referência profissional de Backend + API REST**

**Stack: Python • FastAPI • PostgreSQL • Docker • Nginx • JWT**
