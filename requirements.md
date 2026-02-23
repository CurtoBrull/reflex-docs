# Requirements Document

## Introduction

Sistema web de documentación y aprendizaje para el framework Reflex (Python full-stack framework). El sistema permitirá a usuarios consultar tutoriales, referencias de API, ejemplos interactivos, y gestionar su perfil. Los administradores podrán gestionar el contenido a través de un panel de administración.

## Glossary

- **Sistema**: La aplicación web Django completa "reflex-docs"
- **Usuario**: Persona que accede al sitio web para consultar documentación
- **Usuario_Registrado**: Usuario que ha creado una cuenta en el sistema
- **Administrador**: Usuario con permisos para gestionar contenido a través del panel de administración
- **Tutorial**: Contenido educativo paso a paso almacenado en base de datos
- **Componente**: Documentación de referencia sobre componentes de Reflex
- **Ejemplo_Interactivo**: Código de ejemplo con resaltado de sintaxis
- **Contenedor**: Instancia Docker que ejecuta un servicio del sistema
- **Pipeline_CI**: Proceso automatizado de integración continua en GitHub Actions
- **Pipeline_CD**: Proceso automatizado de despliegue continuo en GitHub Actions

## Requirements

### Requirement 1: Estructura del Proyecto Django

**User Story:** Como desarrollador, quiero una estructura de proyecto Django modular con apps separadas, para que el código esté organizado por funcionalidad.

#### Acceptance Criteria

1. THE Sistema SHALL contener cinco apps Django: core, tutorials, components, playground, accounts
2. THE Sistema SHALL utilizar un directorio "config" para la configuración principal de Django
3. THE Sistema SHALL incluir directorios "static" y "templates" en la raíz del proyecto
4. THE Sistema SHALL utilizar manage.py como punto de entrada de comandos Django
5. THE Sistema SHALL mantener archivos requirements.txt y requirements-dev.txt separados

### Requirement 2: Configuración de Base de Datos

**User Story:** Como desarrollador, quiero utilizar PostgreSQL como base de datos, para que el sistema tenga una base de datos robusta y escalable.

#### Acceptance Criteria

1. THE Sistema SHALL conectarse a PostgreSQL versión 16
2. THE Sistema SHALL leer las credenciales de base de datos desde variables de entorno
3. THE Sistema SHALL utilizar las variables DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
4. WHEN el Sistema inicia, THE Sistema SHALL verificar la conexión a la base de datos
5. THE Sistema SHALL utilizar psycopg2-binary como adaptador de PostgreSQL

### Requirement 3: Gestión de Variables de Entorno

**User Story:** Como desarrollador, quiero gestionar la configuración mediante variables de entorno, para que las credenciales sensibles no estén en el código.

#### Acceptance Criteria

1. THE Sistema SHALL utilizar python-decouple para leer variables de entorno
2. THE Sistema SHALL incluir un archivo .env.example con todas las variables requeridas
3. THE Sistema SHALL leer SECRET_KEY, DEBUG, ALLOWED_HOSTS desde variables de entorno
4. THE Sistema SHALL proporcionar valores por defecto seguros para desarrollo local
5. THE Sistema SHALL excluir el archivo .env del control de versiones

### Requirement 4: Contenedorización con Docker

**User Story:** Como desarrollador, quiero ejecutar el proyecto en contenedores Docker, para que el entorno sea reproducible y portable.

#### Acceptance Criteria

1. THE Sistema SHALL incluir un Dockerfile basado en python:3.12-slim
2. THE Sistema SHALL configurar PYTHONDONTWRITEBYTECODE=1 y PYTHONUNBUFFERED=1
3. THE Sistema SHALL instalar dependencias del sistema: libpq-dev, gcc
4. THE Sistema SHALL utilizar /app como directorio de trabajo
5. THE Sistema SHALL incluir archivos .dockerignore y .gitignore apropiados

### Requirement 5: Entorno de Desarrollo Local

**User Story:** Como desarrollador, quiero levantar el proyecto localmente con un comando, para que pueda desarrollar rápidamente.

#### Acceptance Criteria

1. THE Sistema SHALL incluir un archivo docker-compose.yml para desarrollo
2. WHEN se ejecuta "docker compose up --build", THE Sistema SHALL iniciar la base de datos y el servidor web
3. THE Sistema SHALL montar el código fuente como volumen para hot reload
4. THE Sistema SHALL exponer el servidor de desarrollo en el puerto 8000
5. THE Sistema SHALL exponer PostgreSQL en el puerto 5432
6. THE Sistema SHALL crear un volumen persistente para los datos de PostgreSQL

