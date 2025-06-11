// Enviar mensaje de contacto
$('#formMensaje').on('submit', function (e) {
    e.preventDefault();

    const datos = {
        nombre: this.nombre.value,
        telefono: this.telefono.value,
        correo: this.correo.value,
        razon: this.razon.value,
        detalle: this.detalle.value
    };

    $.ajax({
        url: '/add/mensaje',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(datos),
        success: function (response) {
            $('#modalMensaje').modal('hide');
            $('#formMensaje')[0].reset();
            mostrarToast('Mensaje enviado con éxito. ¡Gracias por contactarnos!', 'success');
        },
        error: function () {
            alert('Error al enviar el mensaje. Intenta nuevamente.');
        }
    });
});