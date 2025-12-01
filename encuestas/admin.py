from django.contrib import admin
from .models import Encuesta, PreguntaEncuesta, RespuestaEncuesta


@admin.register(Encuesta)
class EncuestaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'dirigida_a_roles', 'activa', 'fecha_inicio', 'fecha_fin')
    list_filter = ('activa', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion')


@admin.register(PreguntaEncuesta)
class PreguntaEncuestaAdmin(admin.ModelAdmin):
    list_display = ('orden', 'get_encuesta', 'tipo', 'requerida')
    list_filter = ('tipo', 'requerida')
    search_fields = ('encuesta__titulo', 'texto')

    def get_encuesta(self, obj):
        return obj.encuesta.titulo
    get_encuesta.short_description = 'Encuesta'


@admin.register(RespuestaEncuesta)
class RespuestaEncuestaAdmin(admin.ModelAdmin):
    list_display = ('get_usuario', 'get_encuesta', 'get_pregunta', 'respuesta_valor', 'fecha_respuesta')
    list_filter = ('encuesta', 'fecha_respuesta')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'encuesta__titulo')
    readonly_fields = ('fecha_respuesta',)

    def get_usuario(self, obj):
        return obj.usuario.get_full_name()
    get_usuario.short_description = 'Usuario'

    def get_encuesta(self, obj):
        return obj.encuesta.titulo
    get_encuesta.short_description = 'Encuesta'

    def get_pregunta(self, obj):
        return f"Q{obj.pregunta.orden}"
    get_pregunta.short_description = 'Pregunta'

