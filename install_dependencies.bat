@echo off
echo Instalando dependencias do Python...
echo.

REM Verifica se o Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python nao encontrado. Por favor, instale o Python primeiro.
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado. Instalando dependencias...
echo.

REM Instala as dependencias
echo Instalando Django e dependencias principais...
pip install Django==4.2.7
pip install djangorestframework==3.14.0
pip install django-cors-headers==4.3.1
pip install django-environ==0.11.2
pip install django-filter==23.3

echo Instalando Flask para APIs...
pip install Flask==3.0.0
pip install Flask-CORS==4.0.0

echo Instalando PostgreSQL...
pip install psycopg2-binary==2.9.9
pip install django-extensions==3.2.3

echo Instalando processamento de PDF e IA...
pip install PyPDF2==3.0.1
pip install pdfplumber==0.10.3
pip install python-docx==1.1.0
pip install google-generativeai==0.3.2

echo Instalando utilitarios...
pip install Pillow==10.1.0
pip install requests==2.31.0
pip install python-decouple==3.8
pip install celery==5.3.4
pip install redis==5.0.1

echo Instalando ferramentas de desenvolvimento...
pip install pytest==7.4.3
pip install pytest-django==4.7.0
pip install factory-boy==3.3.0
pip install coverage==7.3.2

echo.
echo Dependencias instaladas com sucesso!
echo.
echo Agora voce pode executar o script extract_pdf_text.py
pause

