from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from .models import Practica, EncuentroSemanal, Evaluacion, ProyectoPractica


@login_required
@ensure_csrf_cookie
def practicas_list(request):
    """Lista de prácticas del estudiante o todas (coordinador)"""
    if request.user.es_coordinador():
        practicas = Practica.objects.all()
    elif request.user.es_estudiante():
        estudiante = request.user.perfil_estudiante
        practicas = estudiante.practicas.all()
    elif request.user.es_docente():
        docente = request.user.perfil_docente
        practicas = Practica.objects.filter(docente_asesor=docente)
    elif request.user.es_instructor():
        instructor = request.user.perfil_instructor
        practicas = Practica.objects.filter(instructor=instructor)
    else:
        return JsonResponse({'error': 'No autorizado'}, status=403)

    return render(request, 'practicas_list.html', {'practicas': practicas})


@login_required
def practica_detail(request, pk):
    """Detalle de una práctica"""
    practica = get_object_or_404(Practica, pk=pk)

    # Validar acceso
    if not (request.user.es_coordinador() or
            (request.user.es_estudiante() and request.user.id == practica.estudiante.usuario.id) or
            (request.user.es_docente() and request.user.perfil_docente.id == practica.docente_asesor.id) or
            (request.user.es_instructor() and request.user.perfil_instructor.id == practica.instructor.id)):
        return JsonResponse({'error': 'No autorizado'}, status=403)

    context = {
        'practica': practica,
        'encuentros': practica.encuentros.all(),
        'evaluaciones': practica.evaluaciones.all(),
    }

    if hasattr(practica, 'proyecto'):
        context['proyecto'] = practica.proyecto

    return render(request, 'practica_detail.html', context)


@login_required
@require_http_methods(["POST"])
def actualizar_estado_practica(request, pk):
    """Actualizar estado de una práctica (solo coordinador)"""
    if not request.user.es_coordinador():
        return JsonResponse({'error': 'No autorizado'}, status=403)

    practica = get_object_or_404(Practica, pk=pk)
    nuevo_estado = request.POST.get('estado')

    estados_validos = ['NO_INICIADA', 'EN_CURSO', 'EN_PAUSA', 'FINALIZADA', 'REPROBADA']
    if nuevo_estado in estados_validos:
        practica.estado = nuevo_estado
        practica.save()
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Estado inválido'}, status=400)


@login_required
def encuentros_list(request):
    """Lista de encuentros semanales"""
    if request.user.es_coordinador():
        encuentros = EncuentroSemanal.objects.all()
    elif request.user.es_estudiante():
        estudiante = request.user.perfil_estudiante
        encuentros = EncuentroSemanal.objects.filter(practica__estudiante=estudiante)
    elif request.user.es_docente():
        docente = request.user.perfil_docente
        encuentros = EncuentroSemanal.objects.filter(practica__docente_asesor=docente)
    else:
        return JsonResponse({'error': 'No autorizado'}, status=403)

    return render(request, 'encuentros_list.html', {'encuentros': encuentros})


@login_required
def encuentro_detail(request, pk):
    """Detalle de un encuentro"""
    encuentro = get_object_or_404(EncuentroSemanal, pk=pk)
    return render(request, 'encuentro_detail.html', {'encuentro': encuentro})


@login_required
@csrf_protect
def encuentro_create(request):
    """Crear un encuentro semanal (solo docente asesor)"""
    if not request.user.es_docente():
        return JsonResponse({'error': 'No autorizado'}, status=403)

    if request.method == 'POST':
        practica = Practica.objects.get(pk=request.POST.get('practica'))
        encuentro = EncuentroSemanal.objects.create(
            practica=practica,
            fecha=request.POST.get('fecha'),
            hora_inicio=request.POST.get('hora_inicio') if request.POST.get('hora_inicio') else None,
            hora_fin=request.POST.get('hora_fin') if request.POST.get('hora_fin') else None,
            tema=request.POST.get('tema'),
            descripcion=request.POST.get('descripcion'),
            acuerdos=request.POST.get('acuerdos', ''),
            registrado_por_docente=request.user.perfil_docente,
        )
        return redirect('practicas:encuentro_detail', pk=encuentro.pk)

    docente = request.user.perfil_docente
    practicas = Practica.objects.filter(docente_asesor=docente, estado='EN_CURSO')
    return render(request, 'encuentro_form.html', {'practicas': practicas})


