# 🎓 Sistema de Gestión de Prácticas Profesionales

Sistema web desarrollado con Django para la gestión integral de prácticas profesionales universitarias.

## 📋 Descripción

Plataforma que permite gestionar el ciclo completo de prácticas profesionales, incluyendo:
- Gestión de estudiantes, docentes e instructores
- Publicación y postulación a vacantes
- Seguimiento de prácticas
- Evaluaciones y encuentros
- Gestión documental (hojas de vida)
- Reportes y estadísticas

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.12 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (recomendado)

### Paso 1: Clonar o Descargar el Proyecto

```bash
cd "C:\Users\1208j\OneDrive\Desktop\proyecto nuclear"
```

### Paso 2: Crear y Activar Entorno Virtual

#### En Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Si hay problemas con permisos en PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Paso 3: Instalar Dependencias

```powershell
pip install -r requirements.txt
```

### Paso 4: Configurar Base de Datos

```powershell
python manage.py makemigrations
python manage.py migrate
```

### Paso 5: Crear Usuarios de Prueba

```powershell
python crear_usuarios_simple.py
```

### Paso 6: Iniciar el Servidor

```powershell
python manage.py runserver
```

El sistema estará disponible en: **http://127.0.0.1:8000/**

---

## 👥 Usuarios del Sistema

### 🔐 Credenciales de Acceso

| Rol | Usuario | Contraseña | Descripción |
|-----|---------|------------|-------------|
| **Coordinador** | `coordinador` | `123456` | Administrador del sistema con acceso completo |
| **Estudiante** | `ana_martinez` | `123456` | Estudiante de Ingeniería de Sistemas (7mo semestre) |
| **Docente** | `dr_garcia` | `123456` | Docente asesor del departamento de Ingeniería |
| **Instructor** | `instructor_techcorp` | `123456` | Instructor empresarial - Jefe de Práctica |

### 📧 Correos Electrónicos

- **Coordinador**: coordinador@universidad.edu
- **Estudiante**: ana@universidad.edu
- **Docente**: garcia@universidad.edu
- **Instructor**: instructor@techcorp.com

---

## 🎯 Funcionalidades por Rol

### 👨‍💼 Coordinador de Prácticas
- ✅ Dashboard con estadísticas generales
- ✅ Gestión de empresas (crear, editar, eliminar)
- ✅ Publicación de vacantes
- ✅ Gestión de prácticas
- ✅ Revisión y aprobación de documentos
- ✅ Gestión de postulaciones
- ✅ Generación de reportes (Excel/PDF)
- ✅ Envío de encuestas
- ✅ Visualización de estadísticas avanzadas

### 👨‍🎓 Estudiante
- ✅ Dashboard personal
- ✅ Visualización de vacantes disponibles
- ✅ Postulación a vacantes
- ✅ Subir hoja de vida y documentos
- ✅ Ver mis documentos
- ✅ Seguimiento de prácticas
- ✅ Completar evaluaciones
- ✅ Ver perfil personal

### 👨‍🏫 Docente Asesor
- ✅ Dashboard de estudiantes asignados
- ✅ Visualización de estudiantes
- ✅ Visualización de prácticas
- ✅ Creación de encuentros de seguimiento
- ✅ Evaluaciones de estudiantes
- ✅ Revisión de documentos

### 👨‍💼 Instructor Empresarial
- ✅ Dashboard de practicantes
- ✅ Visualización de practicantes asignados
- ✅ Creación de encuentros
- ✅ Evaluaciones de desempeño
- ✅ Gestión de actividades

---

## 📂 Estructura del Proyecto

