#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario
from django.contrib.auth import authenticate

print("Verificando usuario ana_martinez...")
try:
    u = Usuario.objects.get(username='ana_martinez')
    print(f"Usuario: {u.username}")
    print(f"Activo: {u.is_active}")
    print(f"Check password 123456: {u.check_password('123456')}")
    
    # Intentar autenticar
    auth = authenticate(username='ana_martinez', password='123456')
    print(f"Authenticate result: {auth}")
    
except Usuario.DoesNotExist:
    print("Usuario NO existe!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

