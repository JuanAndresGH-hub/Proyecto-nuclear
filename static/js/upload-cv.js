/**
 * Script para manejar la carga de hoja de vida
 * Versión mejorada con mejor compatibilidad
 */

// Usar DOMContentLoaded Y delegación de eventos para asegurar que funcione
document.addEventListener('DOMContentLoaded', function() {
    console.log('Upload CV script cargado');

    // Buscar el formulario inmediatamente
    attachFormHandler();

    // También buscar cuando se muestre el modal (por si se carga dinámicamente)
    const modalElement = document.getElementById('uploadCVModal');
    if (modalElement) {
        modalElement.addEventListener('shown.bs.modal', function() {
            console.log('Modal mostrado, re-attachando handler');
            attachFormHandler();
        });
    }
});

function attachFormHandler() {
    const uploadForm = document.querySelector('#uploadCVModal form');

    if (uploadForm) {
        console.log('Formulario encontrado, attachando evento submit');

        // Remover listeners anteriores para evitar duplicados
        uploadForm.removeEventListener('submit', handleSubmit);

        // Agregar el nuevo listener
        uploadForm.addEventListener('submit', handleSubmit);
    } else {
        console.log('Formulario NO encontrado');
    }
}

function handleSubmit(e) {
    console.log('Submit event triggered!');

    // Mostrar indicador de carga
    const submitBtn = this.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Subiendo...';
    }

    // El formulario se enviará normalmente (sin preventDefault)
    console.log('Formulario se está enviando...');
}

