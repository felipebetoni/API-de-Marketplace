# Exemplos de Requests

## Baseado em cURL

Você pode copiar e colar estes comandos no terminal.

### 1️⃣ REGISTRO E AUTENTICAÇÃO

```bash
# Registrar novo usuário (vendedor)
curl -X POST http://localhost/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "vendedor@example.com",
    "username": "vendedor123",
    "full_name": "João Silva",
    "password": "Senha123!@#"
  }'

# Resposta:
# {
#   "id": 1,
#   "email": "vendedor@example.com",
#   "username": "vendedor123",
#   "full_name": "João Silva",
#   "is_active": true,
#   "created_at": "2024-12-28T10:30:00"
# }

# Fazer login
curl -X POST http://localhost/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=vendedor123&password=Senha123!@#"

# Resposta:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer"
# }

# SALVE O TOKEN PARA USAR NOS PRÓXIMOS COMANDOS
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 2️⃣ USUÁRIOS

```bash
# Obter dados do usuário atual
curl http://localhost/users/me \
  -H "Authorization: Bearer $TOKEN"

# Obter dados de um usuário específico
curl http://localhost/users/1
```

### 3️⃣ PRODUTOS (CRUD)

```bash
# CRIAR novo produto
curl -X POST http://localhost/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15 Pro",
    "description": "Smartphone Apple com 256GB de armazenamento",
    "price": 4999.99,
    "stock": 50
  }'

# Resposta:
# {
#   "id": 1,
#   "name": "iPhone 15 Pro",
#   "description": "Smartphone Apple com 256GB de armazenamento",
#   "price": 4999.99,
#   "stock": 50,
#   "seller_id": 1,
#   "is_active": true,
#   "created_at": "2024-12-28T10:35:00"
# }

# LISTAR todos os produtos
curl http://localhost/products

# Listar com paginação
curl "http://localhost/products?skip=0&limit=20"

# Obter um produto específico
curl http://localhost/products/1

# LISTAR meus produtos
curl http://localhost/products/my-products \
  -H "Authorization: Bearer $TOKEN"

# ATUALIZAR um produto
curl -X PUT http://localhost/products/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 4799.99,
    "stock": 45
  }'

# DELETAR um produto
curl -X DELETE http://localhost/products/1 \
  -H "Authorization: Bearer $TOKEN"
```

### 4️⃣ PEDIDOS (CRUD)

```bash
# Primeiro, registre e faça login como comprador
curl -X POST http://localhost/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "comprador@example.com",
    "username": "comprador456",
    "full_name": "Maria Santos",
    "password": "Senha456!@#"
  }'

curl -X POST http://localhost/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=comprador456&password=Senha456!@#"

# SALVE O TOKEN DO COMPRADOR
export BUYER_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# CRIAR novo pedido
curl -X POST http://localhost/orders \
  -H "Authorization: Bearer $BUYER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      }
    ]
  }'

# Resposta:
# {
#   "id": 1,
#   "buyer_id": 2,
#   "total_amount": 9999.98,
#   "status": "pending",
#   "items": [
#     {
#       "id": 1,
#       "product_id": 1,
#       "quantity": 2,
#       "price": 4999.99,
#       "created_at": "2024-12-28T10:40:00"
#     }
#   ],
#   "created_at": "2024-12-28T10:40:00"
# }

# LISTAR meus pedidos
curl http://localhost/orders \
  -H "Authorization: Bearer $BUYER_TOKEN"

# Obter um pedido específico
curl http://localhost/orders/1 \
  -H "Authorization: Bearer $BUYER_TOKEN"

# ATUALIZAR status do pedido (vendedor/admin)
curl -X PATCH http://localhost/orders/1/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "processing"
  }'

# Mudar para enviado
curl -X PATCH http://localhost/orders/1/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped"
  }'

# Marcar como entregue
curl -X PATCH http://localhost/orders/1/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "delivered"
  }'

# CANCELAR um pedido (só funciona se status = pending)
curl -X POST http://localhost/orders/1/cancel \
  -H "Authorization: Bearer $BUYER_TOKEN"
```

### 5️⃣ HEALTH CHECK

```bash
# Verificar se a API está funcionando
curl http://localhost/health

# Resposta: {"status": "healthy"}
```

## 🧪 Testando com Insomnia/Postman

### Passo 1: Importar Variáveis

```
Base URL: http://localhost
Token: {{token}}
BuyerToken: {{buyer_token}}
```

### Passo 2: Criar Requests

1. **POST** `{{Base URL}}/auth/register`
   - Body: JSON com email, username, full_name, password

2. **POST** `{{Base URL}}/auth/login`
   - Body: form-data com username e password
   - Salve response.access_token como {{token}}

3. **GET** `{{Base URL}}/products`
   - Sem autenticação

4. **POST** `{{Base URL}}/products`
   - Header: `Authorization: Bearer {{token}}`
   - Body: JSON com product details

5. **POST** `{{Base URL}}/orders`
   - Header: `Authorization: Bearer {{buyer_token}}`
   - Body: JSON com items array

## 📝 Notas

- Substitua `localhost` por seu servidor em produção
- Tokens JWT expiram em 30 minutos (configurável)
- Use HTTPS em produção
- Nunca compartilhe seus tokens
- Senhas precisam ter pelo menos 8 caracteres
