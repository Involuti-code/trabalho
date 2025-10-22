@echo off
title Sistema Administrativo - N2
echo ========================================
echo    SISTEMA ADMINISTRATIVO - N2
echo ========================================
echo.

REM Verifica se o Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo.
    echo Por favor, instale o Python primeiro:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python encontrado. Verificando dependencias...
echo.

REM Verifica se as dependencias estao instaladas
python -c "import PyPDF2" >nul 2>&1
if %errorlevel% neq 0 (
    echo Dependencias nao encontradas. Instalando...
    call install_dependencies.bat
    if %errorlevel% neq 0 (
        echo Erro ao instalar dependencias!
        pause
        exit /b 1
    )
)

echo.
echo Executando teste do sistema...
python teste_sistema.py

echo.
echo ========================================
echo.
echo Escolha uma opcao:
echo 1. Executar Sistema Django
echo 2. Executar API Flask
echo 3. Configurar banco de dados
echo 4. Executar migrações
echo 5. Criar superusuário
echo 6. Executar testes
echo 7. Sair
echo.
set /p opcao="Digite sua opcao (1-7): "

if "%opcao%"=="1" (
    echo.
    echo Iniciando Sistema Django...
    cd app
    python manage.py runserver
) else if "%opcao%"=="2" (
    echo.
    echo Iniciando API Flask...
    cd app
    python flask_api.py
) else if "%opcao%"=="3" (
    echo.
    echo Configurando banco de dados...
    cd app
    python setup_database.py
    pause
) else if "%opcao%"=="4" (
    echo.
    echo Executando migrações...
    cd app
    python manage.py migrate
    pause
) else if "%opcao%"=="5" (
    echo.
    echo Criando superusuário...
    cd app
    python manage.py createsuperuser
    pause
) else if "%opcao%"=="6" (
    echo.
    echo Executando testes...
    cd app
    python manage.py test
    pause
) else if "%opcao%"=="7" (
    echo.
    echo Saindo...
    exit /b 0
) else (
    echo.
    echo Opcao invalida!
    pause
)

echo.
echo Sistema finalizado.
pause

