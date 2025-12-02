#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Iniciando build para Render..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p staticfiles
mkdir -p media/hojas_vida

# Recolectar archivos estáticos
echo "🎨 Recolectando archivos estáticos..."
python manage.py collectstatic --no-input --clear

# Aplicar migraciones
echo "🗄️  Aplicando migraciones de base de datos..."
python manage.py migrate --noinput

# Crear usuarios de prueba (opcional, comentar si no deseas)
echo "👥 Creando usuarios de prueba..."
python crear_usuarios_simple.py || echo "⚠️  Usuarios ya existen o error al crearlos"

echo "✅ Build completado exitosamente!"

