"""
Middleware personalizado para garantizar que CSRF funcione correctamente
"""
from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token


class CSRFFixMiddleware(MiddlewareMixin):
    """
    Middleware que asegura que el token CSRF se envíe correctamente
    """

    def process_request(self, request):
        # Asegurar que se genere el token CSRF para todas las peticiones
        get_token(request)
        return None


