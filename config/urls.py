"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from usuarios.views import (login_view, logout_view, dashboard_estudiante,
                            dashboard_docente, dashboard_instructor, dashboard_coordinador,
                            profile_view, update_profile_view)
from empresas.views import vacantes_list

urlpatterns = [
    path('', login_view, name='home'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile_view, name='update_profile'),
    path('vacantes/', vacantes_list, name='vacantes_list'),
    path('dashboard/estudiante/', dashboard_estudiante, name='dashboard_estudiante'),
    path('dashboard/docente/', dashboard_docente, name='dashboard_docente'),
    path('dashboard/instructor/', dashboard_instructor, name='dashboard_instructor'),
    path('dashboard/coordinador/', dashboard_coordinador, name='dashboard_coordinador'),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/empresas/', include('empresas.urls')),
    path('api/practicas/', include('practicas.urls')),
    path('api/encuestas/', include('encuestas.urls')),
    path('api/notificaciones/', include('notificaciones.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

