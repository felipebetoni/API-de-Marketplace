#!/bin/bash
# Script de inicialização rápida para Linux/Mac

set -e

echo "🚀 Iniciando API de Marketplace..."

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker não está instalado. Use INSTALACAO_LOCAL.md${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Docker Compose não está instalado.${NC}"
    exit 1
fi

# Verificar .env
if [ ! -f .env ]; then
    echo -e "${YELLOW}Criando arquivo .env...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ Arquivo .env criado${NC}"
fi

# Iniciar containers
echo -e "${YELLOW}Iniciando containers Docker...${NC}"
docker-compose up -d

# Aguardar banco ficar pronto
echo -e "${YELLOW}Aguardando banco de dados ficar pronto...${NC}"
sleep 10

# Verificar health
echo -e "${YELLOW}Verificando saúde da aplicação...${NC}"
for i in {1..30}; do
    if curl -s http://localhost/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ API está saudável!${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

echo ""
echo -e "${GREEN}✅ Tudo pronto!${NC}"
echo ""
echo "📚 Próximas ações:"
echo "   - API: http://localhost"
echo "   - Docs: http://localhost/docs"
echo "   - Logs: docker-compose logs -f"
echo "   - Parar: docker-compose down"
echo ""
echo "👉 Leia GUIA_USO.md para começar!"
