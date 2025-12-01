from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from .models import Empresa, Vacante, Postulacion
from usuarios.models import Estudiante


@login_required
def empresas_list(request):
    """Lista de empresas"""
    empresas = Empresa.objects.filter(activa=True)
    return render(request, 'empresas_list.html', {'empresas': empresas})


@login_required
def empresa_detail(request, pk):
    """Detalle de una empresa"""
    empresa = get_object_or_404(Empresa, pk=pk)
    vacantes = empresa.vacantes.filter(estado='ACTIVA')
    return render(request, 'empresa_detail.html', {'empresa': empresa, 'vacantes': vacantes})


@login_required
@csrf_protect
def empresa_edit(request, pk):
    """Editar una empresa (solo coordinador)"""
    if not request.user.es_coordinador():
        return JsonResponse({'error': 'No autorizado'}, status=403)

    empresa = get_object_or_404(Empresa, pk=pk)

    if request.method == 'POST':
        # Actualizar datos de la empresa
        empresa.nombre = request.POST.get('nombre')
        empresa.nit = request.POST.get('nit')
        empresa.contacto = request.POST.get('contacto')
        empresa.telefono = request.POST.get('telefono')
        empresa.correo = request.POST.get('correo')
        empresa.direccion = request.POST.get('direccion')
        empresa.ciudad = request.POST.get('ciudad')
        empresa.descripcion = request.POST.get('descripcion')
        empresa.activa = request.POST.get('activa') == 'on'
        empresa.save()

        return redirect('empresas:empresa_detail', pk=empresa.pk)

    return render(request, 'empresa_edit.html', {'empresa': empresa})


@login_required
@csrf_protect
def empresa_create(request):
    """Crear una empresa (solo coordinador)"""
    if not request.user.es_coordinador():
        return JsonResponse({'error': 'No autorizado'}, status=403)

    if request.method == 'POST':
        empresa = Empresa.objects.create(
            nombre=request.POST.get('nombre'),
            nit=request.POST.get('nit'),
            contacto=request.POST.get('contacto'),
            telefono=request.POST.get('telefono'),
            correo=request.POST.get('correo'),
            direccion=request.POST.get('direccion'),
            ciudad=request.POST.get('ciudad'),
            descripcion=request.POST.get('descripcion'),
            activa=request.POST.get('activa') == 'on'
        )
        return redirect('empresas:empresa_detail', pk=empresa.pk)

    return render(request, 'empresa_edit.html', {'empresa': None})


@login_required
def vacantes_list(request):
    """Lista de vacantes disponibles"""
    vacantes = Vacante.objects.filter(estado='ACTIVA')

    # Filtros opcionales
    empresa = request.GET.get('empresa')
    modalidad = request.GET.get('modalidad')

    if empresa:
        vacantes = vacantes.filter(empresa__id=empresa)
    if modalidad:
        vacantes = vacantes.filter(modalidad=modalidad)

    return render(request, 'vacantes_list.html', {'vacantes': vacantes})


@login_required
def vacante_detail(request, pk):
    """Detalle de una vacante"""
    vacante = get_object_or_404(Vacante, pk=pk)
    return render(request, 'vacante_detail.html', {'vacante': vacante})


@login_required
@csrf_protect
def vacante_create(request, empresa_pk=None):
    """Crear una vacante (solo coordinador)"""
    if not request.user.es_coordinador():
        return JsonResponse({'error': 'No autorizado'}, status=403)

    # Si se proporciona empresa_pk, pre-seleccionar esa empresa
    empresa_seleccionada = None
    if empresa_pk:
        empresa_seleccionada = get_object_or_404(Empresa, pk=empresa_pk)

    if request.method == 'POST':
        empresa = Empresa.objects.get(pk=request.POST.get('empresa'))
        vacante = Vacante.objects.create(
            empresa=empresa,
            titulo=request.POST.get('titulo'),
            descripcion=request.POST.get('descripcion'),
            perfil_requerido=request.POST.get('perfil_requerido'),
            modalidad=request.POST.get('modalidad'),
            duracion_meses=request.POST.get('duracion_meses'),
            salario_rango=request.POST.get('salario_rango', ''),
            cantidad_plazas=request.POST.get('cantidad_plazas'),
            fecha_inicio_estimada=request.POST.get('fecha_inicio_estimada'),
            fecha_fin_estimada=request.POST.get('fecha_fin_estimada'),
            estado='ACTIVA'
        )
        return redirect('empresas:empresa_detail', pk=empresa.pk)

    empresas = Empresa.objects.filter(activa=True)
    return render(request, 'vacante_form.html', {
        'empresas': empresas,
        'empresa_seleccionada': empresa_seleccionada,
        'vacante': None
    })


