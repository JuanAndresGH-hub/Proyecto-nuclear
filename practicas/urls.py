from django.urls import path
from . import views

app_name = 'practicas'

urlpatterns = [
    # Prácticas
    path('practicas/', views.practicas_list, name='practicas_list'),
    path('practicas/<int:pk>/', views.practica_detail, name='practica_detail'),
    path('practicas/<int:pk>/actualizar-estado/', views.actualizar_estado_practica, name='actualizar_estado_practica'),

    # Encuentros Semanales
    path('encuentros/', views.encuentros_list, name='encuentros_list'),
    path('encuentros/<int:pk>/', views.encuentro_detail, name='encuentro_detail'),
    path('encuentros/crear/', views.encuentro_create, name='encuentro_create'),

    # Evaluaciones
    path('evaluaciones/', views.evaluaciones_list, name='evaluaciones_list'),
    path('evaluaciones/crear/', views.evaluacion_create, name='evaluacion_create'),

    # Proyecto de Práctica
    path('proyectos/<int:pk>/', views.proyecto_detail, name='proyecto_detail'),
    path('proyectos/<int:pk>/actualizar/', views.proyecto_update, name='proyecto_update'),
]

