from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

ESTADO_PRACTICA = (
    ('NO_INICIADA', 'No Iniciada'),
    ('EN_CURSO', 'En Curso'),
    ('EN_PAUSA', 'En Pausa'),
    ('FINALIZADA', 'Finalizada'),
    ('REPROBADA', 'Reprobada'),
)

TIPO_EVALUADOR = (
    ('DOCENTE', 'Docente Asesor'),
    ('INSTRUCTOR', 'Instructor'),
)


class Practica(models.Model):
    """Modelo de una práctica del estudiante (pueden haber hasta 5)"""
    estudiante = models.ForeignKey('usuarios.Estudiante', on_delete=models.CASCADE, related_name='practicas')
    numero = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    vacante = models.ForeignKey('empresas.Vacante', on_delete=models.SET_NULL, null=True, blank=True)
    docente_asesor = models.ForeignKey('usuarios.DocenteAsesor', on_delete=models.SET_NULL, null=True, blank=True, related_name='practicas_asesoradas')
    instructor = models.ForeignKey('usuarios.Instructor', on_delete=models.SET_NULL, null=True, blank=True, related_name='practicas_tutoriadas')
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_PRACTICA, default='NO_INICIADA')
    promedio_final = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    puede_pasar_a_siguiente = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['estudiante', 'numero']
        unique_together = ('estudiante', 'numero')

    def __str__(self):
        return f"Práctica {self.numero} - {self.estudiante.usuario.get_full_name()}"

    def calcular_promedio(self):
        """Calcula el promedio de la práctica basado en evaluaciones"""
        evaluaciones = self.evaluaciones.all()
        if not evaluaciones.exists():
            return None

        total = sum(ev.nota for ev in evaluaciones)
        promedio = total / evaluaciones.count()
        self.promedio_final = promedio
        self.puede_pasar_a_siguiente = promedio >= 3.5
        self.save()
        return promedio

    def es_aprobada(self):
        """Retorna True si la práctica está aprobada"""
        return self.promedio_final and self.promedio_final >= 3.5


class EncuentroSemanal(models.Model):
    """Modelo de encuentros semanales entre estudiante y docente"""
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE, related_name='encuentros')
    fecha = models.DateField()
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    tema = models.CharField(max_length=255)
    descripcion = models.TextField()
    acuerdos = models.TextField(blank=True, null=True)
    registrado_por_docente = models.ForeignKey('usuarios.DocenteAsesor', on_delete=models.SET_NULL, null=True, blank=True)
    asistencia_estudiante = models.BooleanField(default=True)
    asistencia_docente = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Encuentro {self.practica} - {self.fecha}"


class Evaluacion(models.Model):
    """Modelo de evaluaciones de una práctica"""
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE, related_name='evaluaciones')
    tipo_evaluador = models.CharField(max_length=20, choices=TIPO_EVALUADOR)
    evaluador_id = models.IntegerField()  # FK a Usuario (DocenteAsesor o Instructor)
    nota = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    rubro = models.CharField(max_length=255, default='Desempeño General')
    comentarios = models.TextField(blank=True, null=True)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_evaluacion']

    def __str__(self):
        return f"Evaluación {self.practica} - {self.get_tipo_evaluador_display()}: {self.nota}"


class ProyectoPractica(models.Model):
    """Modelo de proyecto/registro de la práctica"""
    practica = models.OneToOneField(Practica, on_delete=models.CASCADE, related_name='proyecto')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    objetivos = models.TextField()
    actividades = models.TextField()
    registro_archivo = models.FileField(upload_to='proyectos/', blank=True, null=True)
    informe_final_archivo = models.FileField(upload_to='informes/', blank=True, null=True)
    fecha_entrega = models.DateField(blank=True, null=True)
    cronograma = models.TextField(blank=True, null=True)
    competencias_desarrolladas = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proyecto: {self.titulo}"

