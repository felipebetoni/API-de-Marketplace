# Problemas Comuns e Soluções

## 🐳 Problemas com Docker

### Erro: "Cannot connect to Docker daemon"
```bash
# Solução: Inicie o Docker Desktop ou daemon
# Windows/Mac: Abra Docker Desktop
# Linux: sudo systemctl start docker
```

### Erro: "Port 5432 already in use"
```bash
# Solução 1: Use uma porta diferente
# Edite docker-compose.yml:
services:
  db:
    ports:
      - "5433:5432"  # Mudou de 5432 para 5433

# Solução 2: Mate o processo
docker ps | grep 5432
docker stop <container-id>
```

### Erro: "Connection refused" ao conectar no PostgreSQL
```bash
# Solução: Aguarde o container ficar pronto
docker-compose logs db

# Ou use health check:
docker-compose up -d
sleep 15  # Aguarde 15 segundos
```

### Erro: "Out of memory"
```bash
# Limpe imagens não usadas
docker system prune -a

# Remova volumes
docker volume prune
```

## 🐍 Problemas com Python

### Erro: "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Solução: Instale as dependências
pip install -r requirements.txt

# Ou use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Erro: "No such file or directory: '.env'"
```bash
# Solução: Crie o arquivo .env
cp .env.example .env
# Ou crie manualmente com as variáveis necessárias
```

### Erro: "jwt.exceptions.JWTError"
```bash
# Solução: Token expirado ou inválido
# Faça login novamente para obter novo token

# Ou aumente o tempo de expiração em .env:
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

## 📊 Problemas com Banco de Dados

### Erro: "UNIQUE constraint failed: users.email"
```python
# Solução: Email já existe
# Use outro email ou delete o usuário

# Limpar banco (dev only):
docker-compose down -v
docker-compose up -d
```

### Erro: "Relation 'products' does not exist"
```bash
# Solução: Tabelas não foram criadas
# Reinicie a API:
docker-compose restart api

# Ou manualmente:
docker-compose down
docker-compose up -d
```

### Erro: "foreign key constraint failed"
```python
# Solução: Você está deletando um usuário que tem produtos
# Delete os produtos primeiro:
DELETE FROM products WHERE seller_id = 1
DELETE FROM users WHERE id = 1
```

## 🔐 Problemas com Autenticação

### Erro: "Invalid authentication credentials"
```bash
# Solução 1: Token inválido ou expirado
# Faça login novamente

# Solução 2: Token não foi enviado corretamente
# Verifique o header:
Authorization: Bearer seu_token_aqui  # Correto
Authorization: seu_token_aqui  # ❌ Errado
```

### Erro: "User not found"
```bash
# Solução: Usuário foi deletado
# Crie uma nova conta

# Ou verifique o user_id no token:
# Decodifique o JWT em jwt.io
```

### Erro: "User is inactive"
```bash
# Solução: Usuário foi desativado
# Reative manualmente no banco:
UPDATE users SET is_active = true WHERE id = 1
```

## 📮 Problemas com Requests

### Erro 400: "Invalid request body"
```json
// ❌ Errado
{
  "name": "Produto",
  "price": -100,  // Preço negativo
  "stock": -5     // Stock negativo
}

// ✅ Correto
{
  "name": "Produto",
  "price": 99.99,
  "stock": 10
}
```

### Erro 422: "Validation error"
```bash
# Verificar resposta detalhada:
curl -v http://localhost/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'

# A resposta mostrará exatamente qual campo está errado
```

### Erro 404: "Not found"
```bash
# Solução: ID não existe
# Verifique o ID correto:
curl http://localhost/products
# Use um product_id que existe
```

### Erro 403: "Not authorized"
```bash
# Solução: Você não é o dono do recurso
# Exemplo: Tentando editar produto de outro vendedor

# Verifique permissões:
GET /products/my-products  # Veja seus produtos
PUT /products/1  # Tente editar
```

## 🌐 Problemas com Nginx

### Erro: "502 Bad Gateway"
```bash
# Solução: API não está respondendo
docker-compose logs api

# Reinicie a API:
docker-compose restart api
```

### Erro: "Connection timeout"
```bash
# Solução: Aumente timeout no nginx
# nginx/conf.d/default.conf:
proxy_connect_timeout 120s;  # Mudou de 60s

# Reinicie nginx:
docker-compose restart nginx
```

## 💾 Problemas com Dados

### Recuperar Dados Depois de docker-compose down

```bash
# Se usou -v (remove volumes):
# ❌ Todos os dados foram deletados

# Se não usou -v:
# ✅ Dados persistem
docker-compose up -d
# Banco retorna aos dados anteriores
```

### Reset Completo do Banco

```bash
# Remove tudo
docker-compose down -v

# Inicia fresh
docker-compose up -d
```

## 🔍 Debug

### Ver Logs Detalhados

```bash
# API
docker-compose logs -f api

# Banco
docker-compose logs -f db

# Nginx
docker-compose logs -f nginx

# Tudo
docker-compose logs -f
```

### Executar Comandos no Container

```bash
# Shell da API
docker-compose exec api bash

# Shell do Banco
docker-compose exec db bash

# Query SQL
docker-compose exec db psql -U marketplace_user -d marketplace_db
```

### Inspeção de Container

```bash
# Ver recursos usados
docker stats

# Ver portas mapeadas
docker-compose ps

# Ver variáveis de ambiente
docker-compose exec api env
```

## ✅ Checklist de Troubleshooting

- [ ] Docker está rodando?
- [ ] Portas estão disponíveis?
- [ ] Arquivo `.env` existe?
- [ ] Token está válido?
- [ ] IDs dos recursos existem?
- [ ] Você tem permissão para acessar?
- [ ] Dados estão em formato correto?
- [ ] Banco está conectado?

## 📞 Obtendo Ajuda

1. Verifique os logs: `docker-compose logs`
2. Reinicie tudo: `docker-compose restart`
3. Reset completo: `docker-compose down -v && docker-compose up -d`
4. Decodifique JWT: https://jwt.io
5. Valide JSON: https://jsonlint.com
