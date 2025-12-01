from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Opciones para roles
ROLES = (
    ('ESTUDIANTE', 'Estudiante'),
    ('COORDINADOR', 'Coordinador de Prácticas'),
    ('DOCENTE', 'Docente Asesor'),
    ('INSTRUCTOR', 'Instructor/Tutor Empresarial'),
)

# Opciones para estado de hoja de vida
ESTADO_HV = (
    ('PENDIENTE', 'Pendiente'),
    ('APROBADA', 'Aprobada'),
    ('RECHAZADA', 'Rechazada'),
)


class Usuario(AbstractUser):
    """Modelo personalizado de usuario con roles específicos"""
    rol = models.CharField(max_length=20, choices=ROLES, default='ESTUDIANTE')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"

    def es_coordinador(self):
        return self.rol == 'COORDINADOR'

    def es_estudiante(self):
        return self.rol == 'ESTUDIANTE'

    def es_docente(self):
        return self.rol == 'DOCENTE'

    def es_instructor(self):
        return self.rol == 'INSTRUCTOR'


class Estudiante(models.Model):
    """Información adicional del estudiante"""
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_estudiante')
    programa_academico = models.CharField(max_length=100)
    semestre = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    hv_archivo = models.FileField(
        upload_to='hojas_vida/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    estado_hv = models.CharField(max_length=20, choices=ESTADO_HV, default='PENDIENTE')
    observaciones_hv = models.TextField(blank=True, null=True)
    practica_actual = models.IntegerField(default=1)  # 1-5
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['usuario__last_name']

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.programa_academico}"


class DocenteAsesor(models.Model):
    """Información del docente asesor"""
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_docente')
    departamento = models.CharField(max_length=100, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['usuario__last_name']

    def __str__(self):
        return f"Dr./Dra. {self.usuario.get_full_name()}"


class Instructor(models.Model):
    """Información del instructor/tutor empresarial"""
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_instructor')
    empresa = models.ForeignKey('empresas.Empresa', on_delete=models.SET_NULL, null=True, blank=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['usuario__last_name']

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.empresa}"

