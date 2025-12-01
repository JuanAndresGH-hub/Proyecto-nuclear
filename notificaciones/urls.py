from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    # Notificaciones
    path('notificaciones/', views.notificaciones_list, name='notificaciones_list'),
    path('notificaciones/<int:pk>/', views.notificacion_detail, name='notificacion_detail'),
    path('notificaciones/<int:pk>/marcar-leida/', views.marcar_leida, name='marcar_leida'),
    path('notificaciones/marcar-todas-leidas/', views.marcar_todas_leidas, name='marcar_todas_leidas'),
]

