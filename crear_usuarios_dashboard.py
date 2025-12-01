"""
Script para crear usuarios específicos vistos en el dashboard del docente
Ejecutar con: python crear_usuarios_dashboard.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario, Estudiante, DocenteAsesor, Instructor
from empresas.models import Empresa
from practicas.models import Practica
from datetime import date, timedelta

print("=" * 60)
print("CREANDO USUARIOS DEL DASHBOARD")
print("=" * 60)

# Obtener docente e instructor
try:
    docente = DocenteAsesor.objects.get(usuario__username='dr_garcia')
    print(f"\n✓ Docente: {docente.usuario.get_full_name()}")
except DocenteAsesor.DoesNotExist:
    print("\n✗ ERROR: El docente 'dr_garcia' no existe.")
    print("Ejecuta primero: python crear_usuarios_prueba.py")
    exit(1)

try:
    instructor = Instructor.objects.get(usuario__username='instructor_techcorp')
    print(f"✓ Instructor: {instructor.usuario.get_full_name()}")
except Instructor.DoesNotExist:
    instructor_user = Usuario.objects.create_user(
        username='instructor_techcorp',
        email='instructor@techcorp.com',
        password='123456',
        first_name='Miguel',
        last_name='Rodríguez',
        rol='INSTRUCTOR'
    )
    instructor = Instructor.objects.create(
        usuario=instructor_user,
        cargo='Jefe de Tecnología'
    )
    print(f"✓ Instructor creado: {instructor.usuario.get_full_name()}")

# Obtener o crear empresas
print("\n" + "=" * 60)
print("EMPRESAS")
print("=" * 60)

empresas = []
empresas_data = [
    {'nombre': 'TechCorp S.A.', 'ciudad': 'Bogotá', 'nit': '900123456-7'},
    {'nombre': 'InnovaSoft Ltda.', 'ciudad': 'Medellín', 'nit': '900987654-3'},
    {'nombre': 'DataSolutions Corp.', 'ciudad': 'Cali', 'nit': '900555777-9'},
]

for emp_data in empresas_data:
    try:
        empresa = Empresa.objects.get(nombre=emp_data['nombre'])
        print(f"✓ Empresa existente: {empresa.nombre}")
    except Empresa.DoesNotExist:
        empresa = Empresa.objects.create(
            nombre=emp_data['nombre'],
            nit=emp_data['nit'],
            ciudad=emp_data['ciudad'],
            direccion=f"Dirección en {emp_data['ciudad']}",
            telefono='3101234567',
            correo=f"contacto@{emp_data['nombre'].lower().replace(' ', '').replace('.', '')}.com"
        )
        print(f"✓ Empresa creada: {empresa.nombre}")
    empresas.append(empresa)

# Estudiantes según el dashboard
print("\n" + "=" * 60)
print("CREANDO ESTUDIANTES")
print("=" * 60)

estudiantes_data = [
    {
        'first_name': 'Lucía',
        'last_name': 'Hernández',
        'username': 'lucia_hernandez',
        'email': 'lucia.hernandez@universidad.edu',
        'programa': 'Administración de Empresas',
        'semestre': 9,
        'empresa': empresas[2]  # DataSolutions
    },
    {
        'first_name': 'María',
        'last_name': 'López',
        'username': 'maria_lopez',
        'email': 'maria.lopez@universidad.edu',
        'programa': 'Ingeniería de Sistemas',
        'semestre': 8,
        'empresa': empresas[0]  # TechCorp
    },
    {
        'first_name': 'Carlos',
        'last_name': 'Moreno',
        'username': 'carlos_moreno',
        'email': 'carlos.moreno@universidad.edu',
        'programa': 'Ingeniería de Sistemas',
        'semestre': 8,
        'empresa': empresas[0]  # TechCorp
    },
    {
        'first_name': 'Pedro',
        'last_name': 'Ramírez',
        'username': 'pedro_ramirez',
        'email': 'pedro.ramirez@universidad.edu',
        'programa': 'Ingeniería Industrial',
        'semestre': 7,
        'empresa': empresas[1]  # InnovaSoft
    },
]

# Verificar si los estudiantes ya existen antes de recrearlos
estudiantes_a_crear = []
for est_data in estudiantes_data:
    if Usuario.objects.filter(username=est_data['username']).exists():
        print(f"✓ Estudiante ya existe: {est_data['username']}")
    else:
        estudiantes_a_crear.append(est_data)

estudiantes_data = estudiantes_a_crear

fecha_inicio = date.today() - timedelta(days=30)
fecha_fin = fecha_inicio + timedelta(days=120)

if estudiantes_data:
    print("\nCreando nuevos usuarios y prácticas:")
else:
    print("\nTodos los estudiantes ya existen. No se creará ninguno nuevo.")

for est_data in estudiantes_data:
    # Crear usuario
    user = Usuario.objects.create_user(
        username=est_data['username'],
        email=est_data['email'],
        password='123456',
        first_name=est_data['first_name'],
        last_name=est_data['last_name'],
        rol='ESTUDIANTE'
    )

    # Crear perfil de estudiante
    estudiante = Estudiante.objects.create(
        usuario=user,
        programa_academico=est_data['programa'],
        semestre=est_data['semestre']
    )

    # Crear práctica
    practica = Practica.objects.create(
        estudiante=estudiante,
        numero=1,
        docente_asesor=docente,
        instructor=instructor,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado='EN_CURSO',
        observaciones=f'Práctica en {est_data["empresa"].nombre}'
    )

    print(f"✓ {user.get_full_name()} - {est_data['programa']} - Semestre {est_data['semestre']}")

# Resumen
print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"\n✓ Empresas: {len(empresas)}")
print(f"✓ Estudiantes nuevos creados: {len(estudiantes_data)}")
print(f"✓ Total estudiantes en el sistema: {Usuario.objects.filter(rol='ESTUDIANTE').count()}")
print(f"✓ Prácticas asignadas al docente: {Practica.objects.filter(docente_asesor=docente).count()}")

print("\n" + "=" * 60)
print("CREDENCIALES DE ACCESO")
print("=" * 60)
print("\nDOCENTE:")
print("  Usuario: dr_garcia")
print("  Contraseña: 123456")

print("\nESTUDIANTES (todos con contraseña: 123456):")
estudiantes_todos = Usuario.objects.filter(rol='ESTUDIANTE').order_by('username')
for est in estudiantes_todos:
    print(f"  {est.first_name} {est.last_name}: {est.username}")

print("\n" + "=" * 60)
print("¡USUARIOS CREADOS EXITOSAMENTE!")
print("=" * 60)
print("\nAhora puedes:")
print("1. Iniciar sesión como cualquier estudiante")
print("2. Subir tu hoja de vida desde el dashboard")
print("3. El docente podrá ver la hoja de vida en 'Mis Documentos'")
print("\n")

