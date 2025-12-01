from django.contrib import admin
from .models import Notificacion


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('get_usuario', 'tipo', 'leida', 'fecha_creacion')
    list_filter = ('tipo', 'leida', 'fecha_creacion')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'mensaje')
    readonly_fields = ('fecha_creacion', 'fecha_lectura')

    def get_usuario(self, obj):
        return obj.usuario.get_full_name()
    get_usuario.short_description = 'Usuario'

