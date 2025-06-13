let allData = [];
let filteredData = [];

$(document).ready(function () {
    $('#filterEspecie, #filterRaza').select2({
        placeholder: "Seleccionar...",
        allowClear: true,
        width: '100%',
        closeOnSelect: false,
        minimumResultsForSearch: 0,
        tags: false
    }).on('select2:select', function () {
        $(this).data('select2').$dropdown.find('.select2-search__field').focus();
    });

    $('#filterEspecie, #filterRaza')
        .on('select2:unselecting', function (e) {
            $(this).data('prevent-open', true);
        })
        .on('select2:opening', function (e) {
            if ($(this).data('prevent-open')) {
                e.preventDefault();
                $(this).removeData('prevent-open');
            }
        });

    $.ajax({
        url: "/api/pacientes",
        method: "GET",
        dataType: "json",
        success: function (data) {
            console.log("Datos recibidos:", data);
            allData = data;
            filteredData = allData;
            popularFiltros();
            actualizarStatsCards();
            aplicarFiltrosYGraficos();
        },
        error: function (xhr, status, error) {
            console.error("Error al cargar los datos:", error);
        }
    });

    $('#filterEspecie, #filterRaza').on('change', function () {
        aplicarFiltrosYGraficos();
    });

    $('#searchTitle').on('input', function () {
        aplicarFiltrosYGraficos();
    });

    $('.period-btn').on('click', function () {
        $('.period-btn').removeClass('active');
        $(this).addClass('active');
        renderGraficos(filteredData);
    });
});

function popularFiltros() {
    const params = {
        especie: $('#filterEspecie').val() || [],
        raza: $('#filterRaza').val() || []
    };

    $.ajax({
        url: '/api/filtros',
        method: 'GET',
        data: params,
        traditional: true,
        success: function (res) {
            actualizarCombo('#filterEspecie', res.especies, params.especie);
            actualizarCombo('#filterRaza', res.razas, params.raza);
        },
        error: function (err) {
            console.error("Error al cargar filtros:", err);
        }
    });
}

function actualizarCombo(id, valores, valoresActuales) {
    const select = $(id);
    select.empty();
    valores.forEach(v => select.append(`<option value="${v}">${v}</option>`));
    select.val(valoresActuales);
    select.trigger('change.select2');
}

function actualizarStatsCards() {
    const totalPacientes = filteredData.length;
    const especiesCount = {};
    const edades = filteredData.map(d => parseInt(d.edad) || 0).filter(e => e > 0);
    const promedioEdad = edades.length > 0 ? (edades.reduce((sum, e) => sum + e, 0) / edades.length).toFixed(1) : 'N/A';
    const apoderadosCount = {};

    filteredData.forEach(d => {
        especiesCount[d.especie] = (especiesCount[d.especie] || 0) + 1;
        apoderadosCount[d.id_apoderado] = (apoderadosCount[d.id_apoderado] || 0) + 1;
    });

    const especiePopular = Object.keys(especiesCount).reduce((a, b) => especiesCount[a] > especiesCount[b] ? a : b, 'N/A');

    $('#totalPacientes').text(totalPacientes);
    $('#totalPacientesVar').text(totalPacientes > 0 ? '↑ Total Pacientes' : '—').addClass(totalPacientes > 0 ? 'positive' : '');
    $('#especiePopular').text(especiePopular);
    $('#promedioEdad').text(promedioEdad);
    $('#promedioEdadVar').text('Edad Promedio');
}

function aplicarFiltrosYGraficos() {
    const especie = $('#filterEspecie').val() || [];
    const raza = $('#filterRaza').val() || [];
    const search = $('#searchTitle').val().toLowerCase();

    filteredData = allData.filter(d =>
        (especie.length === 0 || especie.includes(d.especie)) &&
        (raza.length === 0 || raza.includes(d.raza)) &&
        (!search || d.nombre.toLowerCase().includes(search))
    );

    cargarTabla(filteredData);
    actualizarStatsCards();
    renderGraficos(filteredData);
}

function cargarTabla(data) {
    const tabla = $('#tablaDatos').DataTable();
    tabla.clear().destroy();

    const cuerpo = data.map(d => [
        d.id,
        d.nombre,
        d.especie,
        d.raza,
        d.fecha_nacimiento || 'N/A',
        d.edad,
        d.id_apoderado
    ]);

    $('#tablaDatos').DataTable({
        data: cuerpo,
        columns: [
            { title: "ID" },
            { title: "Nombre" },
            { title: "Especie" },
            { title: "Raza" },
            { title: "Fecha Nacimiento" },
            { title: "Edad", className: "text-end" },
            { title: "ID Apoderado", className: "text-end" }
        ],
        responsive: true
    });
}

