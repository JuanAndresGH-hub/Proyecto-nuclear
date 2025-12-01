import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from empresas.models import Empresa, Vacante
from django.utils import timezone

# Crear empresas
empresas_data = [
    {
        'nombre': 'TechCorp S.A.S.',
        'nit': '1234567890',
        'contacto': 'Juan Pérez',
        'telefono': '601-1234567',
        'correo': 'rh@techcorp.com',
        'ciudad': 'Bogotá',
        'descripcion': 'Empresa de desarrollo de software especializada en soluciones web y móviles'
    },
    {
        'nombre': 'Innovación Digital',
        'nit': '9876543210',
        'contacto': 'María González',
        'telefono': '602-9876543',
        'correo': 'contacto@innovaciondigital.com',
        'ciudad': 'Medellín',
        'descripcion': 'Consultora especializada en transformación digital y análisis de datos'
    },
    {
        'nombre': 'Tech Solutions LLC',
        'nit': '5555555555',
        'contacto': 'Carlos López',
        'telefono': '603-5555555',
        'correo': 'info@techsolutions.com',
        'ciudad': 'Cali',
        'descripcion': 'Agencia de desarrollo web y aplicaciones empresariales'
    }
]

empresas = []
for datos in empresas_data:
    empresa, created = Empresa.objects.get_or_create(nombre=datos['nombre'], defaults=datos)
    empresas.append(empresa)
    if created:
        print(f"✓ Empresa creada: {empresa.nombre}")

# Crear vacantes
vacantes_data = [
    {
        'empresa': empresas[0],
        'titulo': 'Practicante de Desarrollo de Software',
        'descripcion': 'Buscamos estudiante para apoyar en desarrollo de aplicaciones web con React y Node.js',
        'perfil_requerido': 'Conocimientos en JavaScript, React, bases de datos. Mínimo 7º semestre.',
        'modalidad': 'HIBRIDO',
        'duracion_meses': 6,
        'salario_rango': '$1,500,000',
        'cantidad_plazas': 2,
        'fecha_inicio_estimada': datetime.now() + timedelta(days=14),
        'fecha_fin_estimada': datetime.now() + timedelta(days=194),
        'estado': 'ACTIVA'
    },
    {
        'empresa': empresas[1],
        'titulo': 'Practicante de Análisis de Datos',
        'descripcion': 'Práctica en análisis de datos y visualización con herramientas modernas',
        'perfil_requerido': 'Conocimientos en Python, SQL, Tableau o Power BI. Mínimo 6º semestre.',
        'modalidad': 'PRESENCIAL',
        'duracion_meses': 5,
        'salario_rango': '$1,200,000',
        'cantidad_plazas': 1,
        'fecha_inicio_estimada': datetime.now() + timedelta(days=7),
        'fecha_fin_estimada': datetime.now() + timedelta(days=157),
        'estado': 'ACTIVA'
    },
    {
        'empresa': empresas[2],
        'titulo': 'Practicante Frontend Junior',
        'descripcion': 'Apoyo en desarrollo de interfaces web modernas y responsivas',
        'perfil_requerido': 'HTML, CSS, JavaScript. Familiaridad con frameworks frontend.',
        'modalidad': 'REMOTO',
        'duracion_meses': 4,
        'salario_rango': '$1,000,000',
        'cantidad_plazas': 3,
        'fecha_inicio_estimada': datetime.now() + timedelta(days=21),
        'fecha_fin_estimada': datetime.now() + timedelta(days=141),
        'estado': 'ACTIVA'
    },
    {
        'empresa': empresas[0],
        'titulo': 'Practicante de QA Testing',
        'descripcion': 'Pruebas de calidad automatizadas y manuales de software',
        'perfil_requerido': 'Conocimientos en testing, preferiblemente Selenium o similares.',
        'modalidad': 'HIBRIDO',
        'duracion_meses': 5,
        'salario_rango': '$1,300,000',
        'cantidad_plazas': 1,
        'fecha_inicio_estimada': datetime.now() + timedelta(days=30),
        'fecha_fin_estimada': datetime.now() + timedelta(days=180),
        'estado': 'ACTIVA'
    }
]

for datos in vacantes_data:
    vacante, created = Vacante.objects.get_or_create(
        empresa=datos['empresa'],
        titulo=datos['titulo'],
        defaults=datos
    )
    if created:
        print(f"✓ Vacante creada: {vacante.titulo}")

print("\n✓ Datos de prueba cargados exitosamente")
print(f"  - Empresas: {len(empresas)}")
print(f"  - Vacantes: {Vacante.objects.count()}")

