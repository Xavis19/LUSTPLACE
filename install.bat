@echo off
echo.
echo ===================================================
echo   🔥 MARKETPLACE LUST - INSTALADOR AUTOMATICO
echo ===================================================
echo.

echo 📋 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado. Descárgalo desde https://python.org
    pause
    exit /b 1
)
echo ✅ Python encontrado

echo.
echo 📦 Creando entorno virtual...
python -m venv .venv
if errorlevel 1 (
    echo ❌ Error creando entorno virtual
    pause
    exit /b 1
)
echo ✅ Entorno virtual creado

echo.
echo 🔧 Activando entorno virtual...
call .venv\Scripts\activate.bat

echo.
echo 📥 Instalando dependencias...
pip install --upgrade pip
pip install Django>=5.0,<6.0 Pillow>=10.0.0 python-decouple>=3.6 pytz>=2023.3
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)
echo ✅ Dependencias instaladas

echo.
echo 📋 Configurando variables de entorno...
if not exist .env (
    copy .env.example .env
    echo ✅ Archivo .env creado desde .env.example
) else (
    echo ℹ️  El archivo .env ya existe
)

echo.
echo 🗄️  Configurando base de datos...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo ❌ Error configurando base de datos
    pause
    exit /b 1
)
echo ✅ Base de datos configurada

echo.
echo 👤 ¿Deseas crear un superusuario? (s/n)
set /p crear_super=
if /i "%crear_super%"=="s" (
    python manage.py createsuperuser
)

echo.
echo ===================================================
echo   ✅ INSTALACION COMPLETADA EXITOSAMENTE
echo ===================================================
echo.
echo 🚀 Para ejecutar el servidor:
echo    1. Activa el entorno: .venv\Scripts\activate
echo    2. Ejecuta: python manage.py runserver
echo    3. Visita: http://127.0.0.1:8000
echo.
echo 📖 Para más información, lee el archivo README.md
echo.
pause