from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils import timezone
from .models import Encuesta, PreguntaEncuesta, RespuestaEncuesta


@login_required
@ensure_csrf_cookie
def encuestas_list(request):
    """Lista de encuestas disponibles para el usuario"""
    ahora = timezone.now()
    encuestas = Encuesta.objects.filter(
        activa=True,
        fecha_inicio__lte=ahora,
        fecha_fin__gte=ahora
    )

    # Filtrar por rol del usuario
    rol_usuario = request.user.rol.lower()
    encuestas_filtradas = []

    for encuesta in encuestas:
        roles = [r.strip().lower() for r in encuesta.dirigida_a_roles.split(',')]
        if rol_usuario in roles or 'todos' in roles:
            encuestas_filtradas.append(encuesta)

    return render(request, 'encuestas_list.html', {'encuestas': encuestas_filtradas})


@login_required
@ensure_csrf_cookie
def encuesta_detail(request, pk):
    """Detalle de una encuesta"""
    encuesta = get_object_or_404(Encuesta, pk=pk)
    preguntas = encuesta.preguntas.all().order_by('orden')
    return render(request, 'encuesta_detail.html', {'encuesta': encuesta, 'preguntas': preguntas})


@login_required
@csrf_protect
def responder_encuesta(request, pk):
    """Responder una encuesta"""
    encuesta = get_object_or_404(Encuesta, pk=pk)
    preguntas = encuesta.preguntas.all().order_by('orden')

    if request.method == 'POST':
        practica_id = request.POST.get('practica_id')

        for pregunta in preguntas:
            respuesta_texto = request.POST.get(f'pregunta_{pregunta.id}_texto')
            respuesta_valor = request.POST.get(f'pregunta_{pregunta.id}_valor')

            # Evitar duplicados
            RespuestaEncuesta.objects.filter(
                encuesta=encuesta,
                pregunta=pregunta,
                usuario=request.user
            ).delete()

            if respuesta_texto or respuesta_valor:
                RespuestaEncuesta.objects.create(
                    encuesta=encuesta,
                    pregunta=pregunta,
                    usuario=request.user,
                    practica_id=practica_id if practica_id else None,
                    respuesta_texto=respuesta_texto,
                    respuesta_valor=int(respuesta_valor) if respuesta_valor else None
                )

        return redirect('encuestas_list')

    return render(request, 'responder_encuesta.html', {'encuesta': encuesta, 'preguntas': preguntas})


@login_required
@csrf_protect
def encuesta_create(request):
    """Crear una encuesta (solo coordinador)"""
    if not request.user.es_coordinador():
        return JsonResponse({'error': 'No autorizado'}, status=403)

    if request.method == 'POST':
        encuesta = Encuesta.objects.create(
            titulo=request.POST.get('titulo'),
            descripcion=request.POST.get('descripcion'),
            dirigida_a_roles=request.POST.get('dirigida_a_roles'),
            activa=request.POST.get('activa') == 'on',
            fecha_inicio=request.POST.get('fecha_inicio'),
            fecha_fin=request.POST.get('fecha_fin'),
            creada_por=request.user
        )
        return redirect('encuesta_detail', pk=encuesta.pk)

    return render(request, 'encuesta_form.html')


@login_required
def encuesta_resultados(request, pk):
    """Ver resultados de una encuesta (solo coordinador)"""
    if not request.user.es_coordinador():
        return JsonResponse({'error': 'No autorizado'}, status=403)

    encuesta = get_object_or_404(Encuesta, pk=pk)
    preguntas = encuesta.preguntas.all().order_by('orden')
    respuestas = RespuestaEncuesta.objects.filter(encuesta=encuesta)

    context = {
        'encuesta': encuesta,
        'preguntas': preguntas,
        'respuestas': respuestas,
        'total_respondentes': respuestas.values('usuario').distinct().count()
    }

    return render(request, 'encuesta_resultados.html', context)

