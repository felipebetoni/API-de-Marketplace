# Estrutura do Projeto

## 📁 Diretórios

```
API de Marketplace/
├── app/                          # Código principal da aplicação
│   ├── __init__.py              # Pacote Python
│   ├── main.py                  # Aplicação FastAPI
│   │
│   ├── core/                    # Configurações e utilitários
│   │   ├── __init__.py
│   │   ├── config.py            # Configurações (variáveis de ambiente)
│   │   ├── security.py          # JWT, hash de senhas, segurança
│   │   └── database.py          # Conexão com PostgreSQL
│   │
│   ├── models/                  # Modelos SQLAlchemy (banco de dados)
│   │   ├── __init__.py          # User, Product, Order, OrderItem
│   │   └── models.py            # (vazio - imports centralizados)
│   │
│   ├── schemas/                 # Schemas Pydantic (validação)
│   │   ├── __init__.py          # Modelos de request/response
│   │   └── schemas.py           # (vazio - imports centralizados)
│   │
│   ├── routes/                  # Rotas FastAPI (endpoints)
│   │   ├── __init__.py
│   │   ├── auth.py              # POST /auth/register, /auth/login
│   │   ├── users.py             # GET /users/me, /users/{id}
│   │   ├── products.py          # CRUD de produtos
│   │   └── orders.py            # CRUD de pedidos
│   │
│   ├── services/                # Lógica de negócio
│   │   ├── __init__.py
│   │   └── crud.py              # Funções CRUD (Create, Read, Update, Delete)
│   │
│   └── dependencies/            # Dependências FastAPI
│       ├── __init__.py
│       └── auth.py              # get_current_user (middleware)
│
├── nginx/                       # Configuração Nginx
│   ├── nginx.conf              # Configuração principal
│   └── conf.d/
│       └── default.conf        # Virtual host padrão
│
├── .env                         # Variáveis de ambiente (não comitar)
├── .env.example                 # Template do .env
├── .gitignore                   # Arquivos ignorados pelo git
├── requirements.txt             # Dependências Python
├── Dockerfile                   # Imagem Docker da API
├── docker-compose.yml           # Orquestração de containers
├── README.md                    # Documentação principal
├── GUIA_USO.md                 # Guia prático de uso
└── ARQUITETURA.md              # Este arquivo

```

## 🔄 Fluxo de Dados

```
Request HTTP
    ↓
FastAPI Router (routes/)
    ↓
Validação Pydantic (schemas/)
    ↓
Autenticação JWT (dependencies/auth.py)
    ↓
Lógica de Negócio (services/crud.py)
    ↓
SQLAlchemy ORM (models/)
    ↓
PostgreSQL Database
    ↓
Response JSON
```

## 📦 Dependências

### Principais
- **fastapi**: Framework web assíncrono
- **uvicorn**: Servidor ASGI
- **sqlalchemy**: ORM para banco de dados
- **psycopg2-binary**: Driver PostgreSQL
- **pydantic**: Validação de dados
- **python-jose**: JWT (tokens)
- **passlib**: Hashing de senhas
- **python-multipart**: Suporte a form data

## 🎯 Padrões de Design

### Arquitetura em Camadas
```
Presentation Layer (routes/)
    ↓
Business Logic Layer (services/)
    ↓
Data Access Layer (models/)
    ↓
Database (PostgreSQL)
```

### Injeção de Dependências
FastAPI usa injeção automática:
```python
async def my_endpoint(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    pass
```

### Soft Deletes
Produtos e usuários usam `is_active` em vez de deletar fisicamente:
```python
product.is_active = False  # Soft delete
db.commit()
```

## 🔐 Fluxo de Autenticação

```
1. User Registration
   POST /auth/register → create_user() → User criado

2. User Login
   POST /auth/login → authenticate_user() → JWT token

3. Protected Request
   GET /users/me com "Authorization: Bearer {token}"
   → verify_token() → get_current_user() → ✓ Acesso concedido
```

## 💾 Operações CRUD

### Create (Criar)
```python
# Exemplo: Criar produto
POST /products
→ create_product(db, product, seller_id)
→ INSERT INTO products VALUES(...)
```

### Read (Ler)
```python
# Exemplo: Listar produtos
GET /products
→ get_all_products(db, skip, limit)
→ SELECT * FROM products WHERE is_active = True
```

### Update (Atualizar)
```python
# Exemplo: Atualizar produto
PUT /products/{id}
→ update_product(db, id, product_update, seller_id)
→ UPDATE products SET ... WHERE id = ? AND seller_id = ?
```

### Delete (Deletar)
```python
# Exemplo: Deletar produto
DELETE /products/{id}
→ delete_product(db, id, seller_id)
→ UPDATE products SET is_active = False WHERE id = ?
```

## 🔗 Relacionamentos do Banco

```
User (1) ──────────→ (N) Product
User (1) ──────────→ (N) Order
Order (1) ─────────→ (N) OrderItem
Product (1) ───────→ (N) OrderItem
```

## 📊 Estados do Pedido

```
┌─────────┐
│ pending │  ← Estado inicial após criação
└────┬────┘
     │ Aceitar
     ↓
┌───────────┐
│processing │  ← Preparando para envio
└────┬──────┘
     │ Enviado
     ↓
┌─────────┐
│ shipped │  ← Em trânsito
└────┬────┘
     │ Entregue
     ↓
┌───────────┐
│ delivered │  ← Finalizado
└───────────┘

Cancelamento (de qualquer estado):
     │ Cancelar (se pending)
     ↓
┌───────────┐
│ cancelled │  ← Cancelado + estoque restaurado
└───────────┘
```

## 🧪 Estrutura de Testes (Exemplo)

```python
# tests/
├── test_auth.py
├── test_users.py
├── test_products.py
└── test_orders.py

# Exemplo:
def test_create_user():
    response = client.post("/auth/register", json={...})
    assert response.status_code == 201
```

## 🚀 Melhorias Potenciais

### Performance
- [ ] Redis cache para produtos
- [ ] Paginação com cursor
- [ ] Índices de banco de dados
- [ ] Query optimization

### Funcionalidades
- [ ] Sistema de avaliações
- [ ] Recomendações de produtos
- [ ] Histórico de atividades
- [ ] Notificações em tempo real (WebSockets)

### DevOps
- [ ] CI/CD com GitHub Actions
- [ ] Monitoring (Prometheus + Grafana)
- [ ] Logging centralizado (ELK)
- [ ] Backup automático

### Segurança
- [ ] Rate limiting
- [ ] 2FA (autenticação dupla)
- [ ] Auditoria de ações
- [ ] HTTPS obrigatório

## 📝 Convenções

### Nomenclatura
- `snake_case` para variáveis e funções
- `PascalCase` para classes
- `UPPER_CASE` para constantes

### Tipo de Arquivo
- `.py` - Python
- `.sql` - SQL
- `.env` - Variáveis de ambiente
- `.json` - Dados estruturados

### Commits Git
```
feat: adicionar novo recurso
fix: corrigir bug
docs: atualizar documentação
refactor: refatorar código
test: adicionar testes
```
