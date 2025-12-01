#!/usr/bin/env python
"""
Test de POST login directamente
"""
import os
import sys
import django
from io import StringIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from usuarios.models import Usuario

print("=" * 60)
print("TEST DE LOGIN VÍA CLIENTE HTTP")
print("=" * 60)

# Crear cliente
client = Client()

# Test 1: GET del formulario
print("\n1. GET /login/ - Obtener formulario")
print("-" * 60)
response = client.get('/login/')
print(f"Status code: {response.status_code}")
print(f"Template usado: {response.templates}")

# Test 2: POST login con credenciales válidas
print("\n2. POST /login/ - Intentar login con ana_martinez/123456")
print("-" * 60)
response = client.post('/login/', {
    'username': 'ana_martinez',
    'password': '123456',
})
print(f"Status code: {response.status_code}")
print(f"Redirected to: {response.url if hasattr(response, 'url') else 'No redirect'}")
print(f"Contenido (primeros 500 chars): {response.content.decode('utf-8')[:500]}")

# Test 3: Verificar que session contiene usuario
print("\n3. Verificar sesión del cliente")
print("-" * 60)
if 'django_tests' in response.wsgi_request.session:
    print("✓ Usuario en sesión")
else:
    print("✗ No hay usuario en sesión")

print("\n" + "=" * 60)
print("FIN DEL TEST")
print("=" * 60)

