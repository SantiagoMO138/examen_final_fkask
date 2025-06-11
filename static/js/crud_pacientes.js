$(document).ready(function () {
    $.ajax({
        url: "/api/list_pacientes",
        method: "GET",
        dataType: "json",
        success: function (data) {
            cargarTabla(data);
        },
        error: function (xhr, status, error) {
            console.error("Error al cargar los datos:", error);
            if (xhr.status === 403) {
                mostrarToast('🚫 Acceso denegado: Solo administradores', 'danger');
            } else {
                mostrarToast('❌ Error al cargar los datos', 'danger');
            }
        }
    });
    cargarOpcionesFormulario();
});

function cargarTabla(data) {
    const cuerpo = data.map(d => [
        d.id,
        d.nombre,
        d.especie,
        d.raza,
        d.fecha_nacimiento || 'N/A',
        d.edad,
        d.id_apoderado
    ]);

    $('#tablaPacientes').DataTable({
        data: cuerpo,
        columns: [
            { title: "ID", visible: false },
            { title: "Nombre" },
            { title: "Especie" },
            { title: "Raza" },
            { title: "Fecha Nacimiento" },
            { title: "Edad", className: "text-end" },
            { title: "ID Apoderado", className: "text-end" },
            {
                title: "Acciones",
                orderable: false,
                searchable: false,
                className: "text-center",
                render: function (data, type, row) {
                    const id = row[0];
                    return `
                        <button class="btn btn-sm btn-warning btn-editar me-1">
                            <i class="fas fa-edit"></i> Editar
                        </button>
                        <button class="btn btn-sm btn-danger btn-eliminar" data-id="${id}">
                            <i class="fas fa-trash-alt"></i> Eliminar
                        </button>`;
                }
            }
        ],
        responsive: true
    });
}

function cargarOpcionesFormulario() {
    $.ajax({
        url: '/api/opciones',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            llenarCombo('#addEspecie', data.especies);
            llenarCombo('#addRaza', data.razas);
            llenarCombo('#addApoderado', data.apoderados);
            llenarCombo('#editarEspecie', data.especies);
            llenarCombo('#editarRaza', data.razas);
            llenarCombo('#editarApoderado', data.apoderados);
        },
        error: function () {
            console.error("Error al cargar combos");
            mostrarToast('❌ Error al cargar opciones', 'danger');
        }
    });
}

function llenarCombo(selector, valores) {
    const select = $(selector);
    select.empty();
    select.append('<option value="">-- Seleccione --</option>');
    valores.forEach(v => {
        select.append(`<option value="${v}">${v}</option>`);
    });
}

// Agregar Paciente
$('#formAgregar').on('submit', function (e) {
    e.preventDefault();

    const datos = {
        nombre: this.nombre.value,
        especie: this.especie.value,
        raza: this.raza.value,
        fecha_nacimiento: this.fecha_nacimiento.value || null,
        edad: parseInt(this.edad.value),
        id_apoderado: parseInt(this.apoderado.value)
    };

    $.ajax({
        url: '/add/pacientes',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(datos),
        success: function (response) {
            $('#modalAgregar').modal('hide');
            $('#formAgregar')[0].reset();
            $('#tablaPacientes').DataTable().destroy();
            cargarDatos();
            mostrarToast('🐾 Paciente agregado con éxito', 'success');
        },
        error: function (xhr) {
            if (xhr.status === 403) {
                mostrarToast('🚫 Acceso denegado: Solo administradores', 'danger');
            } else {
                mostrarToast('❌ Error al agregar el paciente', 'danger');
            }
        }
    });
});

function cargarDatos() {
    $('#loader').removeClass('d-none');
    $.ajax({
        url: "/api/list_pacientes",
        method: "GET",
        dataType: "json",
        success: function (data) {
            $('#tablaPacientes').DataTable().clear().destroy();
            cargarTabla(data);
        },
        error: function (xhr) {
            if (xhr.status === 403) {
                mostrarToast('🚫 Acceso denegado: Solo administradores', 'danger');
            } else {
                mostrarToast('❌ Error al cargar datos', 'danger');
            }
        },
        complete: function () {
            $('#loader').addClass('d-none');
        }
    });
}

function mostrarToast(mensaje, tipo = 'primary') {
    const toastEl = $('#toastNotificacion');
    const toastBody = $('#toastMensaje');

    toastEl.removeClass('bg-primary bg-success bg-danger bg-warning');
    toastEl.addClass(`bg-${tipo}`);
    toastBody.text(mensaje);

    const toast = new bootstrap.Toast(toastEl[0]);
    toast.show();
}

// Eliminar Paciente
$('#tablaPacientes').on('click', '.btn-eliminar', function () {
    const id = $(this).data('id');
    if (confirm("¿Estás seguro de eliminar este paciente?")) {
        $.ajax({
            url: `/del/pacientes/${id}`,
            method: 'DELETE',
            success: function () {
                mostrarToast('❌ Paciente eliminado', 'danger');
                cargarDatos();
            },
            error: function (xhr) {
                if (xhr.status === 403) {
                    mostrarToast('🚫 Acceso denegado: Solo administradores', 'danger');
                } else {
                    mostrarToast('❌ Error al eliminar', 'danger');
                }
            }
        });
    }
});

// Editar Paciente
$('#tablaPacientes').on('click', '.btn-editar', function () {
    const row = $(this).closest('tr');
    const data = $('#tablaPacientes').DataTable().row(row).data();

    $('#editarId').val(data[0]);
    $('#editarNombre').val(data[1]);
    $('#editarEspecie').val(data[2]);
    $('#editarRaza').val(data[3]);
    $('#editarFechaNacimiento').val(data[4] === 'N/A' ? '' : data[4]);
    $('#editarEdad').val(data[5]);
    $('#editarApoderado').val(data[6]);

    const modal = new bootstrap.Modal(document.getElementById('modalEditar'));
    modal.show();
});

// Guardar Cambios Edición
$('#formEditar').on('submit', function (e) {
    e.preventDefault();
    const id = $('#editarId').val();

    const datos = {
        nombre: $('#editarNombre').val(),
        especie: $('#editarEspecie').val(),
        raza: $('#editarRaza').val(),
        fecha_nacimiento: $('#editarFechaNacimiento').val() || null,
        edad: parseInt($('#editarEdad').val()),
        id_apoderado: parseInt($('#editarApoderado').val())
    };

    $.ajax({
        url: `/upd/pacientes/${id}`,
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(datos),
        success: function () {
            $('#modalEditar').modal('hide');
            mostrarToast('✏️ Paciente actualizado', 'warning');
            cargarDatos();
        },
        error: function (xhr) {
            if (xhr.status === 403) {
                mostrarToast('🚫 Acceso denegado: Solo administradores', 'danger');
            } else {
                mostrarToast('❌ Error al actualizar', 'danger');
            }
        }
    });
});