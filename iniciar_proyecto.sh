#!/bin/bash
# Script de Inicialización para Linux/Mac

echo "==============================================="
echo "  Sistema de Gestión de Prácticas"
echo "  Script de Inicialización"
echo "==============================================="
echo ""

# Verificar Python
echo "[1/8] Verificando Python..."
if command -v python3 &> /dev/null; then
    echo "✓ $(python3 --version)"
else
    echo "✗ Python no encontrado. Por favor instala Python 3.12+"
    exit 1
fi

# Crear entorno virtual
echo ""
echo "[2/8] Creando entorno virtual..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Entorno virtual creado"
else
    echo "✓ Entorno virtual ya existe"
fi

# Activar entorno virtual
echo ""
echo "[3/8] Activando entorno virtual..."
source .venv/bin/activate
echo "✓ Entorno virtual activado"

# Instalar dependencias
echo ""
echo "[4/8] Instalando dependencias..."
pip install -r requirements.txt --quiet
echo "✓ Dependencias instaladas"

# Crear directorios
echo ""
echo "[5/8] Creando directorios necesarios..."
mkdir -p media/hojas_vida staticfiles static/css static/js
echo "✓ Directorios creados"

# Aplicar migraciones
echo ""
echo "[6/8] Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate
echo "✓ Migraciones aplicadas"

# Recolectar estáticos
echo ""
echo "[7/8] Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear
echo "✓ Archivos estáticos recolectados"

# Crear usuarios
echo ""
echo "[8/8] Creando usuarios de prueba..."
if [ -f "crear_usuarios_simple.py" ]; then
    python crear_usuarios_simple.py
    echo "✓ Usuarios creados"
fi

# Resumen
echo ""
echo "==============================================="
echo "  ✓ Inicialización Completa"
echo "==============================================="
echo ""
echo "Usuarios disponibles:"
echo "  Coordinador: coordinador / 123456"
echo "  Estudiante:  ana_martinez / 123456"
echo "  Docente:     dr_garcia / 123456"
echo "  Instructor:  instructor_techcorp / 123456"
echo ""
echo "Para iniciar el servidor:"
echo "  python manage.py runserver"
echo ""
echo "Accede en: http://127.0.0.1:8000/login/"
echo ""

