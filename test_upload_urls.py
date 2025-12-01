"""
Script de prueba para verificar que la carga de archivos funciona
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Estudiante

# Verificar que los estudiantes existen
print("=" * 60)
print("VERIFICACIÓN DE ESTUDIANTES")
print("=" * 60)

estudiantes = Estudiante.objects.all()
for estudiante in estudiantes:
    print(f"\nID: {estudiante.id}")
    print(f"Usuario: {estudiante.usuario.username}")
    print(f"Nombre: {estudiante.usuario.get_full_name()}")
    print(f"HV Archivo: {estudiante.hv_archivo}")
    print(f"Estado HV: {estudiante.estado_hv}")
    print("-" * 40)

print("\n" + "=" * 60)
print("URLs ESPERADAS:")
print("=" * 60)
for estudiante in estudiantes[:3]:
    print(f"\nPara {estudiante.usuario.get_full_name()}:")
    print(f"  URL: /api/usuarios/estudiantes/{estudiante.id}/hoja-vida/")

print("\n")

