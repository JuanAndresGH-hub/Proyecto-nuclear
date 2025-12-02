# Script para preparar el proyecto para GitHub y Render
# Ejecutar en PowerShell

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "   PREPARANDO PROYECTO PARA GITHUB Y RENDER" -ForegroundColor Yellow
Write-Host "================================================================`n" -ForegroundColor Cyan

# Verificar si Git está instalado
Write-Host "[1/5] Verificando Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✓ $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git no está instalado" -ForegroundColor Red
    Write-Host "  Descarga Git desde: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Verificar si ya hay un repositorio Git
Write-Host "`n[2/5] Verificando repositorio Git..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "✓ Repositorio Git ya existe" -ForegroundColor Green
    $reinit = Read-Host "¿Deseas reinicializar? (s/N)"
    if ($reinit -eq "s" -or $reinit -eq "S") {
        Remove-Item -Recurse -Force .git
        git init
        Write-Host "✓ Repositorio reinicializado" -ForegroundColor Green
    }
} else {
    git init
    Write-Host "✓ Repositorio Git inicializado" -ForegroundColor Green
}

# Agregar archivos
Write-Host "`n[3/5] Agregando archivos al repositorio..." -ForegroundColor Yellow
git add .
Write-Host "✓ Archivos agregados" -ForegroundColor Green

# Hacer commit
Write-Host "`n[4/5] Creando commit inicial..." -ForegroundColor Yellow
git commit -m "Initial commit - Sistema de Gestion de Practicas para Render"
Write-Host "✓ Commit creado" -ForegroundColor Green

# Mostrar instrucciones
Write-Host "`n[5/5] Próximos pasos..." -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   PROYECTO LISTO PARA GITHUB" -ForegroundColor Green
Write-Host "================================================================`n" -ForegroundColor Cyan

Write-Host "SIGUIENTE PASO: Subir a GitHub" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Crea un repositorio en GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Ejecuta estos comandos (reemplaza TU_USUARIO):" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/TU_USUARIO/sistema-practicas.git" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Luego ve a Render y sigue DESPLIEGUE_RENDER.md" -ForegroundColor White
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   LEE DESPLIEGUE_RENDER.md PARA INSTRUCCIONES COMPLETAS" -ForegroundColor Yellow
Write-Host "================================================================`n" -ForegroundColor Cyan

# Abrir archivo de guía
$abrir = Read-Host "¿Deseas abrir DESPLIEGUE_RENDER.md ahora? (S/n)"
if ($abrir -ne "n" -and $abrir -ne "N") {
    Start-Process "DESPLIEGUE_RENDER.md"
}

