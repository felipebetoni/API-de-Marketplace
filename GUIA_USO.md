# Guia de Uso da API

## 🎯 Fluxo Básico

### 1. Criar Conta

```bash
curl -X POST http://localhost/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "seller@example.com",
    "username": "seller123",
    "full_name": "João Vendedor",
    "password": "SenhaSegura123!"
  }'
```

Resposta:
```json
{
  "id": 1,
  "email": "seller@example.com",
  "username": "seller123",
  "full_name": "João Vendedor",
  "is_active": true,
  "created_at": "2024-12-28T10:30:00"
}
```

### 2. Fazer Login

```bash
curl -X POST http://localhost/auth/login \
  -d "username=seller123&password=SenhaSegura123!"
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Salve o `access_token` para usar em requests autenticados!**

### 3. Criar Produtos (como vendedor)

```bash
curl -X POST http://localhost/products \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop Dell XPS",
    "description": "Laptop de alta performance",
    "price": 2500.00,
    "stock": 10
  }'
```

### 4. Listar Produtos

```bash
curl http://localhost/products?skip=0&limit=20
```

### 5. Criar Pedido (como comprador)

Primeiro, crie outra conta para ser comprador:

```bash
curl -X POST http://localhost/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "buyer@example.com",
    "username": "buyer456",
    "full_name": "Maria Compradora",
    "password": "SenhaSegura456!"
  }'
```

Faça login e crie um pedido:

```bash
curl -X POST http://localhost/orders \
  -H "Authorization: Bearer SEU_TOKEN_COMPRADOR" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      }
    ]
  }'
```

### 6. Acompanhar Pedido

```bash
curl http://localhost/orders \
  -H "Authorization: Bearer SEU_TOKEN_COMPRADOR"
```

## 🔑 Padrão de Autenticação

Todos os endpoints protegidos requerem o header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## ✅ Validações Importantes

### Usuários
- **Email**: Deve ser válido
- **Username**: Mínimo 3 caracteres, único
- **Password**: Mínimo 8 caracteres
- **Full name**: Opcional

### Produtos
- **Name**: Obrigatório, mínimo 1 caractere
- **Price**: Obrigatório, deve ser > 0
- **Stock**: Padrão 0, deve ser >= 0
- **Description**: Opcional

### Pedidos
- **Quantity**: Deve ser > 0
- **Stock disponível**: Sistema valida automaticamente
- **Status válidos**: pending, processing, shipped, delivered, cancelled

## 🚨 Códigos de Erro Comuns

| Código | Significado | Solução |
|--------|------------|---------|
| 400 | Dados inválidos | Verificar validação |
| 401 | Token inválido/expirado | Fazer login novamente |
| 403 | Não autorizado | Recurso pertence a outro usuário |
| 404 | Não encontrado | Verificar IDs |
| 422 | Validação falhou | Verificar formato dos dados |

## 💡 Exemplos Avançados

### Buscar Meus Produtos

```bash
curl http://localhost/products/my-products \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Atualizar Produto

```bash
curl -X PUT http://localhost/products/1 \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 2800.00,
    "stock": 15
  }'
```

### Cancelar Pedido (se status for pending)

```bash
curl -X POST http://localhost/orders/1/cancel \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Atualizar Status do Pedido

```bash
curl -X PATCH http://localhost/orders/1/status \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped"
  }'
```

## 📊 Verificação de Saúde

```bash
curl http://localhost/health
```

Resposta:
```json
{
  "status": "healthy"
}
```

## 📖 Documentação Interativa

Acesse `http://localhost/docs` ou `http://localhost:8000/docs` para testar todos os endpoints visualmente!