```
proyecto nuclear/
├── config/                 # Configuración principal de Django
│   ├── settings.py        # Configuraciones del proyecto
│   ├── urls.py            # URLs principales
│   ├── middleware.py      # Middleware personalizado
│   └── wsgi.py            # WSGI para despliegue
│
├── usuarios/              # Aplicación de gestión de usuarios
│   ├── models.py          # Modelos: Usuario, Estudiante, Docente, Instructor
│   ├── views.py           # Vistas y lógica de negocio
│   ├── urls.py            # Rutas de la aplicación
│   └── admin.py           # Panel de administración
│
├── empresas/              # Aplicación de gestión empresarial
│   ├── models.py          # Modelos: Empresa, Vacante, Postulacion
│   ├── views.py           # Vistas de vacantes y postulaciones
│   └── urls.py            # Rutas de empresas
│
├── practicas/             # Aplicación de gestión de prácticas
│   ├── models.py          # Modelos: Practica, Encuentro, Evaluacion
│   ├── views.py           # Vistas de prácticas y seguimiento
│   └── urls.py            # Rutas de prácticas
│
├── encuestas/             # Aplicación de encuestas
│   ├── models.py          # Modelos de encuestas
│   ├── views.py           # Vistas de encuestas
│   └── urls.py            # Rutas de encuestas
│
├── notificaciones/        # Aplicación de notificaciones
│   └── models.py          # Sistema de notificaciones
│
├── templates/             # Plantillas HTML
│   ├── base.html          # Plantilla base
│   ├── login.html         # Login
│   ├── dashboard*.html    # Dashboards por rol
│   ├── profile.html       # Perfil de usuario
│   ├── mis_documentos.html # Documentos del estudiante
│   └── ...                # Otras plantillas
│
├── static/                # Archivos estáticos
│   ├── css/               # Hojas de estilo
│   └── js/                # JavaScript
│
├── media/                 # Archivos subidos
│   └── hojas_vida/        # Hojas de vida
│
├── manage.py              # Script de gestión de Django
├── requirements.txt       # Dependencias del proyecto
├── db.sqlite3             # Base de datos SQLite
│
└── Scripts de utilidad:
    ├── crear_usuarios_simple.py           # Crear usuarios básicos
    ├── crear_estudiantes_con_practicas.py # Crear datos de prueba
    ├── eliminar_duplicados.py             # Limpiar duplicados
    └── check_user.py                      # Verificar usuarios
```

---

## 🔧 Scripts Útiles

### Crear Usuarios Básicos
```powershell
python crear_usuarios_simple.py
```
Crea los 4 usuarios principales del sistema.

### Verificar Usuarios
```powershell
python check_user.py
```
Muestra todos los usuarios registrados.

### Eliminar Duplicados
```powershell
python eliminar_duplicados.py
```
Limpia usuarios duplicados del sistema.

### Crear Datos de Prueba Completos
```powershell
python crear_estudiantes_con_practicas.py
```
Crea estudiantes con prácticas asignadas (requiere usuarios básicos).

---

## 🌐 URLs Principales

### Autenticación
- Login: `http://127.0.0.1:8000/login/`
- Logout: `http://127.0.0.1:8000/logout/`
- Registro: `http://127.0.0.1:8000/register/`

### Dashboards
- Coordinador: `http://127.0.0.1:8000/dashboard/coordinador/`
- Estudiante: `http://127.0.0.1:8000/dashboard/estudiante/`
- Docente: `http://127.0.0.1:8000/dashboard/docente/`
- Instructor: `http://127.0.0.1:8000/dashboard/instructor/`

### Gestión
- Empresas: `http://127.0.0.1:8000/api/empresas/empresas/`
- Vacantes: `http://127.0.0.1:8000/api/empresas/vacantes/`
- Prácticas: `http://127.0.0.1:8000/api/practicas/practicas/`
- Perfil: `http://127.0.0.1:8000/api/usuarios/perfil/`
- Mis Documentos: `http://127.0.0.1:8000/api/usuarios/mis-documentos/`

### Panel Administrativo
- Admin: `http://127.0.0.1:8000/admin/`
  - Usuario: `coordinador`
  - Contraseña: `123456`

---

## 📦 Dependencias Principales

```
Django==5.2.8                    # Framework web
djangorestframework==3.16.1      # API REST
django-cors-headers==4.9.0       # CORS
pillow==12.0.0                   # Manejo de imágenes
openpyxl==3.1.2                  # Exportación Excel
reportlab==4.0.9                 # Generación PDF
python-dotenv==1.0.1             # Variables de entorno
psycopg2-binary==2.9.10          # PostgreSQL (producción)
gunicorn==23.0.0                 # Servidor WSGI (producción)
redis==5.0.1                     # Cache
```

---

## 🎨 Características de la Interfaz

