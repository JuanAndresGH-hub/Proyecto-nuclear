from django.db import models

TIPO_NOTIFICACION = (
    ('ASIGNACION_DOCENTE', 'Asignación de Docente Asesor'),
    ('CAMBIO_ESTADO_PRACTICA', 'Cambio de Estado de Práctica'),
    ('POSTULACION_ACEPTADA', 'Postulación Aceptada'),
    ('POSTULACION_RECHAZADA', 'Postulación Rechazada'),
    ('HOJA_VIDA_APROBADA', 'Hoja de Vida Aprobada'),
    ('HOJA_VIDA_RECHAZADA', 'Hoja de Vida Rechazada'),
    ('ENCUENTRO_PROGRAMADO', 'Encuentro Programado'),
    ('RECORDATORIO_ENCUENTRO', 'Recordatorio de Encuentro'),
    ('RESULTADO_EVALUACION', 'Resultado de Evaluación'),
    ('OTROS', 'Otros'),
)


class Notificacion(models.Model):
    """Modelo de notificaciones del sistema"""
    usuario_destino = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=50, choices=TIPO_NOTIFICACION, default='OTROS')
    titulo = models.CharField(max_length=255)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(blank=True, null=True)

    # Relación con entidades relevantes (opcionales)
    practica = models.ForeignKey('practicas.Practica', on_delete=models.SET_NULL, null=True, blank=True)
    postulacion = models.ForeignKey('empresas.Postulacion', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.usuario_destino.get_full_name()}"

    def marcar_como_leida(self):
        """Marca la notificación como leída"""
        if not self.leida:
            from django.utils import timezone
            self.leida = True
            self.fecha_lectura = timezone.now()
            self.save()

