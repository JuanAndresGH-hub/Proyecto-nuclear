from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField

TIPO_PREGUNTA = (
    ('ESCALA', 'Escala (1-5)'),
    ('OPCION_MULTIPLE', 'Opción Múltiple'),
    ('TEXTO', 'Texto Abierto'),
    ('SI_NO', 'Sí/No'),
)

DESTINATARIOS = (
    ('ESTUDIANTE', 'Estudiante'),
    ('DOCENTE', 'Docente Asesor'),
    ('INSTRUCTOR', 'Instructor'),
)


class Encuesta(models.Model):
    """Modelo de encuesta de satisfacción"""
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    dirigida_a_roles = models.CharField(
        max_length=100,
        help_text="Roles destinatarios separados por comas"
    )
    activa = models.BooleanField(default=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creada_por = models.ForeignKey('usuarios.Usuario', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo


class PreguntaEncuesta(models.Model):
    """Modelo de pregunta dentro de una encuesta"""
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='preguntas')
    orden = models.IntegerField(default=0)
    texto = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_PREGUNTA, default='ESCALA')
    requerida = models.BooleanField(default=True)
    opciones = models.TextField(
        blank=True,
        null=True,
        help_text="Para opción múltiple, separar con | (ej: Opción1|Opción2|Opción3)"
    )

    class Meta:
        ordering = ['encuesta', 'orden']

    def __str__(self):
        return f"{self.encuesta.titulo} - Q{self.orden}"


class RespuestaEncuesta(models.Model):
    """Modelo para registrar respuestas de encuestas"""
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='respuestas')
    pregunta = models.ForeignKey(PreguntaEncuesta, on_delete=models.CASCADE, related_name='respuestas')
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    practica = models.ForeignKey('practicas.Practica', on_delete=models.SET_NULL, null=True, blank=True)
    respuesta_texto = models.TextField(blank=True, null=True)
    respuesta_valor = models.IntegerField(blank=True, null=True)  # Para escalas
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_respuesta']
        unique_together = ('encuesta', 'pregunta', 'usuario')

    def __str__(self):
        return f"Respuesta de {self.usuario.get_full_name()} a {self.encuesta.titulo}"

