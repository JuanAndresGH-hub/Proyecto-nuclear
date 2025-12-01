"""
Script para eliminar estudiantes duplicados
Ejecutar con: python eliminar_duplicados.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario, Estudiante
from practicas.models import Practica

print("=" * 60)
print("ELIMINANDO ESTUDIANTES DUPLICADOS")
print("=" * 60)

# Lista de duplicados a eliminar (con punto en el username)
duplicados_a_eliminar = [
    'carlos.moreno',
    'lucia.hernandez',
    'maria.lopez',
    'pedro.ramirez'
]

print("\nEstudiantes que serán eliminados:")
for username in duplicados_a_eliminar:
    try:
        user = Usuario.objects.get(username=username)
        print(f"  - {username} (ID: {user.id}) - {user.get_full_name()}")

        # Verificar si tiene prácticas
        if hasattr(user, 'estudiante_perfil'):
            practicas = Practica.objects.filter(estudiante=user.estudiante_perfil)
            if practicas.exists():
                print(f"    ⚠ Tiene {practicas.count()} práctica(s) que también se eliminarán")
    except Usuario.DoesNotExist:
        print(f"  - {username} (no existe)")

print("\n" + "=" * 60)
respuesta = input("¿Deseas continuar con la eliminación? (s/n): ")

if respuesta.lower() == 's':
    print("\nEliminando usuarios duplicados...")
    for username in duplicados_a_eliminar:
        try:
            user = Usuario.objects.get(username=username)
            nombre_completo = user.get_full_name()
            user.delete()
            print(f"  ✓ Eliminado: {username} - {nombre_completo}")
        except Usuario.DoesNotExist:
            print(f"  ⚠ No existe: {username}")

    print("\n" + "=" * 60)
    print("ESTUDIANTES RESTANTES:")
    print("=" * 60)

    estudiantes = Usuario.objects.filter(rol='ESTUDIANTE').order_by('username')
    for user in estudiantes:
        print(f"  {user.username} - {user.get_full_name()} - {user.email}")

    print("\n" + "=" * 60)
    print("✓ PROCESO COMPLETADO")
    print("=" * 60)
else:
    print("\n✗ Operación cancelada")

