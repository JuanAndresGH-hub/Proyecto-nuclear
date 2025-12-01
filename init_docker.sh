#!/bin/bash

# Script para inicializar la base de datos con datos de prueba en Docker

echo "🐳 Inicializando proyecto en Docker..."

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cp .env.example .env
fi

# Construir imágenes
echo "🔨 Construyendo imágenes Docker..."
docker-compose build

# Iniciar servicios
echo "🚀 Levantando servicios..."
docker-compose up -d

# Esperar a que la BD esté lista
echo "⏳ Esperando que PostgreSQL esté listo..."
sleep 10

# Ejecutar migraciones
echo "📦 Ejecutando migraciones..."
docker-compose exec -T web python manage.py migrate

# Crear superusuario si no existe
echo "👤 Creando usuarios de prueba..."
docker-compose exec -T web python manage.py shell < crear_usuarios_prueba.py || true

# Cargar datos de prueba
echo "📊 Cargando datos de prueba..."
docker-compose exec -T web python manage.py shell < cargar_datos_prueba.py || true

# Recolectar estáticos
echo "📁 Recolectando archivos estáticos..."
docker-compose exec -T web python manage.py collectstatic --noinput

echo "✅ ¡Setup completado!"
echo ""
echo "📱 Accede a la aplicación:"
echo "   URL: http://localhost:8000/login"
echo "   Usuario: coordinador"
echo "   Contraseña: 123456"
echo ""
echo "🛑 Para detener: docker-compose down"
echo "🔄 Para reiniciar: docker-compose up"

