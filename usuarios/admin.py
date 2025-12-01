from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Estudiante, DocenteAsesor, Instructor


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'rol', 'activo')
    list_filter = ('rol', 'activo', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('rol', 'telefono', 'activo')}),
    )


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('get_nombre', 'programa_academico', 'semestre', 'estado_hv', 'practica_actual')
    list_filter = ('estado_hv', 'semestre', 'programa_academico')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'programa_academico')

    def get_nombre(self, obj):
        return obj.usuario.get_full_name()
    get_nombre.short_description = 'Nombre'


@admin.register(DocenteAsesor)
class DocenteAsesorAdmin(admin.ModelAdmin):
    list_display = ('get_nombre', 'departamento')
    list_filter = ('departamento',)
    search_fields = ('usuario__first_name', 'usuario__last_name')

    def get_nombre(self, obj):
        return obj.usuario.get_full_name()
    get_nombre.short_description = 'Nombre'


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('get_nombre', 'empresa', 'cargo')
    list_filter = ('empresa',)
    search_fields = ('usuario__first_name', 'usuario__last_name', 'empresa__nombre')

    def get_nombre(self, obj):
        return obj.usuario.get_full_name()
    get_nombre.short_description = 'Nombre'

