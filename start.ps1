# Script Rápido de Inicio
# Para uso diario del servidor

Write-Host "🚀 Iniciando servidor..." -ForegroundColor Cyan

# Activar entorno virtual
& ".\.venv1\Scripts\Activate.ps1"

# Iniciar servidor
Write-Host ""
Write-Host "✓ Servidor Django iniciando..." -ForegroundColor Green
Write-Host "  Accede en: http://127.0.0.1:8000/login/" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver

