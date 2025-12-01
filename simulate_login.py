#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simular el POST del formulario de login
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from usuarios.models import Usuario

print("="*60)
print("SIMULANDO POST DE LOGIN")
print("="*60)

client = Client()

# Primero GET para obtener CSRF token
print("\n1. GET /login/ para obtener CSRF token")
response = client.get('/login/')
csrf_token = response.cookies.get('csrftoken').value if 'csrftoken' in response.cookies else None
print(f"CSRF Token obtenido: {csrf_token[:30] if csrf_token else 'NO'}")

# Ahora POST con datos correctos
print("\n2. POST /login/ con ana_martinez/123456")
response = client.post('/login/', {
    'username': 'ana_martinez',
    'password': '123456',
})

print(f"Status code: {response.status_code}")
print(f"Redirect URL: {response.url if response.status_code in [301, 302] else 'No redirect'}")

# Verificar si hay error en el response
error_msg = 'invlidas'.encode() if sys.version_info[0] == 3 else 'invlidas'
if b'invlidas' in response.content or 'invlidas' in response.content.decode('utf-8', errors='ignore'):
    print("ERROR: Mensaje de error encontrado en response")
else:
    print("OK: No hay mensaje de error")


print("\n" + "="*60)

