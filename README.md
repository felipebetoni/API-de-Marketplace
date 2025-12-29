# API de Marketplace

Uma API profissional de Marketplace desenvolvida com **Python + FastAPI**, demonstrando arquitetura limpa, validação robusta e APIs REST em padrão de produção.

## Funcionalidades

- **CRUD de Usuários** - Registro e gerenciamento de usuários com autenticação
- **CRUD de Produtos** - Criação e gerenciamento de produtos por vendedores
- **CRUD de Pedidos** - Criação e acompanhamento completo de pedidos
- **Autenticação JWT** - Tokens Bearer com expiração configurável
- **Validação Pydantic** - Validação robusta em todos os inputs
- **Banco PostgreSQL** - Armazenamento relacional e persistente
- **Docker & Docker Compose** - Containerização e orquestração
- **Nginx Reverse Proxy** - Balanceamento de carga e cache HTTP
- **Health Checks** - Monitoramento automático de serviços
- **Soft Deletes** - Preservação de dados com flag de ativo/inativo

## Arquitetura

```
app/
├── core/               # Configuração, segurança e banco de dados
│   ├── config.py      # Variáveis de ambiente
│   ├── security.py    # JWT e hash de senhas
│   └── database.py    # Conexão com PostgreSQL
├── models/            # Modelos SQLAlchemy
│   └── __init__.py    # User, Product, Order, OrderItem
├── schemas/           # Schemas Pydantic (validação)
│   └── __init__.py    # Request/Response models
├── routes/            # Rotas FastAPI
│   ├── auth.py        # Autenticação
│   ├── users.py       # Usuários
│   ├── products.py    # Produtos
│   └── orders.py      # Pedidos
├── services/          # Lógica de negócio
│   └── crud.py        # Operações CRUD
├── dependencies/      # Dependências FastAPI
│   └── auth.py        # Autenticação e autorização
└── main.py            # Aplicação principal
```

## Como Começar

### Pré-requisitos

Para executar este projeto, você precisará de:

- Docker e Docker Compose instalados (recomendado)
- OU Python 3.11+ com PostgreSQL (para desenvolvimento local)

### Opção 1: Com Docker (Recomendado)

A maneira mais rápida de começar é usar Docker:

```bash
# Navegue até o diretório do projeto
cd "API de Marketplace"

# Inicie todos os serviços
docker-compose up -d

# A aplicação estará disponível em:
# http://localhost

# Documentação interativa em:
# http://localhost/docs
```

Aguarde cerca de 10 segundos para o PostgreSQL inicializar completamente.

### Opção 2: Instalação Local

Para desenvolvimento sem Docker:

```bash
# Crie um ambiente virtual Python
python -m venv venv

# Ative o ambiente virtual
source venv/bin/activate          # Linux/Mac
# ou
venv\Scripts\activate              # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
# Copie .env.example para .env e edite com suas configurações
cp .env.example .env

# Inicie o servidor de desenvolvimento
uvicorn app.main:app --reload
```

## Documentação da API

### Autenticação

**Registrar novo usuário**
```bash
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "usuario",
  "full_name": "Seu Nome",
  "password": "senha_segura_123"
}
```

