/**
 * Script para manejar CSRF tokens en formularios
 * Asegura que el token CSRF se envíe correctamente en todos los POST
 */

(function() {
    // Obtener el token CSRF de la cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    // Asegurar que el token CSRF se envíe en todos los formularios POST
    const forms = document.querySelectorAll('form[method="POST"]');
    forms.forEach(form => {
        // Si no existe un CSRF token, agregarlo
        if (!form.querySelector('[name="csrfmiddlewaretoken"]')) {
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrftoken;
            form.insertBefore(csrfInput, form.firstChild);
        }
    });

    // Interceptar requests AJAX para agregar el token CSRF
    if (window.fetch) {
        const originalFetch = window.fetch;
        window.fetch = function(url, options = {}) {
            options = options || {};

            // Si es una solicitud POST, PUT, DELETE o PATCH, agregar el token CSRF
            if (['POST', 'PUT', 'DELETE', 'PATCH'].includes((options.method || 'GET').toUpperCase())) {
                options.headers = options.headers || {};
                options.headers['X-CSRFToken'] = csrftoken;
            }

            return originalFetch.apply(this, arguments);
        };
    }

    // Para jQuery si está disponible
    if (typeof jQuery !== 'undefined') {
        jQuery.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!(/^http:/.test(settings.url) || /^https:/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    }
})();

