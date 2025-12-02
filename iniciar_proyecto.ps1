# Script de Inicializacion del Proyecto
# Sistema de Gestion de Practicas Profesionales

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Sistema de Gestion de Practicas" -ForegroundColor Cyan
Write-Host "  Script de Inicializacion" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "[1/8] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "OK $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "X Python no encontrado" -ForegroundColor Red
    exit 1
}

# Crear entorno virtual si no existe
Write-Host ""
Write-Host "[2/8] Verificando entorno virtual..." -ForegroundColor Yellow
if (!(Test-Path ".venv1")) {
    Write-Host "  Creando entorno virtual..." -ForegroundColor Cyan
    python -m venv .venv1
    Write-Host "OK Entorno virtual creado" -ForegroundColor Green
} else {
    Write-Host "OK Entorno virtual ya existe" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host ""
Write-Host "[3/8] Activando entorno virtual..." -ForegroundColor Yellow
& ".\.venv1\Scripts\Activate.ps1"
Write-Host "OK Entorno virtual activado" -ForegroundColor Green

# Instalar dependencias
Write-Host ""
Write-Host "[4/8] Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "OK Dependencias instaladas" -ForegroundColor Green

# Crear directorios necesarios
Write-Host ""
Write-Host "[5/8] Creando directorios necesarios..." -ForegroundColor Yellow
$directories = @("media", "media/hojas_vida", "staticfiles", "static/css", "static/js")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "OK Directorios creados" -ForegroundColor Green

# Aplicar migraciones
Write-Host ""
Write-Host "[6/8] Aplicando migraciones de base de datos..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate
Write-Host "OK Migraciones aplicadas" -ForegroundColor Green

# Recolectar archivos estaticos
Write-Host ""
Write-Host "[7/8] Recolectando archivos estaticos..." -ForegroundColor Yellow
python manage.py collectstatic --noinput --clear
Write-Host "OK Archivos estaticos recolectados" -ForegroundColor Green

# Crear usuarios de prueba
Write-Host ""
Write-Host "[8/8] Creando usuarios de prueba..." -ForegroundColor Yellow
if (Test-Path "crear_usuarios_simple.py") {
    python crear_usuarios_simple.py
    Write-Host "OK Usuarios creados o ya existen" -ForegroundColor Green
} else {
    Write-Host "AVISO Script de usuarios no encontrado" -ForegroundColor Yellow
}

# Resumen final
Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  OK Inicializacion Completa" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Usuarios disponibles:" -ForegroundColor White
Write-Host "  Coordinador: coordinador / 123456" -ForegroundColor Yellow
Write-Host "  Estudiante:  ana_martinez / 123456" -ForegroundColor Yellow
Write-Host "  Docente:     dr_garcia / 123456" -ForegroundColor Yellow
Write-Host "  Instructor:  instructor_techcorp / 123456" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para iniciar el servidor, ejecuta:" -ForegroundColor White
Write-Host "  python manage.py runserver" -ForegroundColor Green
Write-Host ""
Write-Host "Accede en: http://127.0.0.1:8000/login/" -ForegroundColor Cyan
Write-Host ""