@login_required
def evaluaciones_list(request):
    """Lista de evaluaciones"""
    if request.user.es_coordinador():
        evaluaciones = Evaluacion.objects.all()
    elif request.user.es_estudiante():
        estudiante = request.user.perfil_estudiante
        evaluaciones = Evaluacion.objects.filter(practica__estudiante=estudiante)
    elif request.user.es_docente():
        docente = request.user.perfil_docente
        evaluaciones = Evaluacion.objects.filter(practica__docente_asesor=docente)
    elif request.user.es_instructor():
        instructor = request.user.perfil_instructor
        evaluaciones = Evaluacion.objects.filter(practica__instructor=instructor)
    else:
        return JsonResponse({'error': 'No autorizado'}, status=403)

    evaluaciones = evaluaciones.select_related('practica__estudiante__usuario').order_by('-fecha_evaluacion')
    return render(request, 'evaluaciones_list.html', {'evaluaciones': evaluaciones})


@login_required
@csrf_protect
def evaluacion_create(request):
    """Crear una evaluación"""
    if not (request.user.es_docente() or request.user.es_instructor()):
        return JsonResponse({'error': 'No autorizado'}, status=403)

    if request.method == 'POST':
        practica = Practica.objects.get(pk=request.POST.get('practica'))

        evaluacion = Evaluacion.objects.create(
            practica=practica,
            tipo_evaluador='DOCENTE' if request.user.es_docente() else 'INSTRUCTOR',
            evaluador_id=request.user.id,
            nota=request.POST.get('nota'),
            rubro=request.POST.get('rubro', 'Desempeño General'),
            comentarios=request.POST.get('comentarios', ''),
        )

        # Recalcular promedio
        practica.calcular_promedio()

        return redirect('practicas:practica_detail', pk=practica.pk)

    # Obtener prácticas según el rol
    if request.user.es_docente():
        practicas = Practica.objects.filter(docente_asesor=request.user.perfil_docente, estado='EN_CURSO')
    else:
        practicas = Practica.objects.filter(instructor=request.user.perfil_instructor, estado='EN_CURSO')

    practicas = practicas.select_related('estudiante__usuario', 'vacante__empresa')

    return render(request, 'evaluacion_form.html', {'practicas': practicas})


@login_required
def proyecto_detail(request, pk):
    """Detalle del proyecto de práctica"""
    proyecto = get_object_or_404(ProyectoPractica, pk=pk)
    return render(request, 'proyecto_detail.html', {'proyecto': proyecto})


@login_required
def proyecto_update(request, pk):
    """Actualizar proyecto de práctica"""
    proyecto = get_object_or_404(ProyectoPractica, pk=pk)

    # Solo el estudiante o coordinador pueden actualizar
    if not (request.user.es_coordinador() or request.user.id == proyecto.practica.estudiante.usuario.id):
        return JsonResponse({'error': 'No autorizado'}, status=403)

    if request.method == 'POST':
        proyecto.titulo = request.POST.get('titulo', proyecto.titulo)
        proyecto.descripcion = request.POST.get('descripcion', proyecto.descripcion)
        proyecto.objetivos = request.POST.get('objetivos', proyecto.objetivos)
        proyecto.actividades = request.POST.get('actividades', proyecto.actividades)
        proyecto.cronograma = request.POST.get('cronograma', proyecto.cronograma)
        proyecto.competencias_desarrolladas = request.POST.get('competencias_desarrolladas', proyecto.competencias_desarrolladas)

        if 'registro_archivo' in request.FILES:
            proyecto.registro_archivo = request.FILES['registro_archivo']
        if 'informe_final_archivo' in request.FILES:
            proyecto.informe_final_archivo = request.FILES['informe_final_archivo']

        proyecto.save()
        return redirect('proyecto_detail', pk=proyecto.pk)

    return render(request, 'proyecto_form.html', {'proyecto': proyecto})

