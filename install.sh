#!/bin/bash

echo ""
echo "==================================================="
echo "  🔥 MARKETPLACE LUST - INSTALADOR AUTOMATICO"
echo "==================================================="
echo ""

# Verificar Python
echo "📋 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Instálalo primero."
    exit 1
fi
echo "✅ Python encontrado: $(python3 --version)"

# Crear entorno virtual
echo ""
echo "📦 Creando entorno virtual..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "❌ Error creando entorno virtual"
    exit 1
fi
echo "✅ Entorno virtual creado"

# Activar entorno virtual
echo ""
echo "🔧 Activando entorno virtual..."
source .venv/bin/activate

# Instalar dependencias
echo ""
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install "Django>=5.0,<6.0" "Pillow>=10.0.0" "python-decouple>=3.6" "pytz>=2023.3"
if [ $? -ne 0 ]; then
    echo "❌ Error instalando dependencias"
    exit 1
fi
echo "✅ Dependencias instaladas"

# Configurar variables de entorno
echo ""
echo "📋 Configurando variables de entorno..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Archivo .env creado desde .env.example"
else
    echo "ℹ️  El archivo .env ya existe"
fi

# Configurar base de datos
echo ""
echo "🗄️  Configurando base de datos..."
python manage.py makemigrations
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ Error configurando base de datos"
    exit 1
fi
echo "✅ Base de datos configurada"

# Crear superusuario
echo ""
read -p "👤 ¿Deseas crear un superusuario? (s/n): " crear_super
if [[ $crear_super =~ ^[Ss]$ ]]; then
    python manage.py createsuperuser
fi

echo ""
echo "==================================================="
echo "   ✅ INSTALACION COMPLETADA EXITOSAMENTE"
echo "==================================================="
echo ""
echo "🚀 Para ejecutar el servidor:"
echo "   1. Activa el entorno: source .venv/bin/activate"
echo "   2. Ejecuta: python manage.py runserver"
echo "   3. Visita: http://127.0.0.1:8000"
echo ""
echo "📖 Para más información, lee el archivo README.md"
echo ""