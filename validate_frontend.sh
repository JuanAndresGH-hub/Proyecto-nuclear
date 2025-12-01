#!/bin/bash
# Script de Validación del Frontend Mejorado
# Este script verifica que todas las mejoras se aplicaron correctamente

echo "🔍 VALIDANDO FRONTEND MEJORADO..."
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de validaciones
PASSED=0
FAILED=0

# Función para validar archivos
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} Archivo encontrado: $1"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} Archivo NO encontrado: $1"
        ((FAILED++))
    fi
}

# Función para validar contenido
check_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Contenido validado en: $1"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} Contenido NO encontrado en: $1"
        ((FAILED++))
    fi
}

echo "📁 VERIFICANDO ARCHIVOS..."
echo ""

# CSS Files
check_file "static/css/style.css"
check_file "static/css/animations.css"

# Templates
check_file "templates/base.html"
check_file "templates/login.html"
check_file "templates/register.html"
check_file "templates/dashboard.html"
check_file "templates/profile.html"
check_file "templates/vacantes_list.html"

# Documentation
check_file "MEJORAS_FRONTEND.md"
check_file "FRONTEND_SUMMARY.md"

echo ""
echo "🎨 VERIFICANDO ESTILOS CSS..."
echo ""

# CSS validation
check_content "static/css/style.css" ":root {"
check_content "static/css/style.css" "--primary-color: #ffffff"
check_content "static/css/style.css" ".sidebar {"
check_content "static/css/style.css" ".card {"
check_content "static/css/animations.css" "@keyframes fadeIn"
check_content "static/css/animations.css" "@keyframes slideInLeft"

echo ""
echo "🏗️  VERIFICANDO TEMPLATES..."
echo ""

# Template validation
check_content "templates/base.html" "{% load static %}"
check_content "templates/base.html" "css/style.css"
check_content "templates/base.html" "css/animations.css"
check_content "templates/login.html" "class=\"login-container\""
check_content "templates/register.html" "class=\"register-container\""
check_content "templates/dashboard.html" "{% extends 'base.html' %}"
check_content "templates/profile.html" "{% extends 'base.html' %}"

echo ""
echo "🎬 VERIFICANDO ANIMACIONES..."
echo ""

# Animation validation
check_content "static/css/animations.css" "fadeInUp"
check_content "static/css/animations.css" "slideInLeft"
check_content "static/css/animations.css" "scaleIn"
check_content "static/css/animations.css" "softGlow"
check_content "static/css/animations.css" "float"

echo ""
echo "📋 RESUMEN DE VALIDACIÓN"
echo "================================"
echo -e "Validaciones Pasadas:  ${GREEN}$PASSED${NC}"
echo -e "Validaciones Fallidas: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ TODAS LAS VALIDACIONES PASARON${NC}"
    echo ""
    echo "🚀 El frontend está listo para usar!"
    echo ""
    echo "Próximos pasos:"
    echo "1. Ejecutar: python manage.py runserver"
    echo "2. Ir a: http://localhost:8000/login"
    echo "3. Probar con: coordinador / 123456"
    exit 0
else
    echo -e "${RED}✗ ALGUNAS VALIDACIONES FALLARON${NC}"
    echo ""
    echo "Por favor, verificar los archivos faltantes."
    exit 1
fi

