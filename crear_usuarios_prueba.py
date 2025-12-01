import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario, Estudiante, DocenteAsesor, Instructor

# Crear superusuario coordinador
coordinador = Usuario.objects.create_superuser(
    username='coordinador',
    email='coordinador@universidad.edu',
    password='123456',
    first_name='Juan',
    last_name='Coordinador',
    rol='COORDINADOR'
)

# Crear estudiante de prueba
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
instructor_user = Usuario.objects.create_user(
    username='instructor_techcorp',
    email='instructor@techcorp.com',
    password='123456',
    first_name='Roberto',
    last_name='Instructor',
    rol='INSTRUCTOR'
)

Instructor.objects.create(
    usuario=instructor_user,
    cargo='Jefe de Tecnología'
)

print("✓ Usuarios de prueba creados exitosamente")
print(f"  - Coordinador: coordinador / 123456")
print(f"  - Estudiante: ana_martinez / 123456")
print(f"  - Docente: dr_garcia / 123456")
print(f"  - Instructor: instructor_techcorp / 123456")