### Requirement 6: Entorno de Producción

**User Story:** Como administrador de sistemas, quiero desplegar el proyecto en producción con Docker Compose, para que el sistema esté listo para usuarios reales.

#### Acceptance Criteria

1. THE Sistema SHALL incluir un archivo docker-compose.prod.yml para producción
2. WHEN se inicia en producción, THE Sistema SHALL ejecutar migraciones automáticamente
3. WHEN se inicia en producción, THE Sistema SHALL ejecutar collectstatic automáticamente
4. THE Sistema SHALL utilizar Gunicorn como servidor WSGI en producción
5. THE Sistema SHALL incluir un servicio Nginx como reverse proxy
6. THE Sistema SHALL configurar restart: always para todos los servicios
7. THE Sistema SHALL compartir archivos estáticos entre web y nginx mediante volumen

### Requirement 7: Servicio de Archivos Estáticos

**User Story:** Como usuario, quiero que los archivos estáticos se sirvan eficientemente, para que la página cargue rápidamente.

#### Acceptance Criteria

1. THE Sistema SHALL configurar STATIC_ROOT para collectstatic
2. THE Sistema SHALL configurar STATICFILES_DIRS apuntando a /static
3. WHERE el entorno es producción, THE Nginx SHALL servir archivos estáticos directamente
4. THE Sistema SHALL incluir TailwindCSS mediante CDN
5. THE Sistema SHALL incluir highlight.js para resaltado de código

### Requirement 8: Pipeline de Integración Continua

**User Story:** Como desarrollador, quiero que el código se valide automáticamente en cada PR, para que se detecten errores antes de fusionar.

#### Acceptance Criteria

1. WHEN se crea un pull request hacia main o develop, THE Pipeline_CI SHALL ejecutarse automáticamente
2. THE Pipeline_CI SHALL utilizar ubuntu-latest como runner
3. THE Pipeline_CI SHALL configurar un servicio PostgreSQL 16 con health check
4. THE Pipeline_CI SHALL instalar Python 3.12 y las dependencias
5. THE Pipeline_CI SHALL ejecutar flake8 con max-line-length 120
6. THE Pipeline_CI SHALL ejecutar python manage.py test
7. IF algún paso falla, THEN THE Pipeline_CI SHALL marcar el PR como fallido

### Requirement 9: Pipeline de Despliegue Continuo

**User Story:** Como administrador de sistemas, quiero que el código se despliegue automáticamente al hacer push a main, para que los cambios lleguen a producción rápidamente.

#### Acceptance Criteria

1. WHEN se hace push a la rama main, THE Pipeline_CD SHALL ejecutarse automáticamente
2. THE Pipeline_CD SHALL conectarse al servidor mediante SSH
3. THE Pipeline_CD SHALL ejecutar git pull en el servidor
4. THE Pipeline_CD SHALL ejecutar docker compose -f docker-compose.prod.yml up -d --build
5. THE Pipeline_CD SHALL ejecutar migraciones de base de datos
6. THE Pipeline_CD SHALL utilizar los secrets: SERVER_HOST, SERVER_USER, SERVER_SSH_KEY
7. IF la conexión SSH falla, THEN THE Pipeline_CD SHALL reportar el error

### Requirement 10: Configuración Regional

**User Story:** Como usuario hispanohablante, quiero que el sistema esté configurado en español, para que las fechas y mensajes estén en mi idioma.

#### Acceptance Criteria

1. THE Sistema SHALL configurar LANGUAGE_CODE como 'es-es'
2. THE Sistema SHALL configurar TIME_ZONE como 'Europe/Madrid'
3. THE Sistema SHALL utilizar USE_I18N=True
4. THE Sistema SHALL utilizar USE_TZ=True

### Requirement 11: App Core - Páginas Principales

**User Story:** Como usuario, quiero acceder a la página principal y navegación del sitio, para que pueda orientarme en la documentación.

#### Acceptance Criteria

1. THE App_Core SHALL gestionar la página de inicio
2. THE App_Core SHALL gestionar la navegación principal
3. THE App_Core SHALL gestionar páginas estáticas generales
4. THE App_Core SHALL incluir models.py, views.py, urls.py, admin.py

### Requirement 12: App Tutorials - Tutoriales

**User Story:** Como usuario, quiero consultar tutoriales paso a paso, para que pueda aprender Reflex de forma estructurada.

#### Acceptance Criteria

