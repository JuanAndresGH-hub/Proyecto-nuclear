from django.db import models
from django.utils import timezone

ESTADO_VACANTE = (
    ('ACTIVA', 'Activa'),
    ('CERRADA', 'Cerrada'),
)

ESTADO_POSTULACION = (
    ('EN_REVISION', 'En Revisión'),
    ('ACEPTADA', 'Aceptada'),
    ('RECHAZADA', 'Rechazada'),
)

ORIGEN_POSTULACION = (
    ('ESTUDIANTE', 'Postulación del Estudiante'),
    ('COORDINADOR', 'Asignación del Coordinador'),
)


class Empresa(models.Model):
    """Modelo de empresa que ofrece prácticas"""
    nombre = models.CharField(max_length=255, unique=True)
    nit = models.CharField(max_length=20, blank=True, null=True, unique=True)
    contacto = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.nombre


class Vacante(models.Model):
    """Modelo de vacante de práctica en una empresa"""
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='vacantes')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    perfil_requerido = models.TextField()
    modalidad = models.CharField(
        max_length=20,
        choices=[('PRESENCIAL', 'Presencial'), ('HIBRIDO', 'Híbrido'), ('REMOTO', 'Remoto')],
        default='PRESENCIAL'
    )
    duracion_meses = models.IntegerField(default=6)
    salario_rango = models.CharField(max_length=100, blank=True, null=True)
    cantidad_plazas = models.IntegerField(default=1)
    fecha_inicio_estimada = models.DateField()
    fecha_fin_estimada = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_VACANTE, default='ACTIVA')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.titulo} - {self.empresa.nombre}"


class Postulacion(models.Model):
    """Modelo de postulación de estudiante a una vacante"""
    estudiante = models.ForeignKey('usuarios.Estudiante', on_delete=models.CASCADE, related_name='postulaciones')
    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE, related_name='postulaciones')
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    origen = models.CharField(max_length=20, choices=ORIGEN_POSTULACION, default='ESTUDIANTE')
    estado = models.CharField(max_length=20, choices=ESTADO_POSTULACION, default='EN_REVISION')
    motivo_rechazo = models.TextField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('estudiante', 'vacante')
        ordering = ['-fecha_postulacion']

    def __str__(self):
        return f"{self.estudiante.usuario.get_full_name()} -> {self.vacante.titulo}"

