@echo off
REM Script de inicialização rápida para Windows

echo.
echo 🚀 Iniciando API de Marketplace...
echo.

REM Verificar Docker
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker não está instalado
    echo Use INSTALACAO_LOCAL.md
    exit /b 1
)

REM Verificar .env
if not exist .env (
    echo 📝 Criando arquivo .env...
    copy .env.example .env
    echo ✓ Arquivo .env criado
)

REM Iniciar containers
echo 🐳 Iniciando containers Docker...
docker-compose up -d

REM Aguardar banco ficar pronto
echo ⏳ Aguardando banco de dados ficar pronto...
timeout /t 10 /nobreak

REM Verificar health
echo 🔍 Verificando saúde da aplicação...
for /L %%i in (1,1,30) do (
    for /f %%A in ('curl -s http://localhost/health 2^>nul') do (
        if not "%%A"=="" (
            echo ✓ API está saudável!
            goto :ready
        )
    )
    timeout /t 1 /nobreak >nul
)

:ready
echo.
echo ✅ Tudo pronto!
echo.
echo 📚 Próximas ações:
echo    - API: http://localhost
echo    - Docs: http://localhost/docs
echo    - Logs: docker-compose logs -f
echo    - Parar: docker-compose down
echo.
echo 👉 Leia GUIA_USO.md para começar!
echo.