1. THE App_Tutorials SHALL almacenar tutoriales en la base de datos
2. THE App_Tutorials SHALL permitir listar todos los tutoriales
3. THE App_Tutorials SHALL permitir ver el detalle de un tutorial
4. THE App_Tutorials SHALL incluir models.py, views.py, urls.py, admin.py

### Requirement 13: App Components - Referencia de API

**User Story:** Como usuario, quiero consultar la referencia de componentes de Reflex, para que pueda entender cómo usar cada componente.

#### Acceptance Criteria

1. THE App_Components SHALL almacenar documentación de componentes
2. THE App_Components SHALL permitir listar todos los componentes
3. THE App_Components SHALL permitir ver el detalle de un componente
4. THE App_Components SHALL incluir models.py, views.py, urls.py, admin.py

### Requirement 14: App Playground - Ejemplos Interactivos

**User Story:** Como usuario, quiero ver ejemplos de código con resaltado de sintaxis, para que pueda entender mejor los conceptos.

#### Acceptance Criteria

1. THE App_Playground SHALL mostrar ejemplos de código
2. THE App_Playground SHALL utilizar highlight.js para resaltado de sintaxis
3. THE App_Playground SHALL permitir listar ejemplos por categoría
4. THE App_Playground SHALL incluir models.py, views.py, urls.py, admin.py

### Requirement 15: App Accounts - Gestión de Usuarios

**User Story:** Como usuario, quiero registrarme y gestionar mi perfil, para que pueda personalizar mi experiencia.

#### Acceptance Criteria

1. THE App_Accounts SHALL permitir registro de nuevos usuarios
2. THE App_Accounts SHALL permitir login de usuarios existentes
3. THE App_Accounts SHALL permitir logout de usuarios autenticados
4. THE App_Accounts SHALL permitir ver y editar el perfil de usuario
5. THE App_Accounts SHALL incluir models.py, views.py, urls.py, admin.py

### Requirement 16: Panel de Administración

**User Story:** Como administrador, quiero gestionar el contenido desde el panel de Django Admin, para que pueda crear y editar tutoriales y componentes.

#### Acceptance Criteria

1. THE Sistema SHALL habilitar el panel de administración de Django
2. THE Sistema SHALL registrar los modelos de todas las apps en admin.py
3. WHEN un Administrador accede a /admin, THE Sistema SHALL mostrar el panel de administración
4. THE Sistema SHALL requerir autenticación para acceder al panel de administración

### Requirement 17: Dependencias de Desarrollo

**User Story:** Como desarrollador, quiero herramientas de testing y linting, para que pueda mantener la calidad del código.

#### Acceptance Criteria

1. THE Sistema SHALL incluir flake8 en requirements-dev.txt
2. THE Sistema SHALL incluir pytest y pytest-django en requirements-dev.txt
3. THE Sistema SHALL incluir coverage en requirements-dev.txt
4. THE Sistema SHALL separar dependencias de desarrollo de las de producción

### Requirement 18: Estrategia de Ramas Git

**User Story:** Como equipo de desarrollo, queremos seguir una estrategia de ramas clara, para que el flujo de trabajo sea ordenado.

#### Acceptance Criteria

1. THE Sistema SHALL utilizar la rama "main" para código de producción
2. THE Sistema SHALL utilizar la rama "develop" para integración
3. THE Sistema SHALL utilizar ramas "feature/*" para nuevas funcionalidades
4. THE Sistema SHALL utilizar ramas "hotfix/*" para correcciones urgentes
5. THE Sistema SHALL proteger las ramas main y develop requiriendo pull requests

### Requirement 19: Configuración de Nginx

**User Story:** Como administrador de sistemas, quiero que Nginx actúe como reverse proxy, para que el sistema maneje múltiples conexiones eficientemente.

#### Acceptance Criteria

1. THE Sistema SHALL incluir un archivo nginx.conf
2. THE Nginx SHALL escuchar en el puerto 80
3. THE Nginx SHALL hacer proxy_pass a Gunicorn
4. THE Nginx SHALL servir archivos estáticos desde /static
5. THE Nginx SHALL configurar timeouts apropiados

### Requirement 20: Soporte para Imágenes

**User Story:** Como administrador, quiero poder subir imágenes para tutoriales y componentes, para que el contenido sea más visual.

#### Acceptance Criteria

1. THE Sistema SHALL incluir Pillow en requirements.txt
2. THE Sistema SHALL configurar MEDIA_ROOT y MEDIA_URL
3. THE Sistema SHALL permitir subir imágenes desde el panel de administración
