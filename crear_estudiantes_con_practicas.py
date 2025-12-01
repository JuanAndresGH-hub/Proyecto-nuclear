"""
Script para crear estudiantes con prácticas asignadas al docente Carlos García
Ejecutar con: python crear_estudiantes_con_practicas.py
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
print("CREANDO ESTUDIANTES Y PRÁCTICAS DE PRUEBA")
print("=" * 60)

# 1. Obtener o crear empresas
print("\n1. Creando empresas...")
try:
    empresa1 = Empresa.objects.get(nombre="TechCorp S.A.")
    print(f"   ✓ Empresa existente: {empresa1.nombre}")
except Empresa.DoesNotExist:
    empresa1 = Empresa.objects.create(
        nombre="TechCorp S.A.",
        nit="900123456-7",
        ciudad="Bogotá",
        direccion="Calle 100 #15-20",
        telefono="3101234567",
        correo="contacto@techcorp.com",
        descripcion="Empresa líder en soluciones tecnológicas"
    )
    print(f"   ✓ Empresa creada: {empresa1.nombre}")

try:
    empresa2 = Empresa.objects.get(nombre="InnovaSoft Ltda.")
    print(f"   ✓ Empresa existente: {empresa2.nombre}")
except Empresa.DoesNotExist:
    empresa2 = Empresa.objects.create(
        nombre="InnovaSoft Ltda.",
        nit="900987654-3",
        ciudad="Medellín",
        direccion="Carrera 50 #30-10",
        telefono="3209876543",
        correo="info@innovasoft.com",
        descripcion="Desarrollo de software a medida"
    )
    print(f"   ✓ Empresa creada: {empresa2.nombre}")

try:
    empresa3 = Empresa.objects.get(nombre="DataSolutions Corp.")
    print(f"   ✓ Empresa existente: {empresa3.nombre}")
except Empresa.DoesNotExist:
    empresa3 = Empresa.objects.create(
        nombre="DataSolutions Corp.",
        nit="900555777-9",
        ciudad="Cali",
        direccion="Avenida 6 Norte #25-30",
        telefono="3155557777",
        correo="contact@datasolutions.com",
        descripcion="Consultoría en análisis de datos"
    )
    print(f"   ✓ Empresa creada: {empresa3.nombre}")

# 2. Obtener docente e instructor
print("\n2. Obteniendo docente e instructor...")
try:
    docente = DocenteAsesor.objects.get(usuario__username='dr_garcia')
    print(f"   ✓ Docente: {docente.usuario.get_full_name()}")
except DocenteAsesor.DoesNotExist:
    print("   ✗ ERROR: El docente 'dr_garcia' no existe. Ejecuta primero: python crear_usuarios_prueba.py")
    exit(1)

try:
    instructor = Instructor.objects.get(usuario__username='instructor_techcorp')
    print(f"   ✓ Instructor: {instructor.usuario.get_full_name()}")
except Instructor.DoesNotExist:
    print("   ✗ ERROR: El instructor 'instructor_techcorp' no existe. Ejecuta primero: python crear_usuarios_prueba.py")
    exit(1)

# 3. Crear estudiantes
print("\n3. Creando estudiantes...")

estudiantes_data = [
    {
        'username': 'lucia_hernandez',
        'email': 'lucia.hernandez@universidad.edu',
        'first_name': 'Lucía',
        'last_name': 'Hernández',
        'programa': 'Administración de Empresas',
        'semestre': 9,
        'empresa': empresa3,
    },
    {
        'username': 'maria_lopez',
        'email': 'maria.lopez@universidad.edu',
        'first_name': 'María',
        'last_name': 'López',
        'programa': 'Ingeniería de Sistemas',
        'semestre': 8,
        'empresa': empresa1,
    },
    {
        'username': 'carlos_moreno',
        'email': 'carlos.moreno@universidad.edu',
        'first_name': 'Carlos',
        'last_name': 'Moreno',
        'programa': 'Ingeniería de Sistemas',
        'semestre': 8,
        'empresa': empresa1,
    },
    {
        'username': 'pedro_ramirez',
        'email': 'pedro.ramirez@universidad.edu',
        'first_name': 'Pedro',
        'last_name': 'Ramírez',
        'programa': 'Ingeniería Industrial',
        'semestre': 7,
        'empresa': empresa2,
    },
]

estudiantes_creados = []

for est_data in estudiantes_data:
    try:
        # Verificar si el usuario ya existe
        user = Usuario.objects.get(username=est_data['username'])
        print(f"   ⚠ Usuario existente: {user.username} - No se creará duplicado")
        estudiante = Estudiante.objects.get(usuario=user)
    except Usuario.DoesNotExist:
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
        print(f"   ✓ Estudiante creado: {user.get_full_name()} ({est_data['username']})")

    estudiantes_creados.append({
        'estudiante': estudiante,
        'empresa': est_data['empresa']
    })

# 4. Crear prácticas para los estudiantes
print("\n4. Creando prácticas asignadas al docente...")

fecha_inicio = date.today() - timedelta(days=30)
fecha_fin = fecha_inicio + timedelta(days=120)

for idx, est_info in enumerate(estudiantes_creados, 1):
    estudiante = est_info['estudiante']
    empresa = est_info['empresa']

    # Verificar si ya tiene una práctica activa
    practica_existente = Practica.objects.filter(
        estudiante=estudiante,
        estado='EN_CURSO'
    ).first()

    if practica_existente:
        print(f"   ⚠ {estudiante.usuario.get_full_name()} ya tiene práctica: {practica_existente}")
        continue

    # Crear práctica
    practica = Practica.objects.create(
        estudiante=estudiante,
        numero=1,  # Primera práctica
        docente_asesor=docente,
        instructor=instructor,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado='EN_CURSO',
        observaciones=f'Práctica en {empresa.nombre}'
    )

    print(f"   ✓ Práctica creada: {estudiante.usuario.get_full_name()} (asignada a docente)")

# 5. Resumen
print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"\n✓ Empresas creadas/verificadas: 3")
print(f"✓ Estudiantes creados/verificados: {len(estudiantes_creados)}")
print(f"✓ Prácticas asignadas al docente: {Practica.objects.filter(docente_asesor=docente).count()}")

print("\n" + "=" * 60)
print("CREDENCIALES DE ACCESO")
print("=" * 60)
print("\nDOCENTE:")
print(f"  Usuario: dr_garcia")
print(f"  Contraseña: 123456")

print("\nESTUDIANTES:")
for est_data in estudiantes_data:
    print(f"  Usuario: {est_data['username']}")
    print(f"  Contraseña: 123456")

print("\n" + "=" * 60)
print("¡PROCESO COMPLETADO EXITOSAMENTE!")
print("=" * 60)
print("\nAhora puedes:")
print("1. Iniciar sesión como 'dr_garcia' / '123456'")
print("2. Ver tus estudiantes asignados en el menú 'Estudiantes Asignados'")
print("3. Crear encuentros semanales")
print("4. Crear evaluaciones")
print("\n")