@login_required
@csrf_protect
def vacante_edit(request, pk):
    """Editar una vacante (solo coordinador)"""
    if not request.user.es_coordinador():
        return JsonResponse({'error': 'No autorizado'}, status=403)

    vacante = get_object_or_404(Vacante, pk=pk)

    if request.method == 'POST':
        vacante.empresa = Empresa.objects.get(pk=request.POST.get('empresa'))
        vacante.titulo = request.POST.get('titulo')
        vacante.descripcion = request.POST.get('descripcion')
        vacante.perfil_requerido = request.POST.get('perfil_requerido')
        vacante.modalidad = request.POST.get('modalidad')
        vacante.duracion_meses = request.POST.get('duracion_meses')
        vacante.salario_rango = request.POST.get('salario_rango', '')
        vacante.cantidad_plazas = request.POST.get('cantidad_plazas')
        vacante.fecha_inicio_estimada = request.POST.get('fecha_inicio_estimada')
        vacante.fecha_fin_estimada = request.POST.get('fecha_fin_estimada')
        vacante.estado = request.POST.get('estado')
        vacante.save()

        return redirect('empresas:empresa_detail', pk=vacante.empresa.pk)

    empresas = Empresa.objects.filter(activa=True)
    return render(request, 'vacante_form.html', {
        'empresas': empresas,
        'empresa_seleccionada': vacante.empresa,
        'vacante': vacante
    })


@login_required
def postulaciones_list(request):
    """Lista de postulaciones para el coordinador"""
    if not request.user.es_coordinador():
        return JsonResponse({'error': 'No autorizado'}, status=403)

    # Obtener todas las postulaciones con información relacionada
    postulaciones = Postulacion.objects.select_related(
        'estudiante__usuario',
        'vacante__empresa'
    ).order_by('-fecha_postulacion')

    # Filtros opcionales
    estado = request.GET.get('estado')
    if estado:
        postulaciones = postulaciones.filter(estado=estado)

    # Estadísticas
    total_postulaciones = Postulacion.objects.count()
    pendientes = Postulacion.objects.filter(estado='EN_REVISION').count()
    aceptadas = Postulacion.objects.filter(estado='ACEPTADA').count()
    rechazadas = Postulacion.objects.filter(estado='RECHAZADA').count()

    context = {
        'postulaciones': postulaciones,
        'total_postulaciones': total_postulaciones,
        'pendientes': pendientes,
        'aceptadas': aceptadas,
        'rechazadas': rechazadas,
    }

    return render(request, 'postulaciones_list.html', context)


@login_required
def postulacion_detail(request, pk):
    """Detalle de una postulación"""
    postulacion = get_object_or_404(Postulacion, pk=pk)

    # Validar acceso
    if not (request.user.es_coordinador() or request.user.id == postulacion.estudiante.usuario.id):
        return JsonResponse({'error': 'No autorizado'}, status=403)

    return render(request, 'postulacion_detail.html', {'postulacion': postulacion})


@login_required
@csrf_protect
def postulacion_create(request):
    """Crear una postulación"""
    if not request.user.es_estudiante():
        return JsonResponse({'error': 'No autorizado'}, status=403)

    estudiante = request.user.perfil_estudiante

    # Validar hoja de vida aprobada
    if estudiante.estado_hv != 'APROBADA':
        return JsonResponse({'error': 'Tu hoja de vida no ha sido aprobada aún'}, status=400)

    # Validar límite de postulaciones por empresa
    if request.method == 'POST':
        vacante = Vacante.objects.get(pk=request.POST.get('vacante'))

        # Verificar si ya existe postulación a esta empresa
        existing = Postulacion.objects.filter(
            estudiante=estudiante,
            vacante__empresa=vacante.empresa
        ).exists()

        if existing:
            return JsonResponse({'error': 'Ya tienes una postulación activa a esta empresa'}, status=400)

        postulacion = Postulacion.objects.create(
            estudiante=estudiante,
            vacante=vacante,
            origen='ESTUDIANTE',
            estado='EN_REVISION'
        )
        return redirect('empresas:postulacion_detail', pk=postulacion.pk)

    vacantes = Vacante.objects.filter(estado='ACTIVA')

    # Obtener el estudiante para verificar estado de hoja de vida
    context = {
        'vacantes': vacantes,
    }

    return render(request, 'postulacion_form.html', context)


@login_required
@csrf_protect
@require_http_methods(["POST"])
def actualizar_estado_postulacion(request, pk):
    """Actualizar estado de una postulación (solo coordinador)"""
    if not request.user.es_coordinador():
        return JsonResponse({'error': 'No autorizado'}, status=403)

    postulacion = get_object_or_404(Postulacion, pk=pk)
    nuevo_estado = request.POST.get('estado')

    if nuevo_estado in ['EN_REVISION', 'ACEPTADA', 'RECHAZADA']:
        postulacion.estado = nuevo_estado
        if nuevo_estado == 'RECHAZADA':
            postulacion.motivo_rechazo = request.POST.get('motivo_rechazo', '')
        postulacion.save()
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Estado inválido'}, status=400)
