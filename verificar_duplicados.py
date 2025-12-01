import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario
from collections import Counter

print("=" * 70)
print("VERIFICACIÓN FINAL DE DUPLICADOS")
print("=" * 70)

# Obtener todos los usernames
usernames = list(Usuario.objects.values_list('username', flat=True))

# Contar ocurrencias
contador = Counter(usernames)
duplicados = {username: count for username, count in contador.items() if count > 1}

if duplicados:
    print("\n❌ SE ENCONTRARON DUPLICADOS:")
    for username, count in duplicados.items():
        print(f"   - {username}: {count} veces")
    print("\nUsuarios con ese username:")
    for username in duplicados.keys():
        usuarios = Usuario.objects.filter(username=username)
        for u in usuarios:
            print(f"     ID: {u.id} | {u.username} | {u.get_full_name()} | {u.email}")
else:
    print("\n✅ NO SE ENCONTRARON DUPLICADOS")

print("\n" + "=" * 70)
print("LISTA DE TODOS LOS ESTUDIANTES:")
print("=" * 70)

estudiantes = Usuario.objects.filter(rol='ESTUDIANTE').order_by('username')
for i, est in enumerate(estudiantes, 1):
    print(f"{i}. {est.username:20} | {est.get_full_name():30} | {est.email}")

print("\n" + "=" * 70)
print("RESUMEN:")
print("=" * 70)
print(f"Total de usuarios en el sistema: {Usuario.objects.count()}")
print(f"Total de estudiantes: {estudiantes.count()}")
print(f"Total de docentes: {Usuario.objects.filter(rol='DOCENTE').count()}")
print(f"Total de instructores: {Usuario.objects.filter(rol='INSTRUCTOR').count()}")
print(f"Total de coordinadores: {Usuario.objects.filter(rol='COORDINADOR').count()}")
print("=" * 70)

if not duplicados:
    print("\n✅ VERIFICACIÓN EXITOSA: Sistema limpio sin duplicados")
else:
    print("\n⚠ ADVERTENCIA: Se encontraron duplicados que deben ser eliminados")

