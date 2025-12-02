# Script para actualizar el repositorio con la correccion de render.yaml

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "   ACTUALIZANDO REPOSITORIO" -ForegroundColor Yellow
Write-Host "================================================================`n" -ForegroundColor Cyan

Write-Host "Agregando cambios..." -ForegroundColor Yellow
git add render.yaml

Write-Host "Creando commit..." -ForegroundColor Yellow
git commit -m "Fix: Corregir configuracion de render.yaml"

Write-Host "Subiendo cambios..." -ForegroundColor Yellow
git push origin main

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "   CAMBIOS SUBIDOS CORRECTAMENTE" -ForegroundColor Green
Write-Host "================================================================`n" -ForegroundColor Cyan

Write-Host "Render detectara los cambios automaticamente y actualizara" -ForegroundColor White
Write-Host "la configuracion. Refresca la pagina de Render.`n" -ForegroundColor White

