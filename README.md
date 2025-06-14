Esta aplicación es un **Sistema de Gestión de Clínica Veterinaria** construido con Flask que maneja registros de pacientes, autenticación de usuarios y análisis de datos a través de un dashboard interactivo.

## Estructura General de la Aplicación

La aplicación sigue una arquitectura de tres capas con separación clara entre presentación, lógica de negocio y datos:

### Backend (Flask)
El archivo principal `app.py` contiene toda la lógica del servidor [1](#0-0) . La aplicación utiliza:

- **Flask-Login** para manejo de sesiones [2](#0-1) 
- **SQLAlchemy** para operaciones de base de datos [3](#0-2) 
- **PostgreSQL** como base de datos principal hospedada en Render

### Frontend
La interfaz utiliza:
- **Bootstrap 5** para diseño responsivo
- **jQuery** para manipulación del DOM y peticiones AJAX
- **Chart.js** para visualización de datos
- **DataTables** para tablas interactivas

## Funcionalidades Principales

### 1. Sistema de Autenticación
La aplicación maneja dos tipos de usuarios con diferentes permisos:

- **Administradores**: Acceso completo a operaciones CRUD de pacientes [4](#0-3) 
- **Usuarios regulares**: Solo visualización del dashboard

El proceso de autenticación verifica credenciales y establece sesiones [5](#0-4) .

### 2. Gestión de Pacientes (Solo Administradores)
Los administradores pueden realizar operaciones CRUD completas:

- **Crear pacientes** mediante `POST /add/pacientes` [6](#0-5) 
- **Actualizar pacientes** con `PUT /upd/pacientes/<id>` [7](#0-6) 
- **Eliminar pacientes** usando `DELETE /del/pacientes/<id>` [8](#0-7) 

### 3. Dashboard Interactivo
El dashboard carga datos mediante AJAX y proporciona:

- **Visualizaciones**: 5 tipos de gráficos diferentes (barras, circular, línea, radar, barras horizontales) [9](#0-8) 
- **Filtros dinámicos**: Por especie y raza usando Select2 [10](#0-9) 
- **Estadísticas en tiempo real**: Tarjetas que muestran métricas calculadas [11](#0-10) 

### 4. Sistema de Contacto
La página principal incluye un formulario de contacto que permite a visitantes enviar mensajes [12](#0-11) . Los mensajes se procesan mediante JavaScript [13](#0-12) .

## Flujo de Datos

1. **Carga inicial**: El dashboard solicita datos de pacientes via `/api/pacientes` [14](#0-13) 
2. **Procesamiento**: Los datos se almacenan en variables globales y se procesan para generar visualizaciones
3. **Filtrado**: Los usuarios pueden filtrar datos dinámicamente, actualizando gráficos y tablas en tiempo real
4. **CRUD**: Los administradores pueden modificar datos mediante formularios que envían peticiones AJAX [15](#0-14) 

## Estructura de Archivos

- `app.py`: Servidor Flask principal con todas las rutas
- `templates/`: Plantillas HTML con Jinja2
- `static/js/`: Lógica JavaScript del cliente
- `static/css/`: Estilos personalizados y responsive design
- `models/`: Modelos de datos SQLAlchemy

## Notes

La aplicación está configurada para despliegue en la nube con variables de entorno para la clave secreta y puerto [16](#0-15) . El sistema implementa control de acceso basado en roles, asegurando que solo los administradores puedan modificar datos de pacientes, mientras que todos los usuarios autenticados pueden visualizar el dashboard analítico.

Wiki pages you might want to explore:
- [Overview (SantiagoMO138/examen_final_fkask)](/wiki/SantiagoMO138/examen_final_fkask#1)
- [System Architecture (SantiagoMO138/examen_final_fkask)](/wiki/SantiagoMO138/examen_final_fkask#2)
- [Dashboard & Analytics (SantiagoMO138/examen_final_fkask)](/wiki/SantiagoMO138/examen_final_fkask#3.3)
