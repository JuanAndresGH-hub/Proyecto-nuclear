from django.urls import path
from . import views

app_name = 'empresas'

urlpatterns = [
    # Empresas
    path('empresas/', views.empresas_list, name='empresas_list'),
    path('empresas/<int:pk>/', views.empresa_detail, name='empresa_detail'),
    path('empresas/<int:pk>/editar/', views.empresa_edit, name='empresa_edit'),
    path('empresas/crear/', views.empresa_create, name='empresa_create'),

    # Vacantes
    path('vacantes/', views.vacantes_list, name='vacantes_list'),
    path('vacantes/<int:pk>/', views.vacante_detail, name='vacante_detail'),
    path('vacantes/crear/', views.vacante_create, name='vacante_create'),
    path('vacantes/<int:pk>/editar/', views.vacante_edit, name='vacante_edit'),
    path('empresas/<int:empresa_pk>/vacantes/crear/', views.vacante_create, name='vacante_create_from_empresa'),

    # Postulaciones
    path('postulaciones/', views.postulaciones_list, name='postulaciones_list'),
    path('postulaciones/<int:pk>/', views.postulacion_detail, name='postulacion_detail'),
    path('postulaciones/crear/', views.postulacion_create, name='postulacion_create'),
    path('postulaciones/<int:pk>/actualizar-estado/', views.actualizar_estado_postulacion, name='actualizar_estado_postulacion'),
]

