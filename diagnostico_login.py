#!/usr/bin/env python
"""
Script de diagnóstico para problema de login
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import authenticate
from usuarios.models import Usuario

print("=" * 60)
print("DIAGNÓSTICO DE LOGIN")
print("=" * 60)

# 1. Verificar usuarios
print("\n1. USUARIOS EN LA BASE DE DATOS:")
print("-" * 60)
users = Usuario.objects.all()
print(f"Total de usuarios: {users.count()}")
for u in users:
    print(f"\n  Usuario: {u.username}")
    print(f"    - Email: {u.email}")
    print(f"    - Nombre: {u.first_name} {u.last_name}")
    print(f"    - Rol: {u.rol} ({u.get_rol_display()})")
    print(f"    - Activo: {u.is_active}")
    print(f"    - Staff: {u.is_staff}")
    print(f"    - Password válido para '123456': {u.check_password('123456')}")
    print(f"    - Password hash: {u.password[:30]}...")

# 2. Intentar autenticar con cada usuario
print("\n\n2. PRUEBA DE AUTENTICACIÓN:")
print("-" * 60)
for u in users:
    print(f"\nIntentando autenticar: {u.username} / 123456")
    user = authenticate(username=u.username, password='123456')
    print(f"  Resultado: {user}")
    if user:
        print(f"  ✓ Autenticación exitosa")
    else:
        print(f"  ✗ Autenticación fallida")
        # Intentar debug adicional
        print(f"    - Check password manual: {u.check_password('123456')}")

# 3. Verificar configuración de autenticación
print("\n\n3. CONFIGURACIÓN DE AUTENTICACIÓN:")
print("-" * 60)
from django.conf import settings
print(f"AUTHENTICATION_BACKENDS: {settings.AUTHENTICATION_BACKENDS}")
print(f"AUTH_USER_MODEL: {settings.AUTH_USER_MODEL}")

print("\n" + "=" * 60)
print("FIN DEL DIAGNÓSTICO")
print("=" * 60)

