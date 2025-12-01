from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update_profile'),

    # Estudiantes
    path('estudiantes/', views.estudiantes_list, name='estudiantes_list'),
    path('estudiantes/<int:pk>/', views.estudiante_detail, name='estudiante_detail'),
    path('estudiantes/<int:pk>/hoja-vida/', views.upload_hoja_vida, name='upload_hoja_vida'),

    # Docentes
    path('docentes/', views.docentes_list, name='docentes_list'),

    # Instructores
    path('instructores/', views.instructores_list, name='instructores_list'),

    # Mis Prácticas, Documentos y Evaluaciones
    path('mis-practicas/', views.mis_practicas, name='mis_practicas'),
    path('mis-practicas/<int:pk>/', views.detalle_practica, name='detalle_practica'),
    path('mis-documentos/', views.mis_documentos, name='mis_documentos'),
    path('mis-evaluaciones/', views.mis_evaluaciones, name='mis_evaluaciones'),

    # Ver documentos de estudiante (para docentes/instructores)
    path('estudiantes/<int:estudiante_id>/documentos/', views.ver_documentos_estudiante, name='ver_documentos_estudiante'),

    # Revisar y aprobar hojas de vida (coordinador)
    path('revisar-hojas-vida/', views.revisar_hojas_vida, name='revisar_hojas_vida'),
    path('estudiantes/<int:estudiante_id>/aprobar-rechazar-hv/', views.aprobar_rechazar_hoja_vida, name='aprobar_rechazar_hoja_vida'),

    # Reportes (coordinador)
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/exportar-estudiantes-excel/', views.exportar_estudiantes_excel, name='exportar_estudiantes_excel'),
    path('reportes/exportar-practicas-pdf/', views.exportar_practicas_pdf, name='exportar_practicas_pdf'),
    path('reportes/estadisticas-avanzadas/', views.estadisticas_avanzadas, name='estadisticas_avanzadas'),
]