function renderGraficos(data) {
    ['pacientesPorEspecie', 'pacientesPorRaza', 'pacientesPorEdad', 'graficoRadar', 'pacientesPorApoderado'].forEach(id => {
        Chart.getChart(id)?.destroy();
    });

    const pacientesEspecie = {}, pacientesRaza = {}, pacientesEdad = {}, pacientesApoderado = {};

    data.forEach(d => {
        pacientesEspecie[d.especie] = (pacientesEspecie[d.especie] || 0) + 1;
        pacientesRaza[d.raza] = (pacientesRaza[d.raza] || 0) + 1;
        const edad = parseInt(d.edad) || 0;
        if (edad > 0) {
            pacientesEdad[edad] = (pacientesEdad[edad] || 0) + 1;
        }
        pacientesApoderado[d.id_apoderado] = (pacientesApoderado[d.id_apoderado] || 0) + 1;
    });

    // Chart 1: Pacientes por Especie (Bar)
    new Chart(document.getElementById('pacientesPorEspecie'), {
        type: 'bar',
        data: {
            labels: Object.keys(pacientesEspecie),
            datasets: [{
                label: 'Pacientes por Especie',
                data: Object.values(pacientesEspecie),
                backgroundColor: '#6A5ACD'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Pacientes por Especie',
                    font: { size: 18 }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let value = context.raw || 0;
                            return `${context.dataset.label}: ${value}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Número de Pacientes'
                    }
                }
            }
        }
    });

    // Chart 2: Pacientes por Raza (Pie)
    new Chart(document.getElementById('pacientesPorRaza'), {
        type: 'pie',
        data: {
            labels: Object.keys(pacientesRaza),
            datasets: [{
                label: 'Pacientes por Raza',
                data: Object.values(pacientesRaza),
                backgroundColor: [
                    '#6A5ACD', '#FFA500', '#4682B4', '#FF6384', '#FFCE56',
                    '#9966FF', '#4BC0C0', '#C9CBCF', '#8E44AD', '#F39C12'
                ],
                borderColor: '#FFFFFF',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Distribución de Pacientes por Raza',
                    font: { size: 18 }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.label || '';
                            let value = context.raw || 0;
                            let total = context.dataset.data.reduce((a, b) => a + b, 0);
                            let percentage = total > 0 ? ((value / total) * 100).toFixed(2) : 0;
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                },
                legend: {
                    position: 'bottom',
                    labels: { boxWidth: 20, font: { size: 12 } }
                }
            }
        }
    });

    // Chart 3: Pacientes por Edad (Line)
    const edades = Object.keys(pacientesEdad).sort((a, b) => a - b);
    new Chart(document.getElementById('pacientesPorEdad'), {
        type: 'line',
        data: {
            labels: edades,
            datasets: [{
                label: 'Pacientes por Edad',
                data: edades.map(e => pacientesEdad[e] || 0),
                fill: false,
                borderColor: '#FFA500',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Pacientes por Edad',
                    font: { size: 18 }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let value = context.raw || 0;
                            return `${context.dataset.label}: ${value}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Número de Pacientes'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Edad'
                    }
                }
            }
        }
    });

    // Chart 4: Pacientes por Especie (Radar)
    new Chart(document.getElementById('graficoRadar'), {
        type: 'radar',
        data: {
            labels: Object.keys(pacientesEspecie),
            datasets: [{
                label: 'Pacientes por Especie',
                data: Object.values(pacientesEspecie),
                backgroundColor: 'rgba(106, 90, 205, 0.5)',
                borderColor: '#6A5ACD',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Pacientes por Especie',
                    font: { size: 18 }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let value = context.raw || 0;
                            return `${context.dataset.label}: ${value}`;
                        }
                    }
                }
            }
        }
    });

    // Chart 5: Pacientes por Apoderado (Horizontal Bar)
    const topApoderados = Object.entries(pacientesApoderado)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
    new Chart(document.getElementById('pacientesPorApoderado'), {
        type: 'bar',
        data: {
            labels: topApoderados.map(a => `Apoderado ${a[0]}`),
            datasets: [{
                label: 'Pacientes por Apoderado',
                data: topApoderados.map(a => a[1]),
                backgroundColor: '#FFA500'
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Top 10 Apoderados por Número de Pacientes',
                    font: { size: 18 }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let value = context.raw || 0;
                            return `${context.dataset.label}: ${value}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Número de Pacientes'
                    }
                }
            }
        }
    });
}

$('#toggleTheme').on('click', function () {
    const html = document.documentElement;
    const isDark = html.getAttribute('data-bs-theme') === 'dark';
    html.setAttribute('data-bs-theme', isDark ? 'light' : 'dark');
    this.textContent = isDark ? 'Modo Claro 🌞' : 'Modo Oscuro 🌙';
});

window.addEventListener('load', function () {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = 'none';
    }
});


