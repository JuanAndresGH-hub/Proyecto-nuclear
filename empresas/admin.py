from django.contrib import admin
from .models import Empresa, Vacante, Postulacion


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'ciudad', 'correo', 'activa')
    list_filter = ('activa', 'ciudad')
    search_fields = ('nombre', 'nit', 'correo')


@admin.register(Vacante)
class VacanteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'modalidad', 'duracion_meses', 'estado', 'cantidad_plazas')
    list_filter = ('estado', 'modalidad', 'empresa', 'fecha_creacion')
    search_fields = ('titulo', 'empresa__nombre')


@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ('get_estudiante', 'get_vacante', 'origen', 'estado', 'fecha_postulacion')
    list_filter = ('estado', 'origen', 'fecha_postulacion')
    search_fields = ('estudiante__usuario__first_name', 'estudiante__usuario__last_name', 'vacante__titulo')
    readonly_fields = ('fecha_postulacion', 'fecha_actualizacion')

    def get_estudiante(self, obj):
        return obj.estudiante.usuario.get_full_name()
    get_estudiante.short_description = 'Estudiante'

    def get_vacante(self, obj):
        return obj.vacante.titulo
    get_vacante.short_description = 'Vacante'

