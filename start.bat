@echo off
echo ================================================================
echo   Sistema de Gestion de Practicas Profesionales
echo   Iniciando servidor...
echo ================================================================
echo.

cd /d "%~dp0"

echo [1/2] Activando entorno virtual...
call .venv1\Scripts\activate.bat

echo [2/2] Iniciando servidor Django...
echo.
echo ================================================================
echo   Servidor iniciado correctamente!
echo ================================================================
echo.
echo   Accede en tu navegador a:
echo   http://127.0.0.1:8000/login/
echo.
echo   Usuarios de prueba (password: 123456):
echo   - coordinador
echo   - ana_martinez
echo   - dr_garcia
echo   - instructor_techcorp
echo.
echo   Presiona Ctrl+C para detener el servidor
echo ================================================================
echo.

python manage.py runserver

