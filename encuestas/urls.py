from django.urls import path
from . import views

app_name = 'encuestas'

urlpatterns = [
    # Encuestas
    path('encuestas/', views.encuestas_list, name='encuestas_list'),
    path('encuestas/<int:pk>/', views.encuesta_detail, name='encuesta_detail'),
    path('encuestas/<int:pk>/responder/', views.responder_encuesta, name='responder_encuesta'),
    path('encuestas/crear/', views.encuesta_create, name='encuesta_create'),

    # Estadísticas
    path('encuestas/<int:pk>/resultados/', views.encuesta_resultados, name='encuesta_resultados'),
]