- ✨ Diseño moderno y responsivo
- 🎨 Sidebar colapsible con navegación intuitiva
- 📊 Gráficos y estadísticas en tiempo real
- 📱 Compatible con dispositivos móviles
- 🌙 Interfaz con colores profesionales
- ✅ Feedback visual para acciones del usuario
- 🔔 Sistema de notificaciones

---

## 🔒 Seguridad

- ✅ Autenticación basada en sesiones Django
- ✅ Protección CSRF habilitada
- ✅ Validación de permisos por rol
- ✅ Sanitización de inputs
- ✅ Gestión segura de archivos subidos

---

## 📝 Flujo de Trabajo Típico

### Para Estudiantes:
1. **Login** con credenciales (`ana_martinez` / `123456`)
2. **Subir hoja de vida** en "Mis Documentos"
3. **Explorar vacantes** disponibles
4. **Postularse** a vacantes de interés
5. **Ver estado** de postulaciones
6. **Completar evaluaciones** cuando sea necesario

### Para Coordinadores:
1. **Login** con credenciales (`coordinador` / `123456`)
2. **Gestionar empresas** - Agregar/editar empresas
3. **Publicar vacantes** para estudiantes
4. **Revisar documentos** - Aprobar hojas de vida
5. **Gestionar postulaciones** - Asignar prácticas
6. **Generar reportes** - Exportar datos
7. **Ver estadísticas** del programa

### Para Docentes:
1. **Login** con credenciales (`dr_garcia` / `123456`)
2. **Ver estudiantes** asignados
3. **Crear encuentros** de seguimiento
4. **Evaluar estudiantes**
5. **Revisar documentos**

### Para Instructores:
1. **Login** con credenciales (`instructor_techcorp` / `123456`)
2. **Ver practicantes** asignados
3. **Registrar encuentros**
4. **Evaluar desempeño**

---

## 🐛 Solución de Problemas Comunes

### Error: "No module named 'django'"
```powershell
pip install -r requirements.txt
```

### Error: "No such table"
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Error: "Port already in use"
```powershell
# Usar otro puerto
python manage.py runserver 8001
```

### Error de permisos en PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### No aparecen usuarios después de crearlos
```powershell
# Recrear usuarios
python crear_usuarios_simple.py
```

---

## 📊 Base de Datos

El proyecto usa **SQLite** para desarrollo (archivo `db.sqlite3`).

### Reiniciar Base de Datos
```powershell
# CUIDADO: Esto elimina todos los datos
Remove-Item db.sqlite3
python manage.py migrate
python crear_usuarios_simple.py
```

---

## 🚀 Despliegue en Producción

### Configuración recomendada:
1. Cambiar a PostgreSQL
2. Configurar variables de entorno (`.env`)
3. Usar `gunicorn` como servidor WSGI
4. Configurar servidor web (Nginx/Apache)
5. Habilitar HTTPS
6. Configurar backups automáticos

---

## 📞 Soporte

Para problemas o consultas sobre el sistema:
- Verificar este README
- Revisar los logs en consola
- Ejecutar scripts de diagnóstico (`check_user.py`)

---

## 📄 Licencia

Proyecto educativo para gestión de prácticas profesionales.

---

## 🎓 Notas Importantes

- **Contraseñas de prueba**: Todas son `123456` (cambiar en producción)
- **Datos de prueba**: Los usuarios creados son ficticios
- **Archivos subidos**: Se almacenan en `media/hojas_vida/`
- **Base de datos**: SQLite para desarrollo, usar PostgreSQL en producción
- **Debug mode**: Está activado, desactivar en producción

---

## 🔄 Actualización del Sistema

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Aplicar migraciones
python manage.py migrate

# Reiniciar servidor
python manage.py runserver
```

---

## ✅ Checklist de Inicio Rápido

- [ ] Python 3.12+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Migraciones aplicadas (`python manage.py migrate`)
- [ ] Usuarios creados (`python crear_usuarios_simple.py`)
- [ ] Servidor iniciado (`python manage.py runserver`)
- [ ] Acceso a http://127.0.0.1:8000/login/
- [ ] Login exitoso con cualquier usuario de prueba

---

**¡Sistema listo para usar! 🎉**

Para comenzar, ejecuta:
```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

Luego visita: http://127.0.0.1:8000/login/

# Proyecto-nuclear
