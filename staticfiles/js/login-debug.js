/**
 * Debug script para verificar datos del login
 * Agregar esto a la página de login
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form[method="POST"]');

    if (form) {
        form.addEventListener('submit', function(e) {
            const formData = new FormData(form);
            console.log('=== LOGIN FORM SUBMIT DEBUG ===');
            console.log('Form action:', form.action);
            console.log('Form method:', form.method);
            console.log('Form data:');
            for (let [key, value] of formData.entries()) {
                console.log(`  ${key}: ${value.substring(0, 50)}${value.length > 50 ? '...' : ''}`);
            }
            console.log('=== END DEBUG ===');

            // NO prevenir el submit - dejar que continue normalmente
            // NO hay e.preventDefault()
        });
    }
});

