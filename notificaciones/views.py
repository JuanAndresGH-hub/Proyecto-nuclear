from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import Notificacion


@login_required
def notificaciones_list(request):
    """Lista de notificaciones del usuario"""
    notificaciones = Notificacion.objects.filter(usuario_destino=request.user).order_by('-fecha_creacion')
    no_leidas = notificaciones.filter(leida=False).count()

    return render(request, 'notificaciones_list.html', {
        'notificaciones': notificaciones,
        'no_leidas': no_leidas
    })


@login_required
def notificacion_detail(request, pk):
    """Detalle de una notificación"""
    notificacion = get_object_or_404(Notificacion, pk=pk)

    # Validar que la notificación sea del usuario
    if notificacion.usuario_destino != request.user:
        return JsonResponse({'error': 'No autorizado'}, status=403)

    # Marcar como leída
    if not notificacion.leida:
        notificacion.marcar_como_leida()

    return render(request, 'notificacion_detail.html', {'notificacion': notificacion})


@login_required
@require_http_methods(["POST"])
def marcar_leida(request, pk):
    """Marcar una notificación como leída"""
    notificacion = get_object_or_404(Notificacion, pk=pk)

    if notificacion.usuario_destino != request.user:
        return JsonResponse({'error': 'No autorizado'}, status=403)

    notificacion.marcar_como_leida()
    return JsonResponse({'success': True})


@login_required
@require_http_methods(["POST"])
def marcar_todas_leidas(request):
    """Marcar todas las notificaciones como leídas"""
    notificaciones = Notificacion.objects.filter(
        usuario_destino=request.user,
        leida=False
    )

    for notificacion in notificaciones:
        notificacion.marcar_como_leida()

    return JsonResponse({'success': True, 'count': notificaciones.count()})

