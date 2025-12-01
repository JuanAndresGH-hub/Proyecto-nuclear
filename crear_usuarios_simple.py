#!/usr/bin/env python
"""
Script para crear usuarios de prueba
Uso: python crear_usuarios_prueba_simple.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario, Estudiante, DocenteAsesor, Instructor

def crear_usuarios():
    print("Creando usuarios de prueba...")

    # Eliminar usuarios existentes (opcional)
    Usuario.objects.all().delete()

    # Crear superusuario coordinador
    print("✓ Creando Coordinador...")
    coordinador = Usuario.objects.create_superuser(
        username='coordinador',
        email='coordinador@universidad.edu',
        password='123456',
        first_name='Juan',
        last_name='Coordinador',
        rol='COORDINADOR'
    )

    # Crear estudiante de prueba
    print("✓ Creando Estudiante...")
    estudiante_user = Usuario.objects.create_user(
        username='ana_martinez',
        email='ana@universidad.edu',
        password='123456',
        first_name='Ana',
        last_name='Martínez',
        rol='ESTUDIANTE'
    )

    Estudiante.objects.create(
        usuario=estudiante_user,
        programa_academico='Ingeniería de Sistemas',
        semestre=7
    )

    # Crear docente asesor
    print("✓ Creando Docente...")
    docente_user = Usuario.objects.create_user(
        username='dr_garcia',
        email='garcia@universidad.edu',
        password='123456',
        first_name='Carlos',
        last_name='García',
        rol='DOCENTE'
    )

    DocenteAsesor.objects.create(
        usuario=docente_user,
        departamento='Ingeniería'
    )

    # Crear instructor
    print("✓ Creando Instructor...")
    instructor_user = Usuario.objects.create_user(
        username='instructor_techcorp',
        email='instructor@techcorp.com',
        password='123456',
        first_name='Miguel',
        last_name='Rodríguez',
        rol='INSTRUCTOR'
    )

    Instructor.objects.create(
        usuario=instructor_user,
        cargo='Jefe de Práctica'
    )

    print("\n✅ ¡Usuarios creados exitosamente!")
    print("\nCredenciales de prueba:")
    print("  👨‍💼 Coordinador: coordinador / 123456")
    print("  👨‍🎓 Estudiante: ana_martinez / 123456")
    print("  👨‍🏫 Docente: dr_garcia / 123456")
    print("  👨‍💼 Instructor: instructor_techcorp / 123456")

if __name__ == '__main__':
    try:
        crear_usuarios()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