**Fazer login**
```bash
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=usuario&password=senha_segura_123
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Usuários

**Obter dados do usuário atual**
```bash
GET /users/me
Authorization: Bearer {access_token}
```

**Obter dados de um usuário**
```bash
GET /users/{user_id}
```

### Produtos

**Listar todos os produtos**
```bash
GET /products?skip=0&limit=10
```

**Criar novo produto** (requer autenticação)
```bash
POST /products
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Produto XYZ",
  "description": "Descrição do produto",
  "price": 99.99,
  "stock": 50
}
```

**Obter meus produtos**
```bash
GET /products/my-products
Authorization: Bearer {access_token}
```

**Atualizar produto**
```bash
PUT /products/{product_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Novo nome",
  "price": 129.99,
  "stock": 30
}
```

**Deletar produto** (soft delete - desativa)
```bash
DELETE /products/{product_id}
Authorization: Bearer {access_token}
```

### Pedidos

**Criar novo pedido**
```bash
POST /orders
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 1
    }
  ]
}
```

**Listar meus pedidos**
```bash
GET /orders?skip=0&limit=10
Authorization: Bearer {access_token}
```

**Obter detalhes do pedido**
```bash
GET /orders/{order_id}
Authorization: Bearer {access_token}
```

**Atualizar status do pedido**
```bash
PATCH /orders/{order_id}/status
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "processing"
}
```

Status válidos: `pending`, `processing`, `shipped`, `delivered`, `cancelled`

**Cancelar pedido** (só funciona se status == pending)
```bash
POST /orders/{order_id}/cancel
Authorization: Bearer {access_token}
```

## Segurança

A aplicação implementa as seguintes medidas de segurança:

- **Passwords**: Hashing com bcrypt via passlib (nunca armazenadas em plaintext)
- **JWT**: Tokens Bearer com expiração configurável (padrão: 30 minutos)
- **CORS**: Habilitado para desenvolvimento, configurável para produção
- **Validação**: Todas as entradas validadas com Pydantic
- **SQL Injection**: Protegido através do ORM SQLAlchemy
- **Authorization**: Verificação de propriedade de recursos em todos os endpoints

## Banco de Dados

O projeto utiliza PostgreSQL 15 com quatro tabelas relacionadas:

### Tabela users

Armazena informações de usuários do sistema:

```sql
- id (chave primária)
- email (único)
- username (único)
- hashed_password
- full_name
- is_active
- created_at
- updated_at
```

### Tabela products

Armazena produtos cadastrados por vendedores:

```sql
- id (chave primária)
- name
- description
- price
- stock
- seller_id (chave estrangeira -> users)
- is_active
- created_at
- updated_at
```

### Tabela orders

Armazena pedidos dos compradores:

```sql
- id (chave primária)
- buyer_id (chave estrangeira -> users)
- total_amount
- status (pending, processing, shipped, delivered, cancelled)
- created_at
- updated_at
```

### Tabela order_items

Armazena itens individuais de cada pedido:

```sql
- id (chave primária)
- order_id (chave estrangeira -> orders)
- product_id (chave estrangeira -> products)
- quantity
- price (preço no momento da compra)
- created_at
```

## Docker

### Serviços inclusos

A aplicação é orquestrada através de três serviços:

| Serviço | Imagem | Porta | Descrição |
|---------|--------|-------|-----------|
| API | python:3.11 | 8000 | Servidor FastAPI |
| PostgreSQL | postgres:15-alpine | 5432 | Banco de dados |
| Nginx | nginx:alpine | 80 | Reverse proxy |

### Comandos úteis

```bash
# Iniciar serviços em background
docker-compose up -d

# Visualizar logs em tempo real
docker-compose logs -f api

# Parar todos os serviços
docker-compose down

# Remover volumes (reseta banco de dados)
docker-compose down -v

# Acessar shell do container da API
docker-compose exec api bash

# Acessar shell do PostgreSQL
docker-compose exec db psql -U marketplace_user -d marketplace_db
```

## Testando a API

### Com cURL

```bash
# Registrar um novo usuário
curl -X POST http://localhost/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "username":"testuser",
    "full_name":"Test User",
    "password":"password123"
  }'

# Fazer login e obter token
curl -X POST http://localhost/auth/login \
  -d "username=testuser&password=password123"

# Listar produtos
curl http://localhost/products
```

### Com Insomnia ou Postman

1. Acesse http://localhost/docs para a documentação Swagger UI interativa
2. Ou acesse http://localhost/redoc para a documentação ReDoc
3. Use a interface para testar todos os endpoints

## Funcionalidades Planejadas

Melhorias planejadas para versões futuras:

- [ ] Autenticação com OAuth2 (Google, GitHub)
- [ ] Página de checkout
- [ ] Integração com sistema de pagamentos (Stripe)
- [ ] Sistema de reviews e ratings
- [ ] Filtros avançados de produtos
- [ ] Notificações via email
- [ ] Testes automatizados (pytest)
- [ ] Integração contínua (GitHub Actions)
- [ ] Logs estruturados
- [ ] Rate limiting
- [ ] Monitoramento com Prometheus

## Variáveis de Ambiente

Configure o arquivo `.env` com as seguintes variáveis:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=Marketplace API
DEBUG=False
```

## Contribuindo

Contribuições são bem-vindas. Para contribuir:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.

## Suporte e Documentação

Para documentação completa e exemplos de uso, consulte os seguintes arquivos no repositório:

- `README.md` - Este arquivo
- `QUICK_REFERENCE.md` - Referência rápida de comandos
- `GUIA_USO.md` - Guia prático de uso
- `ARQUITETURA.md` - Arquitetura detalhada da aplicação
- `INSTALACAO_LOCAL.md` - Instruções para instalação local
- `TROUBLESHOOTING.md` - Solução de problemas comuns
- `EXEMPLOS_REQUESTS.md` - Exemplos de requisições