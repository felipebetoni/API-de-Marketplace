# ⚡ Quick Reference - Guia Rápido

## 🚀 Iniciar em 3 Passos

```bash
# 1. Entre na pasta
cd "API de Marketplace"

# 2. Inicie Docker
docker-compose up -d

# 3. Acesse
# API: http://localhost
# Docs: http://localhost/docs
```

## 📍 URLs Importantes

| Recurso | URL |
|---------|-----|
| **API** | http://localhost |
| **Swagger Docs** | http://localhost/docs |
| **ReDoc** | http://localhost/redoc |
| **Health Check** | http://localhost/health |
| **PostgreSQL** | localhost:5432 |

## 🔑 Usuário de Teste

```json
{
  "email": "teste@example.com",
  "username": "testuser",
  "password": "TestPass123!"
}
```

## 📝 Fluxo Básico (cURL)

### 1️⃣ Registrar
```bash
curl -X POST http://localhost/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email":"seu@email.com",
    "username":"seuuser",
    "password":"Senha123!"
  }'
```

### 2️⃣ Login
```bash
curl -X POST http://localhost/auth/login \
  -d "username=seuuser&password=Senha123!"
```

**Copie o `access_token` da resposta →** `TOKEN="seu_token_aqui"`

### 3️⃣ Criar Produto
```bash
curl -X POST http://localhost/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"iPhone 15",
    "description":"Smartphone",
    "price":3999,
    "stock":10
  }'
```

### 4️⃣ Listar Produtos
```bash
curl http://localhost/products
```

### 5️⃣ Criar Pedido
```bash
curl -X POST http://localhost/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{"product_id":1,"quantity":2}]
  }'
```

## 🛑 Comandos Docker

```bash
# Iniciar
docker-compose up -d

# Parar
docker-compose down

# Ver logs
docker-compose logs -f api

# Resetar banco
docker-compose down -v

# Executar comando
docker-compose exec api bash
```

## 📋 Endpoints Essenciais

### Auth
- `POST /auth/register` - Criar conta
- `POST /auth/login` - Fazer login

### Users
- `GET /users/me` - Meu perfil
- `GET /users/{id}` - Perfil de alguém

### Products
- `POST /products` - Criar
- `GET /products` - Listar
- `GET /products/my-products` - Meus
- `PUT /products/{id}` - Atualizar
- `DELETE /products/{id}` - Deletar

### Orders
- `POST /orders` - Criar
- `GET /orders` - Listar meus
- `GET /orders/{id}` - Ver detalhes
- `PATCH /orders/{id}/status` - Mudar status
- `POST /orders/{id}/cancel` - Cancelar

## 🔒 Header de Autenticação

Todos os endpoints autenticados precisam do header:

```
Authorization: Bearer seu_token_jwt_aqui
```

## ✅ Validation Rules

| Campo | Regra |
|-------|-------|
| **Email** | Válido + único |
| **Username** | 3-50 caracteres + único |
| **Password** | Mínimo 8 caracteres |
| **Price** | Maior que 0 |
| **Stock** | Maior ou igual a 0 |
| **Quantity** | Maior que 0 |

## 🚨 Status Codes

| Código | Significado |
|--------|------------|
| `200` | OK |
| `201` | Criado |
| `204` | Sem conteúdo |
| `400` | Bad request |
| `401` | Não autenticado |
| `403` | Não autorizado |
| `404` | Não encontrado |
| `422` | Validação falhou |

## 🐳 Arquitetura

```
┌─ Cliente (Browser/cURL/Postman)
└─ Nginx (porta 80)
   └─ FastAPI (porta 8000)
      └─ PostgreSQL (porta 5432)
```

## 📦 Stack

```
Python 3.11
├─ FastAPI (web framework)
├─ SQLAlchemy (ORM)
├─ PostgreSQL (database)
├─ JWT (autenticação)
├─ Pydantic (validação)
└─ Docker (containerização)
```

## 💡 Dicas

### 💾 Copiar um Token
```bash
# No response do login, copie o access_token inteiro
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 🔍 Decodificar JWT
```bash
# Acesse https://jwt.io e cole seu token para ver dados
```

### 📊 Ver Banco
```bash
# Acesse o banco manualmente:
docker-compose exec db psql -U marketplace_user -d marketplace_db

# Exemplos de queries:
SELECT * FROM users;
SELECT * FROM products;
SELECT * FROM orders;
```

### 🔄 Resetar Tudo
```bash
docker-compose down -v
docker-compose up -d
# Banco limpo, pronto para novos testes
```

## 📚 Documentos Relacionados

| Arquivo | Para quê? |
|---------|-----------|
| [README.md](README.md) | Visão geral completa |
| [GUIA_USO.md](GUIA_USO.md) | Exemplos de uso |
| [ARQUITETURA.md](ARQUITETURA.md) | Entender design |
| [INSTALACAO_LOCAL.md](INSTALACAO_LOCAL.md) | Sem Docker |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Problemas |
| [EXEMPLOS_REQUESTS.md](EXEMPLOS_REQUESTS.md) | Mais exemplos |

## 🎯 Workflow Típico

```
1. docker-compose up -d     → Inicia API
2. POST /auth/register       → Cria usuário
3. POST /auth/login         → Obtém token
4. POST /products           → Cria produtos
5. GET /products            → Lista produtos
6. POST /orders             → Faz pedido
7. GET /orders              → Acompanha pedido
```

## ⚠️ Erros Comuns

| Erro | Solução |
|------|---------|
| Porta em uso | `docker ps` e veja qual container |
| Banco não conecta | `docker-compose logs db` |
| Token inválido | Faça login novamente |
| 404 Not Found | Verifique o ID do recurso |
| 403 Forbidden | Você não é o dono |

## 🆘 Ajuda Rápida

**Problema?**
1. Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Check logs: `docker-compose logs`
3. Reset: `docker-compose down -v`

**Não funciona?**
1. Docker está rodando?
2. Portas disponíveis?
3. `.env` configurado?

---

**Pronto para começar? Execute:** `docker-compose up -d`

**Explorar API? Acesse:** http://localhost/docs
