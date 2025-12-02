"""
Script de Verificacion del Sistema
Sistema de Gestion de Practicas Profesionales
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from empresas.models import Empresa, Vacante
from practicas.models import Practica
from django.db import connection

User = get_user_model()

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_success(text):
    print(f"✓ {text}")

def print_info(text):
    print(f"  {text}")

def verificar_base_datos():
    print_header("VERIFICACION DE BASE DE DATOS")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print_success("Conexion a base de datos OK")
        print_info(f"Motor: {connection.settings_dict['ENGINE']}")
        print_info(f"Base de datos: {connection.settings_dict['NAME']}")
        return True
    except Exception as e:
        print(f"✗ Error de conexion: {e}")
        return False

def verificar_usuarios():
    print_header("VERIFICACION DE USUARIOS")

    usuarios_esperados = {
        'coordinador': 'COORDINADOR',
        'ana_martinez': 'ESTUDIANTE',
        'dr_garcia': 'DOCENTE',
        'instructor_techcorp': 'INSTRUCTOR'
    }

    total = 0
    for username, rol in usuarios_esperados.items():
        try:
            user = User.objects.get(username=username)
            print_success(f"{username} ({rol}) - ID: {user.id}")
            total += 1
        except User.DoesNotExist:
            print(f"✗ Usuario {username} no encontrado")

    print_info(f"\nTotal usuarios de prueba: {total}/{len(usuarios_esperados)}")
    return total == len(usuarios_esperados)

def verificar_modelos():
    print_header("VERIFICACION DE MODELOS")

    modelos = [
        ('Usuarios', User),
        ('Empresas', Empresa),
        ('Vacantes', Vacante),
        ('Practicas', Practica),
    ]

    for nombre, modelo in modelos:
        try:
            count = modelo.objects.count()
            print_success(f"{nombre}: {count} registros")
        except Exception as e:
            print(f"✗ Error en {nombre}: {e}")

    return True

def verificar_directorios():
    print_header("VERIFICACION DE DIRECTORIOS")

    directorios = [
        'media',
        'media/hojas_vida',
        'static',
        'staticfiles',
        'templates',
    ]

    total = 0
    for directorio in directorios:
        if os.path.exists(directorio):
            print_success(f"{directorio}")
            total += 1
        else:
            print(f"✗ {directorio} no encontrado")

    print_info(f"\nTotal directorios: {total}/{len(directorios)}")
    return total == len(directorios)

def verificar_archivos():
    print_header("VERIFICACION DE ARCHIVOS CLAVE")

    archivos = [
        'manage.py',
        'requirements.txt',
        'db.sqlite3',
        'README.md',
        'GUIA_DESPLIEGUE.md',
        'start.ps1',
        'start.bat',
    ]

    total = 0
    for archivo in archivos:
        if os.path.exists(archivo):
            print_success(f"{archivo}")
            total += 1
        else:
            print(f"⚠ {archivo} no encontrado")

    print_info(f"\nTotal archivos: {total}/{len(archivos)}")
    return True

def main():
    print("\n")
    print("=" * 70)
    print("  VERIFICACION DEL SISTEMA")
    print("  Sistema de Gestion de Practicas Profesionales")
    print("=" * 70)

    resultados = []

    # Ejecutar verificaciones
    resultados.append(("Base de Datos", verificar_base_datos()))
    resultados.append(("Usuarios", verificar_usuarios()))
    resultados.append(("Modelos", verificar_modelos()))
    resultados.append(("Directorios", verificar_directorios()))
    resultados.append(("Archivos", verificar_archivos()))

    # Resumen
    print_header("RESUMEN DE VERIFICACION")

    total_ok = sum(1 for _, ok in resultados if ok)
    total = len(resultados)

    for nombre, ok in resultados:
        status = "✓ OK" if ok else "✗ ERROR"
        print(f"  {nombre:.<30} {status}")

    print("\n" + "=" * 70)
    if total_ok == total:
        print("  ✓✓✓ SISTEMA COMPLETAMENTE OPERATIVO ✓✓✓")
        print("=" * 70)
        print("\n  Para iniciar el servidor:")
        print("    python manage.py runserver")
        print("\n  Accede en: http://127.0.0.1:8000/login/")
        print("\n  Usuarios de prueba (password: 123456):")
        print("    - coordinador")
        print("    - ana_martinez")
        print("    - dr_garcia")
        print("    - instructor_techcorp")
    else:
        print(f"  ⚠ SISTEMA CON ADVERTENCIAS ({total_ok}/{total} OK)")
        print("=" * 70)
        print("\n  Revisa los errores arriba y ejecuta:")
        print("    python manage.py migrate")
        print("    python crear_usuarios_simple.py")

    print("\n")
    return total_ok == total

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Error critico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

