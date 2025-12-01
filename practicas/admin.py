from django.contrib import admin
from .models import Practica, EncuentroSemanal, Evaluacion, ProyectoPractica


@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    list_display = ('get_estudiante', 'numero', 'get_empresa', 'estado', 'promedio_final', 'puede_pasar_a_siguiente')
    list_filter = ('estado', 'numero', 'fecha_inicio')
    search_fields = ('estudiante__usuario__first_name', 'estudiante__usuario__last_name')

    def get_estudiante(self, obj):
        return obj.estudiante.usuario.get_full_name()
    get_estudiante.short_description = 'Estudiante'

    def get_empresa(self, obj):
        return obj.vacante.empresa.nombre if obj.vacante else 'Sin asignar'
    get_empresa.short_description = 'Empresa'


@admin.register(EncuentroSemanal)
class EncuentroSemanalAdmin(admin.ModelAdmin):
    list_display = ('get_practica', 'fecha', 'tema', 'asistencia_estudiante', 'asistencia_docente')
    list_filter = ('fecha', 'asistencia_estudiante', 'asistencia_docente')
    search_fields = ('practica__estudiante__usuario__first_name', 'tema')

    def get_practica(self, obj):
        return f"Práctica {obj.practica.numero} - {obj.practica.estudiante.usuario.get_full_name()}"
    get_practica.short_description = 'Práctica'


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('get_practica', 'tipo_evaluador', 'nota', 'rubro', 'fecha_evaluacion')
    list_filter = ('tipo_evaluador', 'nota', 'fecha_evaluacion')
    search_fields = ('practica__estudiante__usuario__first_name', 'rubro')

    def get_practica(self, obj):
        return f"Práctica {obj.practica.numero} - {obj.practica.estudiante.usuario.get_full_name()}"
    get_practica.short_description = 'Práctica'


@admin.register(ProyectoPractica)
class ProyectoPracticaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'get_estudiante', 'fecha_entrega')
    list_filter = ('fecha_entrega', 'fecha_creacion')
    search_fields = ('titulo', 'practica__estudiante__usuario__first_name')

    def get_estudiante(self, obj):
        return obj.practica.estudiante.usuario.get_full_name()
    get_estudiante.short_description = 'Estudiante'

